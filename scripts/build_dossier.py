"""Optional publication exporter: python -m pip install reportlab; run from repo root."""
from pathlib import Path
import csv
import json
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import landscape, A4
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon
from reportlab.graphics import renderSVG
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import EmbeddedType1Face, Font

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT/'assets/fonts/latin-modern'

def register_latex_fonts():
    """Embed Latin Modern, the closest maintained form of LaTeX's default Computer Modern."""
    definitions = [
        ('LatinModern', 'lmr10'),
        ('LatinModern-Bold', 'lmbx10'),
        ('LatinModern-Italic', 'lmri10'),
        ('LatinModern-BoldItalic', 'lmbxi10'),
    ]
    for alias, stem in definitions:
        face = EmbeddedType1Face(str(FONT_DIR/f'{stem}.afm'), str(FONT_DIR/f'{stem}.pfb'))
        # Latin Modern AFM files encode these metrics as decimal strings;
        # ReportLab expects numeric ascent/descent during paragraph layout.
        face.ascent = float(face.ascent)
        face.descent = float(face.descent)
        pdfmetrics.registerTypeFace(face)
        pdfmetrics.registerFont(Font(alias, face.name, 'WinAnsiEncoding'))
    pdfmetrics.registerFontFamily(
        'LatinModern', normal='LatinModern', bold='LatinModern-Bold',
        italic='LatinModern-Italic', boldItalic='LatinModern-BoldItalic')

register_latex_fonts()
R = json.loads((ROOT/'artifacts/reference/report.json').read_text())
C = json.loads((ROOT/'configs/tropical-5mw.json').read_text())
NAVY = colors.HexColor('#102A43')
TEAL = colors.HexColor('#0F766E')
GRAY = colors.HexColor('#486581')
PALE = colors.HexColor('#E7F3F1')
LIGHT = colors.HexColor('#F1F5F9')
AMBER = colors.HexColor('#92400E')

def arrow(d, x1,y1,x2,y2,color=GRAY):
    d.add(Line(x1,y1,x2,y2,strokeColor=color,strokeWidth=2))
    if x1==x2:
        sign=1 if y2>y1 else -1
        d.add(Polygon([x2,y2,x2-4,y2-8*sign,x2+4,y2-8*sign],fillColor=color,strokeColor=color))
    else:
        sign=1 if x2>x1 else -1
        d.add(Polygon([x2,y2,x2-8*sign,y2-4,x2-8*sign,y2+4],fillColor=color,strokeColor=color))

def box(d,x,y,w,h,title,sub='',fill=LIGHT):
    d.add(Rect(x,y,w,h,rx=5,ry=5,fillColor=fill,strokeColor=colors.HexColor('#BCCCDC')))
    d.add(String(x+w/2,y+h/2+(6 if sub else -4),title,fontName='LatinModern-Bold',fontSize=13,textAnchor='middle',fillColor=NAVY))
    if sub:d.add(String(x+w/2,y+h/2-12,sub,fontName='LatinModern',fontSize=11,textAnchor='middle',fillColor=GRAY))

def electrical():
    d=Drawing(1000,400)
    for row,path in [(225,'A'),(75,'B')]:
        box(d,10,row+85,315,55,f'UTILITY INTERFACE {path} / 20 kV','Upstream independence unverified')
        arrow(d,65,row+85,65,row+55)
        box(d,10,row,110,55,f'MV-{path}','switchgear')
        box(d,155,row,170,55,f'TX-{path}: 3 x 4 MVA','2 duty + 1 spare')
        box(d,360,row,130,55,f'LV-{path}','400 V example')
        box(d,525,row,170,55,f'UPS-{path}: 6 x 1.25 MW','5 duty + 1 spare',PALE)
        box(d,730,row,110,55,f'PDU-{path}','rack interface')
        box(d,885,row,105,55,f'RACK {path}','dual cord')
        for x1,x2 in [(120,155),(325,360),(490,525),(695,730),(840,885)]:arrow(d,x1,row+27,x2,row+27)
        box(d,350,row-50,150,37,f'GEN-{path}: 4 x 3 MW',fill=PALE)
        arrow(d,425,row-13,425,row)
    d.add(String(12,8,'Concept block SLD | breaker, protection, earthing, ties and auxiliary circuits require detailed design.',fontName='LatinModern',fontSize=12,fillColor=AMBER))
    return d

def cooling():
    d=Drawing(1000,350)
    box(d,20,135,200,80,'CHILLER PLANT','6 x 1.25 MWth; 5 + 1',PALE)
    box(d,290,135,180,80,'FWS / CHW LOOP','Shared header; 6 K rise')
    box(d,560,240,200,70,'AIR TERMINALS','3.5 MW IT heat')
    box(d,560,40,200,70,'CDUs / 4 HALLS','2 x 500 kWth per hall')
    box(d,835,240,145,70,'AIR IT','rack inlet')
    box(d,835,40,145,70,'LIQUID IT','1.5 MW heat')
    arrow(d,220,175,290,175)
    arrow(d,470,175,515,175)
    d.add(Line(515,75,515,275,strokeColor=GRAY,strokeWidth=2))
    arrow(d,515,275,560,275);arrow(d,515,75,560,75)
    arrow(d,760,275,835,275);arrow(d,760,75,835,75)
    d.add(String(805,120,'TCS boundary',fontName='LatinModern',fontSize=12,fillColor=GRAY))
    d.add(String(20,315,'Facility cooling interfaces / conceptual supply direction',fontName='LatinModern-Bold',fontSize=18,fillColor=NAVY))
    d.add(String(20,15,'Concept flow diagram | supply/return collapsed; isolation, hydraulics, chemistry and thermal ride-through remain open.',fontName='LatinModern',fontSize=12,fillColor=AMBER))
    return d

def scaled(d,width):
    factor=width/d.width
    result=Drawing(width,d.height*factor)
    from reportlab.graphics.shapes import Group
    group=Group(*d.contents)
    group.scale(factor,factor)
    result.add(group)
    return result

def energy_chart():
    d=Drawing(720,235)
    d.add(String(0,222,'Annual gross facility energy includes IT plus supporting systems',fontName='LatinModern',fontSize=13,fillColor=NAVY))
    for i,m in enumerate(R['energy']['monthly']):
        x=35+i*56;it=m['it_kwh']/1e6;over=(m['facility_kwh']-m['it_kwh'])/1e6
        d.add(Rect(x,30,30,it*40,fillColor=TEAL,strokeColor=None))
        d.add(Rect(x,30+it*40,30,over*40,fillColor=colors.HexColor('#B8D8D3'),strokeColor=None))
        d.add(String(x+15,14,str(i+1),fontName='LatinModern',textAnchor='middle',fontSize=10,fillColor=GRAY))
    for v in range(5):
        d.add(String(20,27+v*40,str(v),fontName='LatinModern',textAnchor='end',fontSize=10,fillColor=GRAY))
    d.add(String(0,198,'GWh',fontName='LatinModern',fontSize=10,fillColor=GRAY))
    d.add(Rect(470,190,12,12,fillColor=TEAL,strokeColor=None));d.add(String(488,191,'IT',fontName='LatinModern',fontSize=10))
    d.add(Rect(530,190,12,12,fillColor=colors.HexColor('#B8D8D3'),strokeColor=None));d.add(String(548,191,'Facility overhead',fontName='LatinModern',fontSize=10))
    return d

def cover_plan():
    d=Drawing(710,125)
    for hall in range(4):
        x=hall*178
        box(d,x,0,160,115,f'H{hall+1:02} / 1.25 MW',fill=PALE)
        # Draw fifty abstract rack cells, no claim of architectural geometry.
        for n in range(50):
            d.add(Rect(x+12+(n%10)*13.5,12+(n//10)*8,8,5,fillColor=TEAL,strokeColor=None))
    return d

def build():
    for path,d in [('05_electrical/single-line-concept.svg',electrical()),('06_mechanical/cooling-loop-concept.svg',cooling())]:
        renderSVG.drawToFile(d,str(ROOT/path))
    dest=ROOT/'deliverables';dest.mkdir(exist_ok=True)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TitleDC',fontName='LatinModern-Bold',fontSize=30,leading=35,textColor=NAVY,spaceAfter=14))
    styles.add(ParagraphStyle(name='SectionDC',fontName='LatinModern-Bold',fontSize=22,leading=28,textColor=NAVY,spaceAfter=12))
    styles.add(ParagraphStyle(name='BodyDC',fontName='LatinModern',fontSize=11,leading=16,textColor=GRAY,spaceAfter=10))
    styles.add(ParagraphStyle(name='SmallDC',fontName='LatinModern',fontSize=9,leading=12,textColor=GRAY,spaceAfter=6))
    story=[]
    def p(t,style='BodyDC'):return Paragraph(t,styles[style])
    def add(t):story.append(p(t))
    def page(title):
        if story:story.append(PageBreak())
        story.append(p(title,'SectionDC'))
    def table(rows,widths):
        content=[[p(escape(str(cell)),'SmallDC') for cell in row] for row in rows]
        t=Table(content,colWidths=widths,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),
                              ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
                              ('LINEBELOW',(0,0),(-1,0),1,TEAL),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT])]))
        story.append(t);story.append(Spacer(1,10))
    e,f,s=R['energy'],R['finance'],R['sizing']
    story.append(p('OPEN DATA CENTER<br/>FACILITY ENGINEERING','TitleDC'))
    add('A building-only, end-to-end concept portfolio<br/><b>Jonathan Oktaviano</b> | Reference release 0.1.0 | 3 September 2026')
    story.append(Spacer(1,12));story.append(cover_plan());story.append(Spacer(1,16))
    table([['DESIGN IT','ANNUAL PUE','CONCEPT CAPEX','IMPLEMENTED EVIDENCE'],
           ['5.00 MW',f'{e["pue"]:.3f}','USD 57.60 million','8760-hour model + six offline cases']],[175,175,175,185])
    add('One scenario connects requirements, power, cooling, energy, facility economics, asset identities and commissioning examples. Source code, source records and original drawings accompany this dossier.')
    story.append(p('Independent portfolio. No AWS affiliation or proprietary hyperscaler design. Synthetic inputs; concept engineering; not certified or for construction.','SmallDC'))

    page('01 / Executive decision')
    add('<b>Keep the base case transparent.</b> Its slightly negative NPV shows why engineering design and commercial assumptions must be assessed together. No real-site investment conclusion is established.')
    table([['RESULT','VALUE','INTERPRETATION'],
           ['Design facility input',f'{s["design_balance"]["facility_kw"]/1000:.3f} MW','Full IT at 35 C; sizing margin applied afterward'],
           ['Annual gross facility energy',f'{e["facility_kwh"]/1e6:.3f} GWh','Fully leased; 75% mean draw; synthetic weather'],
           ['Pre-tax unlevered NPV',f'USD {f["npv_usd"]/1e6:.3f} million','15 years; 10% nominal discount'],
           ['Conventional IRR',f'{f["irr"]:.2%}','Not a levered equity return'],
           ['Simple payback',f'{f["simple_payback_years"]:.2f} years','Undiscounted first crossing']],[215,180,315])
    add('Capital is an author-selected USD 48m base allowance plus 20% contingency. Capacity pricing is USD 180/kW-month with a 35-95% occupancy ramp. Energy reimbursement is 100%; rent and electricity recovery remain separate cash-flow lines.')
    add('<b>Next evidence:</b> utility connection and site hazards; equipment and contractor quotations; lease terms; construction phasing; cooling ride-through; detailed isolation and protection design.')

    page('02 / Electrical concept and capacity')
    story.append(scaled(electrical(),720));story.append(Spacer(1,10))
    add('Each A/B path has a full-facility capacity allowance with one local unit unavailable. Total installed A+B nameplate is redundancy, not twice the customer demand. Supporting loads connect outside the IT UPS boundary; their detailed feeders are omitted here.')
    add(f'Battery allowance: <b>{s["battery_per_path_kwh"]:,.0f} kWh per path</b> for ten minutes at modeled UPS output, after inverter, usable-energy and end-of-life factors. This is not a battery-string selection or cooling ride-through result.')
    story.append(p('Outstanding: utility/fault data, breaker/tie arrangement, protection coordination, earthing, cable sizing, generator dynamics, physical route separation and auxiliary power.','SmallDC'))

    page('03 / Cooling and interface design')
    story.append(scaled(cooling(),720));story.append(Spacer(1,8))
    table([['QUANTITY','SCREENING RESULT','BOUNDARY'],
           ['Total design cooling load',f'{s["design_balance"]["cooling_kwth"]:,.0f} kWth','IT, UPS/distribution losses, terminal fans, envelope'],
           ['CHW mass flow',f'{s["chw_mass_flow_kg_s"]:.1f} kg/s','Water approximation; 6 K rise'],
           ['Air-side volume flow',f'{s["air_volume_flow_m3_s"]:.1f} m3/s','Air IT + terminal fans; 12 K rise']],[210,180,320])
    add('The shared loop is an explicit common-path risk. Hydraulic isolation, water chemistry, condensation limits, pump selection and thermal transients need further design. The displayed layout is an original concept, not a copied vendor P&amp;ID.')

    page('04 / Energy and sustainability')
    story.append(energy_chart())
    add(f'Annual IT energy is {e["it_kwh"]/1e6:.2f} GWh and gross facility energy is {e["facility_kwh"]/1e6:.2f} GWh. PUE is the ratio of annual energies, not an average of hourly ratios. Gross facility demand remains unchanged by optional PV accounting.')
    add(f'At the illustrative factors, grid emissions are {e["operational_grid_tco2e"]:,.0f} tCO2e/year and direct-site water is {e["direct_site_water_m3"]:,.0f} m3/year. These are factor-based scenario outputs, not measured Indonesia performance. Baseline PV is zero; BESS has no annual dispatch model.')
    story.append(p('Excludes humidity/latent loads, vendor part-load maps, embodied materials, refrigerants, diesel and upstream water. Source definitions: DOE/FEMP guidance, S01 and S14 in the source register.','SmallDC'))

    page('05 / Economics and sensitivity')
    with (ROOT/'artifacts/reference/sensitivity.csv').open() as stream: sens=list(csv.DictReader(stream))
    grid=[['CAPEX / CAPACITY PRICE','80%','100%','120%']]
    for factor in (0.8,1.0,1.2):
        vals=[r for r in sens if float(r['capex_factor'])==factor]
        grid.append([f'{factor:.0%}']+[f'USD {float(r["npv_usd"])/1e6:+.2f}m' for r in vals])
    add('NPV at the 10% nominal discount rate. Both drivers change the underlying cash-flow model; maintenance and residual value follow the changed base CAPEX.')
    table(grid,[245,155,155,155])
    add('Power charges use imported energy and monthly demand peaks. In the 100% reimbursement base case, electricity costs cancel against recovery in net cash flow. This does not remove the gross utility expense or credit/contract risk.')
    add('Replacement allowance occurs in year eight; residual asset recovery occurs in year fifteen. The model has no debt, tax, working capital or construction-period cash flow. Test zero residual, lower reimbursement and delayed occupancy before interpreting financial attractiveness.')
    story.append(p('Method reference: NIST HB 135e2025 for lifecycle discounting concepts; all prices, rates and terms are synthetic project assumptions. The editable workbook exposes inputs, formulas, sensitivity and checks.','SmallDC'))

    page('06 / Lifecycle coverage and honest maturity')
    table([['LIFECYCLE','DELIVERED','NEXT EVIDENCE GATE'],
           ['Define / select','OPR, assumptions, site gates, charter','Owner and real-site evidence'],
           ['Value / design','Sizing, energy, cash flow, original concepts','Quotes, calibrated curves, detailed studies'],
           ['Coordinate','DXF/SVG and rack-only OpenUSD with matching IDs','Survey, coordinated BIM and validated CFD'],
           ['Control / assure','Points, six offline cases, FMEA and common-cause model','Hardware tests and topology validation'],
           ['Build / commission','Procurement gates, FAT/SAT/IST plan','Witnessed physical evidence'],
           ['Operate / improve','SOP/MOP/EOP, maintenance and dashboard specification','Site approval, drills and historian integration']],[150,300,260])
    add('The repository retains the requested lifecycle structure and adds a shared calculation package, strict schema, requirements traceability, source/license records, automated tests and hashed evidence. Each claimed maturity level has an explicit limit.')
    add('The portfolio emphasizes a reviewable chain: requirement -> input -> equation -> equipment/geometry -> risk -> verification. Folders that specify future CFD/BIM work are labeled as specifications, not completed solver results.')

    page('07 / Commissioning and operational evidence')
    table([['CASE','OBSERVATION','EXPECTED SUPERVISORY STATE','RESULT']]+[
        [r['id'],['Normal supply','Utility lost','Generator ready','No remaining supply','Telemetry stale','Leak and high inlet temperature'][i],r['expected_source'],'PASS' if r['passed'] else 'FAIL']
        for i,r in enumerate(R['commissioning'])],[85,240,270,115])
    add('These are six offline software checks, not physical integrated tests. They confirm state/alarms and the disabled-write boundary. Real acceptance requires approved procedures, safe prerequisites, instruments, witness records, deviations and operations sign-off.')
    add('Operational handover links asset records, current drawings, manuals, settings, spares, training, maintenance restrictions and incident procedures. A stale-data condition produces UNKNOWN, preventing a healthy-looking dashboard from being treated as trustworthy evidence.')
    story.append(p('The local model tests also cover dimensional balances, adverse inputs, PV curtailment, financial sign patterns, geometry IDs and common-cause availability. Remote CI remains pending user upload.','SmallDC'))

    sources=json.loads((ROOT/'research/sources.json').read_text())
    for index, group in enumerate((sources[:8],sources[8:]),8):
        page(f'0{index} / Primary sources and access boundaries')
        for source in group:
            label=escape(source['title'])
            url=escape(source['url'],{'"':'&quot;'})
            story.append(p(f'<b>{source["id"]} · <a href="{url}" color="#0F766E">{label}</a></b><br/>{escape(source["publisher"])} | {escape(source["publication"])}<br/>{escape(source["access_notes"])}','SmallDC'))
        if index==9:
            add('Accessed 3 September 2026. Research inspected relevant sections and source records, not every page of every cited work. Vendor runtimes and calculators were not executed. Full current ASHRAE content and the RD100 PDF remained inaccessible. Original project prose, diagrams and data are provided; external assets retain their own terms.')
    def footer(canv,doc):
        canv.setStrokeColor(colors.HexColor('#D9E2EC'));canv.line(48,34,794,34)
        canv.setFont('LatinModern',8);canv.setFillColor(GRAY)
        canv.drawString(48,22,'OPEN DATA CENTER FACILITY | 0.1.0 | CONCEPT / SYNTHETIC DATA')
        canv.drawRightString(794,22,str(doc.page))
    doc=SimpleDocTemplate(str(dest/'facility-portfolio.pdf'),pagesize=landscape(A4),rightMargin=48,leftMargin=48,topMargin=38,bottomMargin=45,
                          title='Open Data Center Facility — Portfolio Dossier',author='Jonathan Oktaviano')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(dest/'facility-portfolio.pdf')

if __name__=='__main__':build()
