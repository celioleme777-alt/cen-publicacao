import subprocess,sys,os
sys.path.insert(0,'/home/claude/work'); from cap import layer
C='/home/claude/work/clips/'
b=[0.0,4.75,12.23,18.55,24.91,32.81,42.45,45.91,53.03,56.33,62.45]
def seg(k,f,src,out):
    ln=b[k+1]-b[k]+0.6; fac=max(1.0,ln/src)
    vf=f"setpts=PTS*{fac:.4f},fps=30,scale=1080:1920:flags=lanczos,format=yuv420p"
    subprocess.run(['ffmpeg','-v','error','-y','-i',C+f,'-an','-vf',vf,'-t',f'{ln:.3f}','-c:v','libx264','-preset','veryfast','-crf','16',out],check=True)
    return b[k]-0.3, ln
def build(name,segs,t0,t1,caps):
    os.makedirs(name,exist_ok=True)
    starts=[]
    for i,(k,f,src) in enumerate(segs):
        st,ln=seg(k,f,src,f'{name}/s{i}.mp4'); starts.append((st,ln))
    T0=starts[0][0]
    fc=[];last='[0:v]'
    for i in range(1,len(segs)):
        off=starts[i][0]-T0; o=f'[x{i}]'; fc.append(f'{last}[{i}:v]xfade=transition=fade:duration=0.6:offset={off:.3f}{o}'); last=o
    # caption track
    lines=['ffconcat version 1.0']; prev=t0
    for j,(a,bb,txt,ref) in enumerate(caps):
        p=f'{name}/c{j}.png'; layer(txt,ref).save(p); lines+= [f"file '{os.path.basename(p)}'",f"duration {bb-a:.3f}"]
    lines.append(f"file '{os.path.basename(p)}'"); open(f'{name}/track.txt','w').write('\n'.join(lines)+'\n')
    n=len(segs)
    fc.append(f"{last}trim=start={t0-T0:.3f}:duration={t1-t0:.3f},setpts=PTS-STARTPTS[bg]")
    fc.append(f"[{n}:v]fps=30,format=rgba[tk]")
    fc.append("[bg][tk]overlay=0:0:shortest=0:eof_action=pass,format=yuv420p[v]")
    inp=[]
    for i in range(n): inp+=['-i',f'{name}/s{i}.mp4']
    inp+=['-f','concat','-safe','0','-i',f'{name}/track.txt']
    subprocess.run(['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(fc),'-map','[v]','-t',f'{t1-t0:.3f}','-c:v','libx264','-preset','veryfast','-crf','16','-r','30',f'{name}/out.mp4'],check=True)
    print(name,'ok')
R='APOCALIPSE 3:8'
build('rA',[(1,'B02_DRONE.mp4',10.0),(2,'B03b.mp4',10.0),(3,'B04b.mp4',10.0),(4,'B05_PORTA_LOFT.mp4',10.0)],12.0,25.4,
 [(12.0,12.40,None,R),(12.40,14.53,'Sei que você tem pouca força,',R),(14.53,16.13,'mas guardou a minha palavra',R),(16.13,18.23,'e não negou o meu nome.”',R),(18.23,18.73,None,None),(18.73,20.73,'Repare: a igreja de Filadélfia',None),(20.73,23.03,'não era grande, nem rica,',None),(23.03,25.07,'nem muito menos influente.',None),(25.07,25.4,'Ela era uma igreja de pouca força,',None)])
build('rB',[(7,'B08a.mp4',6.0),(8,'A07b.mp4',10.0),(9,'B01b.mp4',6.0)],52.6,56.8,
 [(52.6,53.20,'e não negue o nome Dele.',None),(53.20,55.27,'A chave não está na sua força,',None),(55.27,56.47,'está na *mão Dele*.',None),(56.47,56.8,'O que Ele abre, ninguém fecha.',None)])
