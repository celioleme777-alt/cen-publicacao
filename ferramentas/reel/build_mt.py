import sys, subprocess, os, json
sys.path.insert(0,'/home/claude/work')
from cap import layer
from PIL import Image, ImageDraw, ImageFont, ImageFilter
os.chdir('/home/claude/work/mt')
OUT=sys.argv[1] if len(sys.argv)>1 else 'REEL13_MEUS_TEMPOS_v1.mp4'
XF=0.5
END_START=87.3; END_LEN=4.6; TOTAL=END_START+END_LEN
# (clip, offset in clip, start, end)
SEG=[('T01',0.0,0.0,4.2),('T02',0.0,4.2,13.1),('T03',0.0,13.1,18.4),('T04',0.0,18.4,25.0),
     ('T05',0.0,25.0,34.9),('T06',0.0,34.9,41.9),('T07',0.0,41.9,45.8),('T08e',0.0,45.8,56.6),
     ('T09',0.0,56.6,63.8),('T10',0.0,63.8,71.6),('T12',0.0,71.6,78.0),('T13',1.5,78.0,82.2),
     ('T11',0.0,82.2,TOTAL)]
SL='SALMOS 31:15'; GN='GÊNESIS 50:20'
CAP=[(0.86,'O relógio da sua vida',None),(2.30,'não está na mão de ninguém.',None),
 (4.32,'Ele está nas mãos *de Deus.*',None),(6.90,'Davi orou em Salmos 31:15:',None),
 (9.40,'“Os meus tempos estão *nas tuas mãos.*”',SL),
 (13.26,'José tinha 17 anos',None),(14.46,'quando os irmãos o jogaram no poço',None),(16.32,'e o venderam como escravo.',None),
 (18.58,'Depois veio a casa de Potifar,',None),(20.68,'a acusação falsa,',None),(22.24,'a prisão.',None),
 (24.06,'*Treze anos.*',None),(25.12,'E durante todo esse tempo,',None),(27.32,'parecia que o relógio tinha parado.',None),
 (30.06,'Mas Deus não esqueceu José na prisão.',None),(32.62,'Ele estava preparando *o palácio.*',None),
 (34.96,'No dia certo,',None),(36.34,'Faraó mandou buscá-lo às pressas.',None),(38.72,'Num só dia,',None),
 (40.10,'José saiu da prisão',None),(41.98,'e foi colocado como *governador do Egito.*',None),
 (45.94,'E José entendeu o que poucos entendem.',None),(48.64,'Olhou para os irmãos e disse,',None),
 (50.14,'em Gênesis 50:20:',None),(51.76,'“Vocês planejaram o mal contra mim,',GN),(54.44,'mas Deus o tornou *em bem.*”',GN),
 (56.80,'Talvez você esteja no seu *tempo de espera.*',None),(59.96,'A promessa demorou,',None),(60.98,'a porta não abriu,',None),
 (61.92,'a resposta não chegou.',None),(63.86,'Mas não confunda',None),(65.40,'*demora* com esquecimento.',None),
 (67.34,'Quem segura o seu tempo',None),(68.66,'é o mesmo que *segura o universo.*',None),
 (71.74,'Em Cristo, a minha vida',None),(73.30,'não está à mercê das pessoas,',None),(75.10,'nem das circunstâncias,',None),
 (76.76,'nem da sorte.',None),(78.04,'Ele está nas mãos de um Pai',None),(79.72,'que *nunca se atrasa.*',None),
 (82.22,'Em Cristo, os meus tempos',None),(84.28,'estão *nas mãos do Senhor!*',None)]
W=json.load(open('words.json'))
def last_word_end(t0,t1):
    e=[b for a,b,_ in W if a>=t0-0.05 and a<t1]
    return max(e) if e else t1
# caption track: list of (img, dur)
os.makedirs('cap',exist_ok=True)
track=[]; t=0.0
def add(img,dur,name):
    p=f'cap/{name}.png'; img.save(p); track.append((p,dur))
add(layer(None,None,True),CAP[0][0],'c000')
for i,(s,txt,ref) in enumerate(CAP):
    nxt=CAP[i+1][0] if i+1<len(CAP) else END_START
    end=min(nxt,last_word_end(s,nxt)+0.6) if i+1<len(CAP) else END_START
    add(layer(txt,ref,True),end-s,f'c{i+1:03d}')
    if end<nxt-0.01: add(layer(None,None,True),nxt-end,f'g{i+1:03d}')
with open('cap/list.txt','w') as f:
    for p,d in track: f.write(f"file '{os.path.abspath(p)}'\nduration {d:.3f}\n")
    f.write(f"file '{os.path.abspath(track[-1][0])}'\n")
# end card
def font(p,s,w):
    ft=ImageFont.truetype(p,s); ft.set_variation_by_axes([w]); return ft
CZ=font('/home/claude/work/fonts/Cinzel[wght].ttf',96,700)
MR=font('/home/claude/work/fonts/Montserrat[wght].ttf',36,500)
MB=font('/home/claude/work/fonts/Montserrat[wght].ttf',44,700)
ec=Image.new('RGBA',(1080,1920),(0,0,0,140)); txt=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(txt)
def ct(y,s,f,col,tr=0):
    w=sum(f.getlength(c) for c in s)+tr*(len(s)-1); x=(1080-w)/2
    for c in s: d.text((x,y),c,font=f,fill=col); x+=f.getlength(c)+tr
ct(700,'CRISTO',CZ,(255,255,255,255),6); ct(815,'EM NÓS',CZ,(255,255,255,255),6)
ct(1000,'Uma verdade por dia sobre',MR,(235,235,235,255)); ct(1055,'quem você é em Cristo',MR,(235,235,235,255))
ct(1190,'@cristoemnoscelioleme',MB,(232,196,106,255))
a=txt.split()[3]; sh=Image.new('RGBA',(1080,1920),(0,0,0,0)); sh.putalpha(a.point(lambda v:int(v*0.7))); sh=sh.filter(ImageFilter.GaussianBlur(6))
ec.alpha_composite(sh,(0,3)); ec.alpha_composite(txt); ec.save('endcard.png')
# video segments
os.makedirs('seg',exist_ok=True)
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
segfiles=[]
for k,(c,off,s,e) in enumerate(SEG):
    pre=XF/2 if k>0 else 0; post=XF/2 if k<len(SEG)-1 else 0
    L=(e-s)+pre+post; src=f'clips/{c}.mp4'; avail=dur(src)-off-0.05
    fac=max(1.0,L/avail)
    out=f'seg/s{k:02d}.mp4'
    vf=f"trim=start={off}:duration={min(avail,L/fac):.3f},setpts=(PTS-STARTPTS)*{fac:.4f},fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={L:.3f},setpts=PTS-STARTPTS"
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p',out],check=True)
    segfiles.append((out,L,s,fac))
    print(c,round(L,2),'fac',round(fac,3))
# xfade chain
inputs=[]; fc=[]; prev='[0:v]'
for i,(p,L,s,f) in enumerate(segfiles): inputs+=['-i',p]
for i in range(1,len(segfiles)):
    off=SEG[i][2]-XF/2
    lab=f'[x{i}]'; fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}{lab}"); prev=lab
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',';'.join(fc),'-map',prev,'-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p','bg.mp4'],check=True)
print('bg',dur('bg.mp4'))
# captions + endcard overlay + final fade
fc=(f"[1:v]format=rgba,setpts=PTS-STARTPTS[cap];[0:v][cap]overlay=0:0:eof_action=pass:enable='lt(t,{END_START})'[v1];"
    f"[2:v]format=rgba,fade=t=in:st={END_START}:d=0.7:alpha=1[ec];[v1][ec]overlay=0:0:enable='gte(t,{END_START})'[v2];"
    f"[v2]fade=t=out:st={TOTAL-1.3:.2f}:d=1.3[v]")
subprocess.run(['ffmpeg','-v','error','-y','-i','bg.mp4','-f','concat','-safe','0','-i','cap/list.txt','-loop','1','-t',f'{TOTAL}','-i','endcard.png',
  '-filter_complex',fc,'-map','[v]','-t',f'{TOTAL}','-r','30','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','video_nosound.mp4'],check=True)
# audio
TR='/mnt/user-data/outputs/reel1/TRILHA_REINO_PODER.mp3'
afc=(f"[0:a]aresample=48000,pan=mono|c0=c0,highpass=f=70,volume=enable='lt(t,0.80)':volume=0,afade=t=in:st=0.80:d=0.08,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad=whole_dur={TOTAL}[vo];"
     f"[vo]asplit=2[vo1][vo2];"
     f"[1:a]aresample=48000,atrim=start=24.99,asetpts=PTS-STARTPTS,volume=0.30,afade=t=in:st=0:d=1.0,atrim=duration={TOTAL},afade=t=out:st={TOTAL-2.5:.2f}:d=2.5[tr];"
     f"[tr][vo2]sidechaincompress=threshold=0.04:ratio=4:attack=20:release=400[trd];"
     f"[vo1][trd]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(['ffmpeg','-v','error','-y','-i','voz.m4a','-i',TR,'-filter_complex',afc,'-map','[a]','-t',f'{TOTAL}','-ac','2','-ar','48000','-f','s16le','mix.raw'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i','video_nosound.mp4','-f','s16le','-ar','48000','-ac','2','-i','mix.raw','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-shortest',OUT],check=True)
print('done',dur(OUT))
