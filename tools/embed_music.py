"""Convert standard MIDI notes/tempo into a self-contained browser score bank."""
from pathlib import Path
import base64,bisect,json,struct

ROOT=Path(__file__).resolve().parents[1]

def decode(raw,exact=False):
 assert raw[:4]==b'MThd'
 hlen=int.from_bytes(raw[4:8],'big');fmt,ntracks,division=struct.unpack('>HHH',raw[8:14]);assert fmt in (0,1) and division<32768
 pos=8+hlen;events=[];tempos=[(0,500000)];markers=[];last=0
 for track in range(ntracks):
  assert raw[pos:pos+4]==b'MTrk';length=int.from_bytes(raw[pos+4:pos+8],'big');data=raw[pos+8:pos+8+length];pos+=8+length
  i=tick=0;running=None
  def vlq():
   nonlocal i
   v=0
   while True:
    b=data[i];i+=1;v=v*128+(b&127)
    if b<128:return v
  while i<len(data):
   tick+=vlq();last=max(last,tick);status=data[i]
   if status>=128:i+=1
   else:assert running is not None;status=running
   if status==255:
    kind=data[i];i+=1;n=vlq();payload=data[i:i+n];i+=n
    if kind==81:tempos.append((tick,int.from_bytes(payload,'big')))
    if kind==6:markers.append((tick,payload.decode('latin1').lower()))
    continue
   if status in (240,247):n=vlq();i+=n;continue
   running=status;kind=status>>4;ch=status&15
   n=1 if kind in (12,13) else 2;v=data[i:i+n];i+=n
   events.append((tick,track,kind,ch,*v))
 # Type-1 files can repeat tempo at the same tick; latest metadata wins.
 tempo=dict(tempos);ticks=sorted(tempo);seconds=[0.]
 for a,b in zip(ticks,ticks[1:]):seconds.append(seconds[-1]+(b-a)*tempo[a]/division/1e6)
 def sec(t):
  j=bisect.bisect_right(ticks,t)-1;return seconds[j]+(t-ticks[j])*tempo[ticks[j]]/division/1e6
 active={};program={};notes=[]
 for e in sorted(events,key=lambda e:e[:2]):
  tick,track,kind,ch,*v=e;k=(track,ch,v[0])
  if kind==12:program[(track,ch)]=v[0]
  elif kind==9 and v[1]>0:
   if k in active:
    begin,vel,prog=active.pop(k);notes.append([sec(begin),max(.03,sec(tick)-sec(begin)),v[0],vel,prog,ch])
   active[k]=(tick,v[1],program.get((track,ch),0))
  elif kind==8 or kind==9 and v[1]==0:
   if k in active:
    begin,vel,prog=active.pop(k);notes.append([sec(begin),max(.03,sec(tick)-sec(begin)),v[0],vel,prog,ch])
 for (track,ch,note),(begin,vel,prog) in active.items():notes.append([sec(begin),min(2,max(.03,sec(last)-sec(begin))),note,vel,prog,ch])
 assert notes,'No playable notes'
 start=min(n[0] for n in notes);notes=sorted([[round(t-start,3),round(min(d,12),3),p,v,pg,c] for t,d,p,v,pg,c in notes])
 # Original loops end exactly on the end-of-track tick so the next pass lands on the beat.
 duration=sec(last)-start if exact else max(t+d for t,d,*_ in notes)+.3
 return {'duration':round(duration,3),'notes':notes}

def main():
 sources=json.loads((ROOT/'audio/sources.json').read_text());bank=[]
 for t in sources['tracks']:
  track={**t,'gain':{'g1_pallet':1.3,'g2_park':1.3,'g7_gladion':.85,'g9_area_zero':2.5,'orig_oak':1.4,'orig_lake':1.7,'orig_tower':1.9,'orig_burrow':2.5,'orig_storm':1.6}.get(t['id'],1),**decode((ROOT/'audio/midi'/(t['id']+'.mid')).read_bytes(),t.get('loop',False))};bank.append(track)
 runtime=(ROOT/'audio/player-source.js').read_text().replace('/* MUSIC_DATA */',json.dumps(bank,ensure_ascii=False,separators=(',',':')))
 (ROOT/'audio/music-player.js').write_text(runtime)
 html=ROOT/'index.html';s=html.read_text();begin='/* MUSIC_BEGIN */';end='/* MUSIC_END */'
 if begin in s:
  a=s.index(begin)+len(begin);b=s.index(end,a);s=s[:a]+'\n'+runtime+'\n'+s[b:]
 else:s=s.replace('</script>','\n'+begin+'\n'+runtime+'\n'+end+'\n</script>')
 html.write_text(s)
 print('Embedded',len(bank),'tracks /',sum(len(t['notes']) for t in bank),'notes; generations',sorted({t['gen'] for t in bank}))

if __name__=='__main__':main()
