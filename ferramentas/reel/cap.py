from PIL import Image, ImageDraw, ImageFont, ImageFilter
M='/home/claude/work/fonts/Montserrat[wght].ttf'; C='/home/claude/work/fonts/Cinzel[wght].ttf'
def font(p,s,w):
    f=ImageFont.truetype(p,s); f.set_variation_by_axes([w]); return f
FM=font(M,73,800); FH=font(C,44,600); FR=font(C,40,600)
GOLD=(232,196,106); WHITE=(255,255,255)
def parse(txt):
    plain='';mask=[];gold=False
    for ch in txt:
        if ch=='*': gold=not gold; continue
        plain+=ch; mask.append(gold)
    out=[];i=0
    for w in plain.split(' '):
        if w: out.append((w,mask[i:i+len(w)]))
        i+=len(w)+1
    return out
def wrap(words,maxw=860):
    lines=[[]]
    for w in words:
        test=' '.join(x for x,_ in lines[-1]+[w])
        if lines[-1] and FM.getlength(test)>maxw: lines.append([w])
        else: lines[-1].append(w)
    return lines
def tracked(d,xy,s,f,fill,tr):
    x,y=xy
    for ch in s:
        d.text((x,y),ch,font=f,fill=fill); x+=f.getlength(ch)+tr
def tw(s,f,tr): return sum(f.getlength(c) for c in s)+tr*(len(s)-1)
def layer(caption=None, ref=None, header=True):
    txt=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(txt)
    if header:
        s='CRISTO EM NÓS'; tr=44*0.14; w=tw(s,FH,tr); tracked(d,((1080-w)/2,168),s,FH,(255,255,255,235),tr)
    if caption:
        lines=wrap(parse(caption)); pitch=91; n=len(lines)
        top=1164 if n==2 else (1164+45 if n==1 else 1164-45)
        for i,ln in enumerate(lines):
            words=ln; full=' '.join(w for w,_ in words); x=(1080-FM.getlength(full))/2; y=top+i*pitch
            for j,(w,g) in enumerate(words):
                k=0
                while k<len(w):
                    m=k
                    while m<len(w) and g[m]==g[k]: m+=1
                    run=w[k:m]; d.text((x,y),run,font=FM,fill=GOLD+(255,) if g[k] else WHITE+(255,)); x+=FM.getlength(run); k=m
                if j<len(words)-1: x+=FM.getlength(' ')
    if ref:
        tr=40*0.14; w=tw(ref,FR,tr); tracked(d,((1080-w)/2,1411),ref,FR,GOLD+(255,),tr)
    a=txt.split()[3]
    sh=Image.new('RGBA',(1080,1920),(0,0,0,0)); sh.putalpha(a.point(lambda v:int(v*0.75)))
    sh=Image.composite(Image.new('RGBA',(1080,1920),(0,0,0,255)),Image.new('RGBA',(1080,1920),(0,0,0,0)),a.point(lambda v:int(v*0.8)))
    sh=sh.filter(ImageFilter.GaussianBlur(6))
    base=Image.new('RGBA',(1080,1920),(0,0,0,0)); base.alpha_composite(sh,(0,3)); base.alpha_composite(txt)
    return base
