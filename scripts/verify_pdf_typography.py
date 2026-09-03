"""Verify the publication font contract. Requires pypdf."""
from collections import Counter
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT/'deliverables/facility-portfolio.pdf'
ALLOWED = {'/LMRoman10-Regular', '/LMRoman10-Bold', '/LMRoman10-Italic', '/LMRoman10-BoldItalic'}

def verify():
    reader = PdfReader(PDF)
    assert len(reader.pages) == 10, f'Expected 10 pages, found {len(reader.pages)}'
    used = Counter()
    def visitor(text, _cm, _tm, font, _size):
        if text.strip():
            used[str(font.get('/BaseFont')) if font else '<missing>'] += len(text.strip())
    for page in reader.pages:
        page.extract_text(visitor_text=visitor)
    assert used, 'No extractable PDF text found'
    assert set(used) <= ALLOWED, f'Unexpected fonts used for text: {sorted(set(used)-ALLOWED)}'
    assert '/LMRoman10-Regular' in used and '/LMRoman10-Bold' in used, used

    embedded = set()
    for page in reader.pages:
        for item in page['/Resources'].get('/Font', {}).values():
            font = item.get_object()
            name = str(font.get('/BaseFont'))
            descriptor = font.get('/FontDescriptor')
            if descriptor and descriptor.get_object().get('/FontFile'):
                embedded.add(name)
    assert set(used) <= embedded, f'Used fonts not embedded: {sorted(set(used)-embedded)}'
    print(f'PASS: {len(reader.pages)} pages use only embedded Latin Modern text fonts: {dict(used)}')

if __name__ == '__main__':
    verify()
