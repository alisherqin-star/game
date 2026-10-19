"""Native-resolution organic pixel drawing primitives shared by scene generators.

Curves are rasterized directly: no blur, resampling, or alpha feathering.
"""
import math
import random
from PIL import Image, ImageDraw


# Distance, secondary material, local light, and mist are separate hue families.
# They are intentionally softer than collectible / danger colors.
LOOKS = {
 'lake': ('#5d8f9d','#9aab83','#e2c190','#c7d9c4'),
 'cave': ('#4a587e','#726486','#77b9b6','#92acb8'),
 'tower': ('#55596f','#8d796b','#e2ba78','#a8a4b2'),
 'sewer': ('#405f6c','#7c7654','#bcbb79','#8ba797'),
 'volcano': ('#4a405d','#89615b','#e4a15f','#9f7d8c'),
 'canopy': ('#486e80','#617f59','#d7bc79','#a9c8a9'),
 'heartwood': ('#3b6663','#8c6650','#d9b871','#a5b18a'),
 'snow': ('#657baf','#a29daf','#e9cead','#e3e5e7'),
 'ice': ('#5a6390','#718baf','#d7c0df','#b9dddb'),
 'sky': ('#668aa3','#8c9b88','#dfbe87','#e9e0c5'),
 'wind': ('#6d7d9d','#9d9b8d','#dcad8e','#ddd9d1'),
 'grave': ('#4a4e76','#697986','#d8ae7d','#a9a2bf'),
 'shadow': ('#494d79','#76546e','#cd9ea7','#aaa3c8'),
 'candy': ('#cfb9df','#a5d3b5','#ffe0a9','#fff1e5'),
 'abyss': ('#345772','#527b77','#b2a4cf','#88bfb8'),
 'core': ('#4d3856','#8c5b55','#e3b165','#b18c8e'),
 'altar': ('#666c98','#a49d8e','#e4c995','#c8c2da'),
}


def rgb(value):
    return tuple(bytes.fromhex(value[1:])) if isinstance(value, str) else tuple(value[:3])


def blend(a, b, amount):
    return tuple(round(x * (1 - amount) + y * amount) for x, y in zip(rgb(a), rgb(b)))


def soften(points, rounds=2, closed=False):
    """Chaikin corner cutting retains uneven masses instead of making perfect ovals."""
    pts = [(float(x), float(y)) for x, y in points]
    for _ in range(rounds):
        pairs = list(zip(pts, pts[1:] + ([pts[0]] if closed else [])))
        out = [] if closed else [pts[0]]
        for a, b in pairs:
            out.extend([(a[0]*.75+b[0]*.25, a[1]*.75+b[1]*.25),
                        (a[0]*.25+b[0]*.75, a[1]*.25+b[1]*.75)])
        if not closed:
            out.append(pts[-1])
        pts = out
    return [(round(x), round(y)) for x, y in pts]


def curve(draw, points, fill, width=1):
    draw.line(soften(points, 3), fill=fill, width=width, joint='curve')


def profile(x, phase=0, scale=1):
    """A periodic multiscale ridge: matching value AND slope at repeat boundaries."""
    x = x / 384 * math.tau
    return scale * (math.sin(x+phase)*12 + math.sin(x*3+phase*1.7)*7 +
                    math.sin(x*7+phase*.4)*3 + math.sin(x*13+phase)*1.4)


class Painter:
    def __init__(self, image, palette, seed=0):
        self.image = image
        self.d = ImageDraw.Draw(image)
        self.p = palette
        self.rng = random.Random(seed)

    def rock(self, box, color=None, snow=False, molten=False):
        x0, y0, x1, y1 = box
        w, h = x1-x0, y1-y0
        cx, cy = (x0+x1)/2, (y0+y1)/2
        points = []
        for i in range(13):
            angle = math.tau*i/13
            r = self.rng.uniform(.84, 1.05)
            points.append((cx+math.cos(angle)*w*.49*r, cy+math.sin(angle)*h*.49*r))
        points = soften(points, 1, True)
        body = color or self.p[0]
        self.d.polygon(points, fill=body, outline=self.p[1])
        # Rounded upper planes are grouped, with broken highlights instead of a frame.
        ridge = [(x0+w*.14,y0+h*.46),(x0+w*.27,y0+h*.16),
                 (x0+w*.54,y0+h*.11),(x0+w*.79,y0+h*.34)]
        curve(self.d, ridge, self.p[2], max(1, round(h/12)))
        curve(self.d, [(x0+w*.2,y0+h*.49),(x0+w*.38,y0+h*.39),
                       (x0+w*.52,y0+h*.48)], self.p[2])
        curve(self.d, [(x0+w*.56,y0+h*.34),(x0+w*.48,y0+h*.63),
                       (x0+w*.61,y0+h*.76)], self.p[1])
        if snow:
            cap=[(x0+w*.13,y0+h*.40),(x0+w*.27,y0+h*.12),(x0+w*.55,y0+h*.07),
                 (x0+w*.84,y0+h*.38),(x0+w*.72,y0+h*.47),(x0+w*.56,y0+h*.36),
                 (x0+w*.40,y0+h*.51),(x0+w*.24,y0+h*.41)]
            self.d.polygon(soften(cap, 2, True), fill=self.p[3])
        if molten:
            curve(self.d, [(cx-3,cy+3),(cx+4,cy+8),(cx+1,y1-4)], self.p[4])
        self.grain(30, body)

    def grain(self, count, base=None):
        """Sparse clustered pigment inside opaque faces; preserve alpha and contours."""
        width,height=self.image.size
        for _ in range(count):
            x=self.rng.randrange(1,max(2,width-2));y=self.rng.randrange(1,max(2,height-2))
            c=self.image.getpixel((x,y))
            if c[3]!=255 or (base and c[:3]!=rgb(base)):
                continue
            if self.image.getpixel((x+1,y))!=c or self.image.getpixel((x,y+1))!=c:
                continue
            factor=self.rng.choice([.06,.09,.13])
            tone=blend(c, '#ffffff' if self.rng.random()<.5 else '#111b26', factor)
            self.d.line((x,y,x+self.rng.choice([1,1,2]),y),fill=tone)

    def foliage(self, box, colors=None):
        colors=colors or [self.p[1],self.p[4],self.p[2],self.p[3]]
        x0,y0,x1,y1=box;w=x1-x0;h=y1-y0
        # Offset, overlapping leaf masses avoid equal-size scallops and black rings.
        for u,v,r in [(.24,.56,.32),(.48,.30,.35),(.71,.50,.34),(.51,.68,.39),(.84,.69,.19)]:
            cx=x0+w*u;cy=y0+h*v;rx=w*r;ry=h*r
            self.d.ellipse((round(cx-rx),round(cy-ry),round(cx+rx),round(cy+ry)),fill=colors[0])
            inner=(round(cx-rx+1),round(cy-ry),round(cx+rx-2),round(cy+ry-3))
            if inner[2]>=inner[0] and inner[3]>=inner[1]:self.d.ellipse(inner,fill=colors[1])
            self.d.ellipse((round(cx-rx+3),round(cy-ry+1),round(cx+rx-4),round(cy+ry-6)),fill=colors[2]) if ry>5 and rx>5 else None
        for _ in range(max(8,round(w*h/13))):
            x=self.rng.randrange(max(0,int(x0)),max(1,min(self.image.width,int(x1)+1)))
            y=self.rng.randrange(max(0,int(y0)),max(1,min(self.image.height,int(y1)+1)))
            if self.image.getpixel((x,y))[:3] in [rgb(colors[1]),rgb(colors[2])]:
                self.d.rectangle((x,y,min(self.image.width-1,x+1),y),fill=self.rng.choice(colors[1:]))

    def bough(self, points, width=5, color=None):
        curve(self.d, points, self.p[1], width+2)
        curve(self.d, [(x-1,y-1) for x,y in points], color or self.p[0], width)
        curve(self.d, [(x-1,y-1) for x,y in points], self.p[2], max(1,width//4))

    def old_arch(self, box, pointed=False):
        x,y,x1,y1=box;w=x1-x;h=y1-y
        for xx in (x,x1-9):
            self.d.rounded_rectangle((xx,y+17,xx+9,y1),radius=2,fill=self.p[0])
            self.d.line((xx+2,y+20,xx+2,y1-2),fill=self.p[2])
            for yy in range(y+23,y1,9):
                self.d.line((xx+1,yy,xx+8,yy),fill=self.p[1])
        if pointed:
            pts=[(x+5,y+24),(x+7,y+15),(x+w*.26,y+7),(x+w*.5,y),
                 (x+w*.75,y+7),(x1-6,y+15),(x1-4,y+24)]
            curve(self.d,pts,self.p[1],11);curve(self.d,pts,self.p[0],9)
            curve(self.d,[(xx,yy-1) for xx,yy in pts],self.p[2],3)
        else:
            self.d.arc((x,y,x1,y+44),180,360,fill=self.p[1],width=12)
            self.d.arc((x+1,y+1,x1-1,y+43),180,360,fill=self.p[0],width=9)
            self.d.arc((x+2,y+2,x1-2,y+42),185,315,fill=self.p[2],width=2)
        for xx in (x-2,x1-11):
            self.d.rounded_rectangle((xx,y1-5,xx+13,y1),radius=2,fill=self.p[2])
        # Uneven erosion and a few creeping leaves, not a bright outline everywhere.
        self.d.rectangle((x+1,y1-16,x+3,y1-12),fill=self.p[1])
        self.grain(65)


def natural_background(theme, sky, palette, layer, style=None):
    """Three calm, horizontally repeatable layers with curved ridges and aged motifs."""
    image=Image.new('RGBA',(384,224));d=ImageDraw.Draw(image)
    rng=random.Random(f'natural-{theme}-{layer}')
    distance,material,light,mist=LOOKS[theme]
    base=blend(sky[0],distance if layer<2 else material,.33+layer*.09)
    hi=blend(base,mist,.13+layer*.025)
    if theme=='candy':
        base=['#d7c6e6','#f1c8d7','#c4e1c2'][layer]
        hi=['#eee0f2','#ffe7ea','#e1efd1'][layer]
    shadow=blend(base,sky[0],.22)
    p=[base,shadow,hi,blend(hi,sky[1],.2),hi,hi]
    pen=Painter(image,p,theme+str(layer))
    outdoor=theme in ('lake','snow','sky','wind','canopy','grave','candy')
    if outdoor:
        # Distant clouds / low fog strips, not a repeating sawtooth mountain chain.
        if layer==0:
            for cx,cy,ww in [(32,53,67),(199,39,87),(334,85,58)]:
                for off in (-384,0,384):
                    for dx,dy,w,h in [(0,5,ww,9),(11,0,ww//2,13),(23,-4,ww//3,15)]:
                        d.ellipse((cx+dx+off,cy+dy,cx+dx+w+off,cy+dy+h),fill=blend(sky[0],sky[1],.28))
        if theme in ('lake','snow','grave','candy'):
            phase=layer*.93+(.5 if theme=='grave' else 0)
            ridge=[]
            for x in range(-2,387):
                height=profile(x,phase,1.0+layer*.16)
                if theme=='snow':height+=math.sin(x/384*math.tau*2+.7)*16
                y=round(125+layer*25+height)
                ridge.append((x,y))
            d.polygon(ridge+[(386,224),(-2,224)],fill=base)
            if theme=='snow':
                snowline=[(x,y+3+round(3*math.sin(x*.06))) for x,y in ridge]
                d.polygon(ridge+list(reversed(snowline)),fill=blend(base,sky[1],.27))
                for x in range(10,384,38):
                    y=ridge[x+2][1]
                    curve(d,[(x,y+7),(x+6,y+22),(x+11,y+38)],shadow)
            elif theme=='candy':
                for x in range(-28,410,82):
                    yy=157+layer*12+int(profile(x,layer,1))
                    for off in (-384,0,384):
                        d.ellipse((x+off,yy-37,x+off+69,yy+17),fill=hi)
            elif theme=='lake' and layer==2:
                for x in range(3,384,41):
                    yy=round(182+profile(x,layer,.2));curve(d,[(x,yy+11),(x+2,yy-2),(x-3,yy-13)],hi)
        if theme in ('sky','wind'):
            for i in range(4 if layer<2 else 3):
                cx=i*116+layer*23;yy=84+(i*37+layer*23)%88
                for off in (-384,0,384):
                    x=cx+off
                    pen.rock((x-30,yy,x+44,yy+24),base)
                    d.ellipse((x-30,yy-3,x+44,yy+5),fill=hi)
                    if theme=='sky':
                        pen.old_arch((x-14,yy-32,x+19,yy))
                        curve(d,[(x+5,yy+13),(x+6,yy+25),(x+2,yy+35)],shadow)
                    else:
                        d.rounded_rectangle((x-8,yy-88,x+15,yy),radius=7,fill=base)
                        d.arc((x-10,yy-90,x+17,yy-68),180,360,fill=hi,width=2)
                        for wy in range(yy-70,yy-10,20):
                            d.rounded_rectangle((x-1,wy,x+6,wy+11),radius=3,fill=shadow)
        if theme in ('canopy','grave'):
            for i in range(4):
                cx=i*108+layer*19
                for off in (-384,0,384):
                    x=cx+off
                    pen.bough([(x,224),(x+8,178),(x+4,121),(x+17,58),(x+9,-10)],8+layer*3,base)
                    pen.bough([(x+6,148),(x-17,111),(x-29,104)],4,base)
                    pen.bough([(x+8,120),(x+36,88),(x+44,52)],3,base)
                    if theme=='canopy':
                        for dx,dy in [(-25,2),(12,-10),(36,14)]:
                            # Clipped/wrapped lobes keep horizontal parallax seamless.
                            d.ellipse((x+dx-24,dy,x+dx+45,dy+63),fill=base)
                            d.ellipse((x+dx-20,dy+3,x+dx+37,dy+46),fill=hi)
                    else:
                        for dx in (-17,20):
                            d.rounded_rectangle((x+dx,204,x+dx+10,224),radius=4,fill=base)
    else:
        # Smoothly eroded cave roof and floor rather than identical hanging wedges.
        ceiling=[];floor=[]
        for x in range(-2,387):
            ceiling.append((x,round(21+layer*5+profile(x,layer*1.2,1.0+layer*.10))))
            floor.append((x,round(203-layer*7+profile(x,layer*.7+2,.75))))
        if theme not in ('tower','altar','sewer','shadow'):
            d.polygon([(-2,0),(386,0)]+list(reversed(ceiling)),fill=base)
        d.polygon(floor+[(386,224),(-2,224)],fill=base)
        if theme in ('volcano','cave','ice','abyss','core'):
            for i in range(4):
                cx=i*117+layer*23;radius=23+(i*7+layer*3)%16;cy=21+(i*17)%32
                for off in (-384,0,384):
                    x=cx+off
                    pts=[(x-radius,0),(x-radius*.8,cy+17),(x-radius*.3,cy+42),
                         (x+radius*.2,cy+57),(x+radius*.6,cy+39),(x+radius,0)]
                    d.polygon(soften(pts,2,True),fill=base)
                    curve(d,[(x-10,cy+3),(x-5,cy+25),(x+6,cy+39)],hi)
                    pen.rock((x-33,179+(i%2)*9,x+30,237),base)
                    if theme in ('ice','cave'):
                        curve(d,[(x+12,cy+2),(x+15,cy+17),(x+13,cy+30)],hi)
                    if theme=='abyss':
                        for dx in (-15,5,18):curve(d,[(x+dx,223),(x+dx+5,194),(x+dx-3,175),(x+dx+2,155)],hi,2)
        if theme in ('sewer','shadow','tower','core','heartwood','altar'):
            for i in range(4):
                cx=i*113+layer*29
                for off in (-384,0,384):
                    x=cx+off
                    if theme=='heartwood':
                        pen.bough([(x+20,224),(x+12,165),(x+23,83),(x+12,-15)],23,base)
                        pen.bough([(x+20,151),(x+57,119),(x+68,80)],7,base)
                        d.arc((x-3,43,x+41,137),80,270,fill=hi,width=2)
                    elif theme=='core':
                        curve(d,[(x+13,0),(x+13,64),(x+30,83),(x+30,224)],base,12)
                        for yy in (40,107,180):d.rounded_rectangle((x+19,yy,x+39,yy+6),radius=2,fill=hi)
                    else:
                        if theme=='altar':
                            # Open celestial terraces rather than another enclosed cave.
                            pen.old_arch((x+12,110+layer*12,x+61,224))
                            d.arc((x+5,32,x+68,95),12,164,fill=hi,width=1)
                            for sx,sy in [(10,49),(46,23),(72,81)]:
                                d.line((x+sx-1,sy,x+sx+1,sy),fill=hi);d.line((x+sx,sy-1,x+sx,sy+1),fill=hi)
                        else:
                            pen.old_arch((x+1,12+layer*9,x+74,214),theme=='shadow')
                        if theme=='tower':
                            for yy in (59,115,173):d.line((x+16,yy,x+60,yy),fill=base,width=2)
                        if theme=='sewer':
                            for xx in (x+8,x+63):curve(d,[(xx,23),(xx+3,41),(xx-2,62)],hi)
                        if theme=='altar':d.ellipse((x+17,58,x+55,96),outline=hi,width=1)
    # Broken layers on broad stone faces give depth without a sharp perimeter.
    source=image.copy()
    for i in range(150):
        x=rng.randrange(2,381);y=rng.randrange(2,222)
        if source.getpixel((x,y))[:3]==rgb(base) and source.getpixel((x+2,y))[3]:
            d.line((x,y,x+rng.randrange(2,6),y),fill=blend(base,hi,.38))
    # Colored ambient light is painted at the native grid. It gives each room
    # a cool depth hue and a warm focal point without blurring any pixel edge.
    if layer==0:
        glows={
            'volcano':[(222,182,104,72,'#ee9759',78),(45,102,94,75,'#7273b2',28)],
            'core':[(191,175,118,89,'#f3b36b',86),(60,85,95,76,'#7f5486',24)],
            'cave':[(280,155,102,88,'#8b86bb',48),(87,173,90,70,'#70b9a3',46)],
            'ice':[(86,95,118,104,'#a595c0',48),(280,174,97,78,'#9de3d4',42)],
            'heartwood':[(69,112,102,106,'#e6bc76',54),(283,145,100,88,'#679c8d',37)],
            'canopy':[(99,78,100,117,'#e0c789',45),(285,167,112,76,'#9fbca6',28)],
            'grave':[(73,56,75,72,'#b6a2cc',44),(296,169,77,73,'#d1aa7e',38)],
            'shadow':[(74,105,105,96,'#b88cac',42),(295,162,80,81,'#8989bd',40)],
            'abyss':[(293,153,89,79,'#ab91c8',40),(95,122,107,95,'#77bdae',35)],
            'sewer':[(81,153,87,79,'#c6b977',40),(293,100,91,90,'#779eaa',26)],
            'altar':[(77,88,100,103,'#e3c99d',47),(281,126,114,93,'#c2a3d8',40)],
            'tower':[(72,155,77,79,'#d9ae75',42),(285,88,105,95,'#8395b9',33)],
            'sky':[(99,48,116,95,'#f0d6a7',43)],
            'wind':[(93,79,99,87,'#eac3a0',44)],
            'snow':[(294,66,122,100,'#edd1ad',45)],
            'candy':[(90,100,106,101,'#eac2bc',36),(280,167,95,72,'#c1dec1',32)],
            'lake':[(83,83,120,100,'#e1c799',34)],
        }.get(theme,[])
        # Background layer zero is the rear layer; emit light through its alpha,
        # while the following foreground silhouettes provide natural occlusion.
        for cx,cy,rx,ry,color,alpha in glows:
            lamp=Image.new('RGBA',image.size);pixels=lamp.load();color=rgb(color)
            for yy in range(max(0,cy-ry),min(224,cy+ry)):
                for xx in range(384):
                    dx=(xx-cx+192)%384-192
                    radius=(dx/rx)**2+((yy-cy)/ry)**2
                    if radius<1:pixels[xx,yy]=color+(round(alpha*(1-radius)**2),)
            image.alpha_composite(lamp)
    return image


def refine_prop(image, theme, kind, palette):
    """Re-author organic silhouettes at their existing size and anchor."""
    old=image
    image=Image.new('RGBA',old.size)
    d=ImageDraw.Draw(image);p=list(palette)
    if theme=='grave' and kind=='dead_tree':p[:3]=['#655c63','#303746','#908177']
    if theme=='volcano' and kind=='basalt':p[:3]=['#595366','#302c40','#8a7b80']
    if theme=='ice' and kind=='snowrock':p[:3]=['#676c85','#34435e','#9698ad']
    pen=Painter(image,p,f'{theme}-{kind}-round')
    w,h=image.size;distance,material,light,mist=LOOKS[theme]
    leafcolors={
        'canopy':['#294c46','#477650','#739557','#b2bd76'],
        'heartwood':['#344c45','#5e754e','#8c9460','#c1ba83'],
        'candy':['#69a88c','#9dd5ad','#c3e4b8','#fff1c2'],
        'snow':['#405f74','#5e7f86','#8eaaa5','#e4e9df'],
        'sky':['#425f66','#64877a','#91a58b','#c4c4a0'],
        'sewer':['#334c48','#566d4b','#80915c','#a9af7a'],
    }.get(theme,[p[1],p[2],p[4],p[3]])
    if kind in ('basalt','slag','ore','snowrock','cairn','vent'):
        if kind=='cairn':
            for box in [(5,35,44,48),(10,24,38,37),(16,14,32,27),(20,6,30,17)]:pen.rock(box)
        elif kind=='vent':
            pen.rock((1,25,47,51));d.ellipse((11,23,36,32),fill=p[1]);d.ellipse((15,26,32,29),fill=p[4]);d.line((19,27,28,27),fill=p[5])
        else:
            for box in [(1,29,25,49),(17,17,43,47),(29,33,49,50)]:
                pen.rock(box,snow=kind=='snowrock',molten=kind=='slag')
            if kind=='ore':
                for x,y in [(12,32),(29,24),(23,36),(36,34)]:
                    d.ellipse((x,y,x+4,y+3),fill=p[4]);d.line((x,y,x+2,y),fill=p[5])
    elif kind in ('icecluster','sap'):
        # Facets are intentional, but widths, inclinations and heights vary.
        for x,y,ww,hh,lean in [(3,24,13,24,-3),(14,5,17,43,2),(29,19,14,29,3)]:
            pts=[(x,y+7),(x+ww//2+lean,y),(x+ww-1,y+9),(x+ww-3,y+hh-1),(x+1,y+hh-1)]
            d.polygon(soften(pts,1,True),fill=p[2],outline=p[1])
            curve(d,[(x+ww//2+lean,y+3),(x+ww//2,y+13),(x+ww//2-1,y+hh-5)],p[3],2)
            d.line((x+3,y+14,x+3,y+hh-5),fill=blend(p[2],distance,.35))
    elif kind in ('fern','moss','snowbush','mintbush','flowers','wilted','frostflower','ivy','mushrooms','coral','kelp','anemone','thorn'):
        if kind in ('moss','mintbush','snowbush'):
            pen.foliage((1,18,w-2,h-1),leafcolors)
            if kind=='snowbush':
                for box in [(4,20,20,26),(18,17,34,23),(28,25,44,30)]:d.ellipse(box,fill=p[3])
        elif kind=='mushrooms':
            for x,y,rr in [(9,27,7),(23,11,10),(38,23,8)]:
                curve(d,[(x,47),(x-2,y+8),(x,y+3)],p[2],2)
                d.ellipse((x-rr,y,x+rr,y+11),fill=p[1]);d.ellipse((x-rr+1,y,x+rr-1,y+7),fill=p[4]);curve(d,[(x-rr+3,y+3),(x,y+1),(x+rr-4,y+2)],p[3]);d.point((x-3,y+4),fill=p[5])
        else:
            for i,(x,y,lean) in enumerate([(7,18,-4),(17,6,5),(27,15,-3),(38,9,4)]):
                curve(d,[(x,47),(x+lean,34),(x-lean,22),(x+lean,y)],leafcolors[1] if kind not in ('coral','anemone') else p[2],2)
                for yy in range(y+7,40,7):
                    if kind in ('coral','thorn','anemone'):
                        for sign in (-1,1):
                            curve(d,[(x,yy+6),(x+sign*5,yy+2),(x+sign*7,yy-4)],p[4],2)
                            d.ellipse((x+sign*7-1,yy-5,x+sign*7+1,yy-3),fill=blend(p[4],mist,.25))
                    else:
                        for sign in (-1,1):
                            curve(d,[(x,yy+3),(x+sign*4,yy-1),(x+sign*7,yy)],leafcolors[2],2)
                            d.point((x+sign*7,yy),fill=leafcolors[3])
                if kind in ('flowers','frostflower','wilted'):
                    xx=x+lean
                    for dx,dy in [(-2,0),(2,1),(0,-2),(0,3)]:d.ellipse((xx+dx-1,y+dy-1,xx+dx+1,y+dy+1),fill=p[3])
                    d.point((xx,y+1),fill=light)
        pen.grain(w*h//15)
    elif kind in ('dead_tree','charred','branch','root'):
        cx=w//2
        pen.bough([(cx-8,h-1),(cx,h-15),(cx-2,h-33),(cx+4,h-49),(cx-2,6)],7)
        for pts in [[(cx,h-28),(cx-13,h-39),(cx-18,h-55),(cx-27,h-59)],
                    [(cx,h-39),(cx+13,h-51),(cx+19,h-69),(cx+27,h-73)],
                    [(cx-1,h-11),(cx+12,h-4),(w-2,h-1)]]:
            if min(y for _,y in pts)<0:pts=[(x,max(3,y)) for x,y in pts]
            pen.bough(pts,3)
        if kind in ('branch','root'):
            for box in [(0,6,23,24),(w-25,1,w-1,21),(7,22,29,35)]:pen.foliage(box,leafcolors)
        if kind=='charred':curve(d,[(cx,17),(cx+2,23),(cx,29)],p[4])
        pen.grain(65)
    elif kind=='fir':
        pen.bough([(32,95),(30,63),(32,26),(30,9)],5)
        for i,(yy,ww) in enumerate([(8,24),(25,39),(44,53),(65,61)]):
            box=(32-ww//2,yy,32+ww//2,yy+27)
            pen.foliage(box,['#334d62','#4b6c76','#74958d','#b6c5ba'])
            cap=[(32-ww*.43,yy+12),(32-ww*.22,yy+4),(31,yy+1),(32+ww*.30,yy+7),
                 (32+ww*.44,yy+13),(32+ww*.20,yy+15),(32,yy+12),(32-ww*.15,yy+17)]
            d.polygon(soften(cap,2,True),fill=p[3])
            curve(d,[(32-ww*.21,yy+8),(31,yy+5),(32+ww*.17,yy+9)],p[5])
    elif kind in ('arch','frozenarch','gothicarch'):
        pen.old_arch((8,4,w-9,h-1),kind=='gothicarch')
        if kind=='frozenarch':
            for x,hh in [(17,15),(29,10),(49,17),(61,12)]:
                curve(d,[(x,22),(x+2,28),(x+1,22+hh)],p[4],3);d.point((x+1,22+hh),fill=p[3])
        elif kind=='arch':
            for x,y in [(11,41),(15,51),(64,27),(66,37),(65,64)]:
                d.ellipse((x,y,x+4,y+2),fill=leafcolors[1]);d.point((x+1,y),fill=leafcolors[2])
    elif kind in ('treehouse','hearttree'):
        if kind=='treehouse':
            pen.bough([(62,111),(58,77),(65,45),(57,4)],12)
            for box in [(1,8,43,45),(23,0,70,36),(49,13,95,51)]:pen.foliage(box,leafcolors)
            d.rounded_rectangle((18,61,72,94),radius=3,fill='#715940')
            for y in (67,75,84):d.line((20,y,70,y),fill='#554b39')
            roof=soften([(11,63),(22,49),(43,38),(59,48),(79,63)],1)
            d.polygon(roof,fill='#355945');curve(d,roof[:-1], '#8ea461',2)
            for y in (51,56,61):d.line((28-((y-51)//2),y,59+(y-51),y),fill='#587649')
            d.rounded_rectangle((48,72,61,94),radius=4,fill='#35443c');d.rounded_rectangle((26,70,39,82),radius=2,fill='#d8bd80');d.line((32,71,32,81),fill='#746148')
            d.rounded_rectangle((12,94,80,98),radius=2,fill='#93774e')
            for x in (21,69):curve(d,[(x,99),(x+1,105),(x-2,111)],'#65523b',2)
        else:
            pts=[(2,127),(19,105),(23,74),(18,40),(29,-5),(70,-5),(79,40),(73,78),(80,111),(95,127)]
            d.polygon(soften(pts,2,True),fill=p[0],outline=p[1])
            for xx in (29,37,67,74):curve(d,[(xx,3),(xx-5,37),(xx,72),(xx-4,105)],p[2],2)
            for xx in (2,17,73,92):pen.bough([(49,103),(xx+3,117),(xx,127)],6)
            d.ellipse((29,26,69,107),fill=p[1]);d.ellipse((35,36,64,94),fill='#987a50');d.ellipse((39,43,60,88),fill='#d2b979');d.ellipse((43,50,55,82),fill='#e5cf99')
            for box in [(0,-3,43,22),(30,-9,74,19),(62,0,95,27)]:pen.foliage(box,leafcolors)
        pen.grain(130)
    elif kind=='icefall':
        d.polygon(soften([(5,0),(58,0),(54,31),(59,61),(54,98),(45,112),(12,109),(3,84),(8,53),(5,24)],2,True),fill=blend(p[2],distance,.35))
        for i,x in enumerate((10,18,28,39,49)):
            curve(d,[(x,0),(x-3,29),(x+2,58),(x-2,83),(x+1,106)],p[2],5)
            curve(d,[(x-1,0),(x-4,29),(x+1,58),(x-3,83),(x,100)],p[3],1)
        for box in [(1,92,26,115),(20,94,45,114),(39,88,63,114)]:pen.rock(box,snow=True)
    elif kind=='tent':
        pts=[(2,46),(10,32),(17,13),(24,6),(31,15),(39,34),(46,46)]
        d.polygon(soften(pts,1),fill=blend(p[2],material,.35),outline=p[1]);curve(d,[(24,8),(25,23),(32,45)],p[3],2)
        d.polygon(soften([(24,11),(28,32),(33,46),(13,46),(18,29)],1,True),fill=p[1]);curve(d,[(5,46),(15,32),(23,12)],p[3])
    else:
        # Existing masonry / machines keep their construction, softened by age,
        # warm reflected light and cool recesses instead of a monochrome outline.
        image=old;d=ImageDraw.Draw(image);pen=Painter(image,p,theme+kind)
        for y in range(h):
            for x in range(w):
                c=image.getpixel((x,y))
                if c[3]!=255:continue
                if c[:3]==rgb(p[2]):d.point((x,y),fill=blend(p[2],light,.24))
                elif c[:3]==rgb(p[1]):d.point((x,y),fill=blend(p[1],distance,.22))
                elif c[:3]==rgb(p[0]):d.point((x,y),fill=blend(p[0],material,.15))
                elif kind=='lantern' and c[:3]==rgb(p[4]):d.point((x,y),fill=light)
                elif kind=='lantern' and c[:3]==rgb(p[5]):d.point((x,y),fill='#f0d6aa')
        if kind in ('column','obelisk','sluice','mausoleum','furnace','gemstand','rune','totem'):
            pen.grain(w*h//12)
            for i in range(5):
                x=pen.rng.randrange(4,w-4);y=pen.rng.randrange(h//2,h-2)
                c=image.getpixel((x,y))
                if c[3]==255:curve(d,[(x,y),(x+1,y+2),(x-1,y+4)],blend(c,p[1],.35))
    return image


def terrain(theme,p,kind,variant):
    """Paint softly clustered 16px materials; preserve an opaque playable surface."""
    rng=random.Random(f'{theme}-soil-{variant}');cool,material,light,mist=LOOKS[theme]
    base=blend(p[0],material,.13);shade=blend(p[0],p[1],.35);bright=blend(p[0],p[2],.47)
    if kind=='cake':base=rgb(p[0]);shade=blend(p[0],p[1],.22);bright=blend(p[0],p[2],.44)
    image=Image.new('RGBA',(16,16),base);d=ImageDraw.Draw(image)
    if kind in ('brick','marble','rune'):
        # Mortar is broken and recessed rather than a heavy grid on every tile.
        for yy in (0,8):
            for start,end in [(0,5+variant),(9+variant//2,15)]:d.line((start,yy,end,yy),fill=shade)
            d.line((2,yy+1,7,yy+1),fill=bright)
            xx=(variant*4+(8 if yy else 0))%16;d.line((xx,yy+2,xx,yy+6),fill=shade)
        if kind=='marble':curve(d,[(0,12),(5,11),(8,13),(15,10)],blend(base,cool,.13))
        if kind=='rune' and variant==2:curve(d,[(7,3),(10,5),(7,6)],blend(base,p[4],.4))
    elif kind in ('root','wood'):
        for y in (-3+variant,4+variant,11+variant):
            curve(d,[(-1,y),(4,y+1),(9,y-1),(17,y+1)],shade)
            curve(d,[(1,y+2),(7,y+3),(13,y+1)],bright)
        if variant==1:d.ellipse((5,6,12,11),outline=shade);d.line((7,9,9,9),fill=shade)
    elif kind=='ice':
        d.polygon([(0,0),(15,0),(15,8),(7,12),(0,10)],fill=blend(base,p[2],.37))
        curve(d,[(0,6+variant),(5,4+variant),(10,5+variant),(15,2+variant)],blend(base,p[3],.43))
        if variant%2:curve(d,[(13,5),(10,10),(11,15)],blend(base,cool,.28))
        d.line((4+variant,2,7+variant,2),fill=blend(base,p[5],.45))
    elif kind in ('basalt','obsidian'):
        for box in [(-5,-2,9,8),(7,-5,22,9),(-2,8,9,20),(8,7,20,20)]:
            x,y,x1,y1=box;offset=variant%3-1
            d.rounded_rectangle((x+offset,y,x1+offset,y1),radius=4,fill=rng.choice([base,shade,bright]))
        # Only the core carries a faint warm mineral vein, not orange frames.
        if kind=='obsidian' and variant==1:curve(d,[(2,4),(4,7),(3,11)],blend(base,p[4],.28))
    else:
        for i in range(16):
            x=rng.randrange(-2,16);y=rng.randrange(-1,16)
            d.rounded_rectangle((x,y,x+rng.randrange(2,5),y+2),radius=1,fill=rng.choice([shade,bright,base]))
        if kind=='cake':
            for y in (6,13):curve(d,[(0,y),(5,y+1),(11,y-1),(15,y)],blend(base,p[2],.4))
    # Small warm flecks and cool recesses keep a material from becoming one flat hue.
    for i in range(8):
        x=rng.randrange(16);y=rng.randrange(16)
        d.line((x,y,min(15,x+1),y),fill=rng.choice([bright,shade,blend(base,light,.18),blend(base,cool,.17)]))
    fill=image.copy()
    if kind in ('root','soil','reef'):
        cap=blend(p[4] if kind=='root' else p[2],material,.27)
    elif kind in ('snow','ice','cake'):cap=blend(p[3],mist,.18)
    else:cap=blend(p[2],material,.2)
    for x in range(16):
        depth=2+rng.randrange(3)
        if kind=='cake':depth=3+round(math.sin((x+variant*3)*math.tau/16))
        d.line((x,0,x,depth),fill=blend(cap,shade,.24))
        d.line((x,0,x,depth-1),fill=cap)
        if x%4!=variant%4:d.point((x,0),fill=blend(cap,light,.20))
    top=image.copy()
    wall=Image.new('RGBA',(16,16),blend(base,p[1],.56));wd=ImageDraw.Draw(wall)
    for y in (0,8):
        wd.line((0,y,7,y),fill=blend(base,p[1],.38));x=(variant*3+y)%16;wd.line((x,y+2,x,y+6),fill=blend(base,p[1],.38))
    return fill,top,wall


def groundcover(theme,p,variant):
    image=Image.new('RGBA',(16,16));d=ImageDraw.Draw(image);rng=random.Random(theme+str(variant))
    cool,material,light,mist=LOOKS[theme]
    if theme in ('volcano','core','ice','snow','sky','wind','altar'):
        pen=Painter(image,[blend(p[0],material,.2),p[1],p[2],p[3],p[4],p[5]],theme+str(variant))
        pen.rock((0,10,10,17),snow=theme in ('ice','snow'));pen.rock((9,12,16,17))
        if variant==2:d.ellipse((4,7,8,11),fill=blend(p[2],material,.3))
    else:
        green=blend(material,'#66875d',.4) if theme!='candy' else '#a1d0ac'
        for i in range(4):
            x=2+i*4;y=8-rng.randrange(5)
            curve(d,[(x,15),(x-1,11),(x-3,y)],green)
            d.line((x-3,y,x-1,y+1),fill=blend(green,light,.35))
            if variant==1:d.ellipse((x-4,y-1,x-1,y+1),fill=blend(p[3],light,.3))
            if theme=='candy' and variant==1:
                d.point((x-3,y-2),fill='#f0b2c8');d.point((x-1,y),fill='#f0b2c8');d.point((x-2,y),fill='#fff0c7')
        if variant==2:
            d.ellipse((3,12,10,16),fill=p[2]);d.line((4,12,7,12),fill=p[3])
    return image
