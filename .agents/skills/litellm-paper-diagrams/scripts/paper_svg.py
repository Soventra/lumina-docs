"""Small SVG drawing primitives for LiteLLM paper diagrams; standard library only."""
from html import escape
from pathlib import Path

PAPER = '#fbfcfe'
INK = '#18334b'
BLUE = '#123ec9'
MUTED = '#597189'
LINE = '#9db2ce'
PANEL = '#f0f5fc'

class Figure:
    def __init__(self, title, description, height=640, width=1040, eyebrow=None, heading=False, offset_y=0):
        self.width, self.height = width, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">', f'<title id="title">{escape(title)}</title>', f'<desc id="desc">{escape(description)}</desc>', '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M2 1L9 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.4" stroke-linejoin="round"/></marker></defs>']
        self.rect(0, 0, width, height, PAPER, PAPER, 0)
        if eyebrow:
            self.text(40, 35, eyebrow, 12, MUTED, mono=True)
        if heading:
            self.text(40, 78, title, 29, INK, weight=500)
        self.offset_y = offset_y
        if offset_y:
            self.parts.append(f'<g transform="translate(0,{offset_y})">')
    def text(self, x, y, value, size=20, color=INK, anchor='start', weight=400, mono=False):
        font = 'monospace' if mono else 'Arial, Helvetica, sans-serif'
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{escape(str(value))}</text>')
    def rect(self, x, y, width, height, fill='white', stroke=LINE, radius=6):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>')
    def path(self, data, color=BLUE, width=1.8, dash=None, arrow=False):
        attrs = f' stroke-dasharray="{dash}"' if dash else ''
        attrs += ' marker-end="url(#arrow)"' if arrow else ''
        self.parts.append(f'<path d="{data}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{attrs}/>')
    def grid(self, x, y, width, height, spacing=24):
        self.parts.append('<g fill="#8aa6cc" opacity="0.23" aria-hidden="true">')
        for px in range(x, x+width+1, spacing):
            for py in range(y, y+height+1, spacing):
                self.parts.append(f'<circle cx="{px}" cy="{py}" r="0.75"/>')
        self.parts.append('</g>')
    def save(self, output):
        Path(output).write_text('\n'.join(self.parts + (['</g>'] if self.offset_y else []) + ['</svg>'])+'\n')
