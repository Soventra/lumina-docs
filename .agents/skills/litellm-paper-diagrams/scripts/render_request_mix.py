"""Selected quiet Sankey: cumulative eligibility and aligned option rows."""
from fractions import Fraction as Q
from pathlib import Path
import json
import argparse

from paper_svg import Figure, BLUE, INK, MUTED


def band(f, a, b, y1, y2, color):
    x1,x2 = a; x3,x4 = b; bend = (y2-y1)*.52
    d = (f'M{x1:.3f} {y1}C{x1:.3f} {y1+bend:.3f} {x3:.3f} {y2-bend:.3f} {x3:.3f} {y2}'
         f'L{x4:.3f} {y2}C{x4:.3f} {y2-bend:.3f} {x2:.3f} {y1+bend:.3f} {x2:.3f} {y1}Z')
    f.parts.append(f'<path d="{d}" fill="{color}" stroke="{color}" stroke-width="0.3"/>')


def option(f,x,y,w,label,checkbox=False):
    f.rect(x,y,w,54,'#e8efff',BLUE,5)
    if checkbox:
        f.rect(x+12,y+20,14,14,BLUE,BLUE,2)
        f.path(f'M{x+15} {y+27}l3 3 6-7','#fff',width=1.6)
        f.text(x+35,y+33,label,18,BLUE)
    else: f.text(x+w/2,y+33,label,19,BLUE,anchor='middle')


def render(destination, model):
    f=Figure('Requests retain fast-path eligibility or move to Python',
        'One input splits at the top into blue fast-path candidates and gray Python requests. Horizontally aligned option rows show endpoint, routing, callbacks and providers. More requests branch away between every pair of rows, including endpoint and routing, and join the left edge of the Python lane. Blue means eligible so far; only the final blue stream reaches Rust. Endpoints, routing strategies and providers each allow one choice. Callbacks allow any combination of supported options; an unsupported callback sends the request to Python. Bedrock and Vertex eligibility applies to Anthropic models. Widths are synthetic, not production telemetry, and have no numeric labels.',height=1400)
    f.rect(25,34,16,16,BLUE,BLUE,2); f.text(52,48,'Fast-path eligible so far',17,INK)
    f.rect(359,34,16,16,'#c4cedc','#c4cedc',2); f.text(386,48,'Other requests',17,MUTED)
    f.text(1000,48,'Illustrative flow',15,MUTED,anchor='end')
    f.text(660,96,'Requests',21,INK,anchor='middle',weight=500)
    f.text(40,266,'Fast-path eligibility',22,INK,weight=500)
    f.text(690,266,'Python',22,INK,weight=500)
    left,scale,rail_right=390,340,980
    rows=[(280,142),(550,142),(820,166),(1114,142)]
    f.parts.append('<defs><linearGradient id="blue-flow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#88aaf2"/><stop offset="1" stop-color="#123ec9"/></linearGradient></defs>')
    remaining=Q(model['initial_eligible_share'])
    # Adjacent sub-bands form one incoming trunk, then visibly diverge.
    source_left=490
    source_split=source_left+float(remaining)*scale
    initial_rail_left=rail_right-float(1-remaining)*scale
    band(f,(source_left,source_split),(source_left,source_split),110,135,'#88aaf2')
    band(f,(source_split,source_left+scale),(source_split,source_left+scale),110,135,'#c7d1df')
    band(f,(source_left,source_split),(left,left+float(remaining)*scale),135,250,'url(#blue-flow)')
    band(f,(source_split,source_left+scale),(initial_rail_left,rail_right),135,250,'#c7d1df')
    band(f,(left,left+float(remaining)*scale),(left,left+float(remaining)*scale),250,rows[0][0],BLUE)
    first_merge=rows[1][0]-20
    band(f,(initial_rail_left,rail_right),(initial_rail_left,rail_right),250,first_merge,'#c7d1df')
    for idx, ((y,h),stage) in enumerate(zip(rows,model['stages'])):
        current=remaining; remaining=Q(stage['eligible_share_of_all_requests'])
        assert 0 < remaining <= current <= 1
        departed=current-remaining
        assert remaining+(1-current)+departed == 1
        sy=y+h
        merge=rows[idx+1][0]-20 if idx<3 else 1340
        end_y=rows[idx+1][0] if idx<3 else 1360
        band(f,(left,left+float(remaining)*scale),(left,left+float(remaining)*scale),sy,end_y,'url(#blue-flow)')
        if departed:
            band(f,(left+float(remaining)*scale,left+float(current)*scale),
                (rail_right-float(1-remaining)*scale,rail_right-float(1-current)*scale),sy,merge,'#c7d1df')
        rail_left=rail_right-float(1-remaining)*scale
        rail_end=rows[idx+2][0]-20 if idx<2 else (1340 if idx==2 else 1360)
        band(f,(rail_left,rail_right),(rail_left,rail_right),merge,rail_end,'#c7d1df')
    for idx,((y,h),stage) in enumerate(zip(rows,model['stages'])):
        f.rect(40,y,610,h,'#f8faff','#b5c5dc',7)
        f.text(60,y+29,stage['label'],20,INK,weight=500)
        f.text(630,y+29,'Choose many' if stage['selection_mode']=='many' else 'Choose one',15,MUTED,anchor='end')
        if idx<2: option(f,60,y+48,570,stage['supported'][0])
        elif idx==2:
            f.text(60,y+55,'Any combination of supported callbacks',17,MUTED)
            option(f,60,y+70,278,'S3 logs',checkbox=True)
            option(f,352,y+70,278,'Spend logging',checkbox=True)
            f.text(60,y+149,'Every enabled callback must be supported',17,MUTED)
        else:
            option(f,60,y+48,174,'Anthropic')
            option(f,246,y+48,194,'Amazon Bedrock')
            option(f,452,y+48,178,'Vertex AI')
            f.text(60,y+125,'Anthropic models',15,MUTED)
        oh=105 if idx==2 else 88
        oy=y+(h-oh)/2
        assert oy+oh/2 == y+h/2
        f.rect(690,oy,310,oh,'#f5f7fa','#cbd5e1',6)
        for n,line in enumerate(stage['other']):f.text(710,oy+29+n*24,line,17,MUTED)
    f.text(left+float(remaining)*scale/2,1385,'Rust',21,BLUE,anchor='middle',weight=500)
    f.text(rail_right-float(1-remaining)*scale/2,1385,'Python',21,INK,anchor='middle',weight=500)
    f.save(destination)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    render(args.output, json.loads(args.model.read_text()))
