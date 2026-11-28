import sys, subprocess, os, json
sys.path.insert(0,'/home/claude/work')
from cap import layer
from PIL import Image, ImageDraw, ImageFont, ImageFilter
os.chdir('/home/claude/work/ne')
OUT=sys.argv[1] if len(sys.argv)>1 else 'REEL6_PROPOSITO_v2.mp4'
XF=0.5
END_START=106.4; END_LEN=4.6; TOTAL=END_START+END_LEN
SEG=[('P01',0.0,0.0,5.8),('P02',0.0,5.8,11.4),('P03',0.0,11.4,15.6),('P04',0.0,15.6,26.9),
     ('P05',0.0,26.9,38.2),('P06',0.0,38.2,49.6),('P07',0.0,49.6,60.0),('P08',0.0,60.0,63.6),
     ('P09',0.0,63.6,76.3),('P10',0.0,76.3,88.2),('P11',0.0,88.2,99.7),('P12',0.0,99.7,TOTAL)]
N2='NEEMIAS 6:2'; N3='NEEMIAS 6:3'; N4='NEEMIAS 6:4'; N9='NEEMIAS 6:9'; N15='NEEMIAS 6:15'; MT='MATEUS 27:40'
CAP=[(0.0,'Quem tem um *propósito*',None),(1.2,'sabe dizer *não*',None),(2.38,'e sabe exatamente para onde está indo.',None),
 (5.88,'Neemias sabia.',None),(6.6,'Porque estava em Jerusalém.',None),
 (8.78,'Deus tinha colocado no coração dele',None),(10.14,'uma *missão*:',None),(11.42,'reconstruir os muros da cidade,',None),(13.66,'que estavam em ruínas.',None),
 (15.76,'No meio da obra, chegou um convite:',None),(18.62,'“Venha, vamos nos encontrar',N2),(20.4,'na planície de Ono.”',N2),
 (22.6,'Parecia até diplomacia.',None),(24.08,'Mas era uma *armadilha.*',None),(26.94,'“Eles estavam tramando fazer-me mal.”',N2),
 (30.2,'Neemias não pensou duas vezes:',None),(32.3,'“Estou fazendo uma *grande obra*,',N3),(34.3,'de modo que não poderei descer.',N3),(36.2,'Por que cessaria essa obra?”',N3),
 (38.36,'Mandaram a mesma mensagem,',N4),(39.66,'não uma, mas *quatro vezes.*',N4),(41.72,'Quatro vezes',None),(42.68,'ele deu a mesma resposta.',None),
 (45.38,'Quem sabe para onde está indo',None),(47.4,'*não negocia a direção.*',None),
 (49.76,'Depois vieram as ameaças,',None),(51.58,'os boatos, a intimidação.',None),
 (54.84,'E ele orou:',None),(55.94,'“Senhor, *fortalece* agora as minhas mãos.”',N9),
 (60.22,'E o muro ficou pronto',N15),(61.54,'em *52 dias.*',N15),
 (63.78,'Jesus também sabia',None),(64.9,'para onde estava indo.',None),
 (67.74,'Gritaram: “Desce da cruz!”',MT),(69.92,'*Ele não desceu.*',None),
 (71.88,'O propósito dele era muito claro:',None),(74.38,'a *sua salvação.*',None),
 (76.46,'Hoje, os convites para sair da rota',None),(78.34,'chegam de outras formas:',None),(79.72,'a distração,',None),(81.78,'a polêmica que não é sua,',None),
 (83.8,'a intimidação, o medo,',None),(85.38,'a briga que não te pertence.',None),
 (88.34,'Mas você não está aqui *por acaso.*',None),(90.56,'Deus te deu uma obra.',None),(91.98,'Deus estabeleceu um *propósito*',None),(93.64,'na sua vida:',None),
 (95.36,'a sua família, o seu chamado,',None),(97.22,'o que Ele colocou nas suas mãos.',None),
 (99.84,'Em Cristo, eu tenho um propósito.',None),(102.22,'Eu sei para onde estou indo.',None),(104.54,'*O meu futuro está garantido!*',None)]
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
afc=(f"[0:a]aresample=48000,pan=mono|c0=c0,highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad=whole_dur={TOTAL}[vo];"
     f"[vo]asplit=2[vo1][vo2];"
     f"[1:a]aresample=48000,atrim=start=24.99,asetpts=PTS-STARTPTS,volume=0.30,afade=t=in:st=0:d=1.0,atrim=duration={TOTAL},afade=t=out:st={TOTAL-2.5:.2f}:d=2.5[tr];"
     f"[tr][vo2]sidechaincompress=threshold=0.04:ratio=4:attack=20:release=400[trd];"
     f"[vo1][trd]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(['ffmpeg','-v','error','-y','-i','voz.m4a','-i',TR,'-filter_complex',afc,'-map','[a]','-t',f'{TOTAL}','-ac','2','-ar','48000','-f','s16le','mix.raw'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i','video_nosound.mp4','-f','s16le','-ar','48000','-ac','2','-i','mix.raw','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-shortest',OUT],check=True)
print('done',dur(OUT))
