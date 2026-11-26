import sys, subprocess, os, json
sys.path.insert(0,'/home/claude/work')
from cap import layer
from PIL import Image, ImageDraw, ImageFont, ImageFilter
os.chdir('/home/claude/work/rs')
OUT=sys.argv[1] if len(sys.argv)>1 else 'REEL14_RESISTO_AO_DIABO_v1.mp4'
XF=0.5
END_START=123.9; END_LEN=4.6; TOTAL=END_START+END_LEN
SEG=[('R01',0.0,0.0,7.0),('R02b',0.0,7.0,14.2),('R03',0.0,14.2,22.0),('R04b',0.0,22.0,32.5),
     ('R05',0.0,32.5,39.4),('R06',0.0,39.4,46.5),('R07',0.0,46.5,58.1),('R08',0.0,58.1,70.0),
     ('R09',0.0,70.0,81.3),('R13',0.0,81.3,89.2),('R11',0.0,89.2,101.5),('R14',0.0,101.5,114.4),
     ('R12',0.0,114.4,TOTAL)]
TG='TIAGO 4:7'; AP='APOCALIPSE 12:11'; JO='1 JOÃO 4:4'
CAP=[(0.0,'O diabo não foge de você.',None),(3.34,'Ele foge do que está *sobre*',None),(5.0,'e *dentro* de você.',None),
 (7.0,'Está escrito em Tiago 4:7:',None),(9.40,'“Submetam-se a Deus.',TG),(11.02,'Resistam ao diabo,',TG),(12.04,'e ele *fugirá de vocês.*”',TG),
 (14.2,'Repare que existe *uma ordem* aqui.',None),(15.76,'Primeiro, você tem que',None),(17.18,'se *submeter* a Deus.',None),(18.84,'Só então você poderá',None),(20.76,'*resistir* ao diabo.',None),
 (22.08,'Quem anda debaixo do governo de Deus',None),(24.12,'anda *coberto.*',None),(25.46,'E é essa cobertura',None),(27.16,'que o inferno reconhece:',None),(28.86,'o *sangue de Jesus*',None),(30.24,'e a *unção do Espírito Santo.*',None),
 (32.52,'Jesus veio para ser exemplo.',None),(34.82,'Ele saiu do Jordão',None),(35.82,'*cheio do Espírito Santo*',None),(37.16,'e foi para o deserto.',None),
 (38.62,'Quarenta dias com fome,',None),(40.64,'sem pão, sem água,',None),(42.5,'*sozinho.*',None),
 (43.06,'E no final desses quarenta dias,',None),(45.34,'o diabo veio com três propostas:',None),(48.72,'pão,',None),(49.62,'espetáculo',None),(50.62,'e *poder.*',None),
 (52.86,'Três atalhos para tirar Jesus',None),(55.3,'do plano perfeito de Deus.',None),
 (58.18,'Jesus não discutiu.',None),(59.82,'Não negociou.',None),(61.2,'Respondeu três vezes:',None),(62.28,'“*Está escrito*, Satanás.”',None),
 (64.34,'E na última, ordenou:',None),(66.42,'“*Retire-se* daqui, Satanás!”',None),(68.28,'E o diabo o deixou.',None),
 (70.02,'O inimigo não tem medo do seu tamanho,',None),(72.44,'da sua formação acadêmica,',None),(74.34,'da sua conta bancária',None),(75.36,'ou da sua posição social.',None),
 (77.4,'Ele tem medo do *sangue*',None),(79.14,'e da *unção* que estão sobre a sua vida.',None),
 (81.32,'Está escrito em Apocalipse 12:11:',None),(83.76,'“Eles o venceram',AP),(85.02,'pelo *sangue do Cordeiro*',AP),(86.56,'e pela palavra do testemunho.”',AP),
 (89.28,'O deserto também pode chegar.',None),(91.02,'Mas, se ele chegar,',None),(91.9,'você não entra nele *sozinho.*',None),
 (94.2,'Está escrito em 1 João 4:4:',None),(97.38,'“Aquele que está em vocês',JO),(98.64,'é *maior* do que aquele',JO),(99.94,'que está no mundo.”',JO),
 (101.58,'O mesmo Espírito que estava',None),(103.26,'sobre Jesus no deserto',None),(105.2,'está *sobre você.*',None),
 (106.84,'Em Cristo, você carrega',None),(108.74,'a mesma *Palavra* que Ele usou',None),(110.64,'e a mesma *autoridade*',None),(112.56,'que estava sobre Ele.',None),
 (114.44,'Então não fuja do diabo.',None),(116.98,'Faça o diabo *fugir de você.*',None),
 (119.52,'Em Cristo, eu resisto ao diabo',None),(121.92,'e ele *foge de mim!*',None)]
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
