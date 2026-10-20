// Self-contained soft MIDI synthesizer. First interaction unlocks audio;
// source arrangements and composer/transcriber attribution live in the bank.
const Music = (() => {
  const tracks = /* MUSIC_DATA */;
  const byId = Object.fromEntries(tracks.map(t => [t.id, t]));
  // orig_* 是为本作写的原创曲（tools/compose_music.py）；剧情场景用 story:<场景 id>
  const playlists = {title:['orig_oak'],village:['g3_littleroot','g1_pallet','orig_oak'],plains:['g3_route101','g8_route1'],burrow:['orig_burrow'],lake:['orig_lake','g6_snowbelle'],lakecave:['g9_area_zero'],tower:['orig_tower','g5_driftveil'],bigslime:['g8_bede'],clam:['g7_gladion'],cloud:['g4_cynthia'],'story:prologueEnd':['orig_oak'],'story:chapter1End':['orig_storm']};
  const levels = {'story:prologueEnd':.55};   // 场景音量（序章收尾在对话底下放得轻一点）
  // 地区的曲子记住放到哪，回来接着放；标题、Boss 和剧情每次从头放
  const resumes = key => key!=='title'&&!key.startsWith('story:')&&!['bigslime','clam','cloud'].includes(key);
  const FADE=1.2,LOOK=.22;
  let pref = {muted:false,volume:28,selection:'auto'};
  try { pref={...pref,...JSON.parse(localStorage.getItem('eevee-music-v1')||'{}')}; } catch {}
  if(!byId[pref.selection])pref.selection='auto';
  pref.volume=Math.max(0,Math.min(100,+pref.volume||0));
  let ac=null,master=null,unlocked=false,deck=null,sceneKey='',scheduled=0;
  const voices=new Set(),cycles={},positions={};
  const save=()=>{try{localStorage.setItem('eevee-music-v1',JSON.stringify(pref));}catch{}};
  const waves=new WeakMap();
  function instrument(context,kind){
    let bank=waves.get(context);if(!bank){bank={};waves.set(context,bank);}
    if(!bank[kind]){const harmonics={piano:[0,1,.23,.10,.045,.018],guitar:[0,1,.30,.13,.06,.025],bass:[0,1,.16,.05],flute:[0,1,.06,.025],strings:[0,1,.18,.07,.025],bell:[0,1,.10,.035]}[kind];bank[kind]=context.createPeriodicWave(new Float32Array(harmonics.length),Float32Array.from(harmonics),{disableNormalization:false});}return bank[kind];
  }
  function sound(context,output,n,time,limit=12,loudness=1) {
    const [,duration,pitch,velocity,program,channel]=n;
    if(pitch<24||pitch>108||duration<=0)return;
    // Smooth band-limited voices replace the short, noisy GBA sample loops.
    const drum=channel===9,strings=program>=40&&program<56,flute=program>=72&&program<80;
    const kind=strings?'strings':flute?'flute':program>=32&&program<40?'bass':program>=24&&program<32?'guitar':program>=8&&program<16?'bell':'piano';
    if(drum&&![35,36,38,40,41,43,45,47,48,50].includes(pitch))return;
    const length=drum?.10:Math.min(duration,limit,strings||flute?4:2.8);
    const attack=Math.min(length*.35,strings?.065:flute?.025:.012),release=strings?.20:.12;
    const o=context.createOscillator(),g=context.createGain();
    const hz=440*Math.pow(2,(pitch-69)/12);
    if(drum){o.type='sine';o.frequency.setValueAtTime(pitch===35||pitch===36?85:155,time);o.frequency.exponentialRampToValueAtTime(45,time+length);}
    else{o.setPeriodicWave(instrument(context,kind));o.frequency.setValueAtTime(hz,time);}
    const velocityGain=Math.pow(velocity/127,1.35),balance=kind==='bass'?.75:kind==='strings'?.65:1;
    const trackGain=Math.min(2.5,loudness),amp=velocityGain*(drum?.035:.085)*balance*trackGain;
    const end=time+length,hold=amp*(strings||flute?.65:drum?.04:.19);
    g.gain.setValueAtTime(.00001,time);g.gain.linearRampToValueAtTime(amp,time+attack);
    g.gain.exponentialRampToValueAtTime(Math.max(.00001,hold),Math.min(end,time+attack+(strings?.30:.20)));
    g.gain.setTargetAtTime(.00001,end,release/4);
    o.connect(g);g.connect(output);o.start(time);o.stop(end+release);
    if(context===ac){const v={o,g};voices.add(v);o.onended=()=>{voices.delete(v);o.disconnect();g.disconnect();};return v;}
  }
  function stopVoices(){if(!ac)return;for(const v of voices){try{v.g.gain.cancelScheduledValues(ac.currentTime);v.g.gain.setTargetAtTime(.00001,ac.currentTime,.008);v.o.stop(ac.currentTime+.04);}catch{}}voices.clear();}
  function volume(){if(master)master.gain.setTargetAtTime(pref.muted?0:pref.volume/100*.65,ac.currentTime,.06);}
  function pickScene(){if(state==='title'||state==='loading')return 'title';if(state==='scene'&&scene)return 'story:'+scene.id;if(bossActive?.alive)return bossActive.type;return curRoom?.region||'village';}
  const listFor=key=>playlists[key]||playlists.plains;
  function choose(){sceneKey=pickScene();const list=listFor(sceneKey);return pref.selection==='auto'?list[(cycles[sceneKey]||0)%list.length]:pref.selection;}
  const bump=()=>{if(pref.selection==='auto')cycles[sceneKey]=(cycles[sceneKey]||0)+1;};   // 手动选的曲子循环时不动地区的轮换
  function upcoming(){const list=listFor(sceneKey);return pref.selection==='auto'?list[((cycles[sceneKey]||0)+1)%list.length]:pref.selection;}
  // Each track plays through its own gain node ("deck"), so a change of scene crossfades instead of cutting.
  function park(d){if(d?.resume)positions[d.track.id]=Math.max(0,ac.currentTime-d.epoch)%d.track.duration;}
  function fadeOut(d){
    if(!d)return;park(d);const t=ac.currentTime,g=d.gain.gain;
    g.cancelScheduledValues(t);g.setValueAtTime(g.value,t);g.linearRampToValueAtTime(0,t+FADE);
    for(const v of voices)if(v.deck===d)try{v.o.stop(t+FADE+.05);}catch{}
    setTimeout(()=>d.gain.disconnect(),(FADE+.5)*1000);
  }
  function play(id,from){
    const track=byId[id]||tracks[0],resume=resumes(sceneKey),level=levels[sceneKey]??1,t=ac.currentTime;
    let at=from??(resume?positions[track.id]||0:0);if(at>track.duration-1)at=0;
    fadeOut(deck);
    const gain=ac.createGain();gain.gain.setValueAtTime(0,t);gain.gain.linearRampToValueAtTime(level,t+FADE);gain.connect(master);
    let cursor=0;while(cursor<track.notes.length&&track.notes[cursor][0]<at)cursor++;
    deck={track,gain,epoch:t+.08-at,cursor,resume,level};
    now.textContent=I18n.trackLabel(track);credit.textContent=track.credit;
  }
  function tick(){
    if(!unlocked||document.hidden)return;
    const id=choose();
    if(!deck||deck.track.id!==id)play(id);
    else{deck.resume=resumes(sceneKey);const level=levels[sceneKey]??1;if(deck.level!==level){deck.level=level;deck.gain.gain.setTargetAtTime(level,ac.currentTime,FADE/3);}}
    const d=deck,notes=d.track.notes,dur=d.track.duration;let elapsed=ac.currentTime-d.epoch;
    // Skip overdue notes after a suspended tab or while muted, rather than firing a burst.
    while(d.cursor<notes.length&&notes[d.cursor][0]<elapsed-.15)d.cursor++;
    // One pass done: the same track wraps on the beat; a different one takes over from its start.
    if(d.cursor>=notes.length&&elapsed+LOOK>dur){
      const next=upcoming();
      if(next===d.track.id){bump();const k=Math.max(1,Math.floor((elapsed+LOOK)/dur));d.epoch+=k*dur;d.cursor=0;elapsed-=k*dur;}
      else if(elapsed>dur){bump();d.resume=false;delete positions[d.track.id];play(next,0);return;}
    }
    if(pref.muted||pref.volume===0)return;
    while(d.cursor<notes.length&&notes[d.cursor][0]<elapsed+LOOK){
      const n=notes[d.cursor++];if(voices.size<56){const v=sound(ac,d.gain,n,Math.max(ac.currentTime+.005,d.epoch+n[0]),12,d.track.gain);if(v)v.deck=d;scheduled++;}
    }
  }
  async function unlock(){try{if(!ac){ac=new(window.AudioContext||window.webkitAudioContext)();master=ac.createGain();const compressor=ac.createDynamicsCompressor();compressor.threshold.value=-9;compressor.ratio.value=4;const low=ac.createBiquadFilter();low.type='lowpass';low.frequency.value=3800;low.Q.value=.5;master.connect(low);low.connect(compressor);compressor.connect(ac.destination);volume();}await ac.resume();unlocked=ac.state==='running';if(unlocked)tick();}catch{now.textContent=I18n.t('点击音乐按钮启用声音');}}
  const style=document.createElement('style');style.textContent=`
  #eeveeMusic{position:fixed;left:50%;transform:translateX(-50%);bottom:max(6px,env(safe-area-inset-bottom));z-index:9;font:12px system-ui;color:#ebdfbc}
  #eeveeMusic button,#eeveeMusic select{font:inherit;border:1px solid #a5b188;border-radius:6px;color:#ebdfbc;background:#354f43;padding:5px 10px;cursor:pointer}
  #eeveeMusicPanel{position:absolute;bottom:34px;left:50%;transform:translateX(-50%);width:280px;max-width:85vw;padding:13px;background:#314a40f5;border:1px solid #b3bd92;border-radius:9px;box-shadow:0 4px 20px #172d3266}
  #eeveeMusicPanel[hidden]{display:none}#eeveeMusicPanel select{display:block;width:100%;margin:9px 0}#eeveeMusicPanel input{width:150px;vertical-align:middle;accent-color:#cfbe8a}#eeveeMusicPanel small{display:block;color:#afbea2;margin-top:7px;font-size:10px}
  #eeveeMusicPanel p{margin:0 0 8px}#eeveeMusic button:focus-visible,#eeveeMusic select:focus-visible{outline:2px solid #eed9a0}
  `;document.head.append(style);
  const box=document.createElement('div');box.id='eeveeMusic';
  box.innerHTML='<button type="button" id="eeveeMusicOpen" aria-expanded="false">♫ 音乐</button><section id="eeveeMusicPanel" hidden aria-label="音乐设置"><p id="eeveeMusicNow">首次操作后开始播放</p><select aria-label="选择背景音乐"></select><label>音量 <input type="range" min="0" max="100" aria-label="背景音乐音量"></label> <button type="button" id="eeveeMusicMute">静音</button><small id="eeveeMusicCredit"></small><small>MIDI 改编合成播放 · P 键开关音乐</small></section>';
  document.body.append(box);
  const open=box.querySelector('#eeveeMusicOpen'),panel=box.querySelector('section'),select=box.querySelector('select'),slider=box.querySelector('input'),mute=box.querySelector('#eeveeMusicMute'),now=box.querySelector('#eeveeMusicNow'),credit=box.querySelector('#eeveeMusicCredit');
  select.add(new Option('自动 · 随场景切换','auto'));for(const t of tracks)select.add(new Option(`${t.gen?`第 ${t.gen} 世代`:'原创'} · ${t.title}`,t.id));select.value=pref.selection;slider.value=pref.volume;
  function labels(){mute.textContent=I18n.t(pref.muted?'开启':'静音');mute.setAttribute('aria-pressed',String(pref.muted));open.textContent=I18n.t(pref.muted?'♫ 已静音':'♫ 音乐');}
  function toggleMute(){pref.muted=!pref.muted;save();volume();labels();unlock();}
  open.onclick=()=>{panel.hidden=!panel.hidden;open.setAttribute('aria-expanded',String(!panel.hidden));unlock();};
  select.onchange=()=>{pref.selection=select.value;save();unlock();};
  slider.oninput=()=>{pref.volume=+slider.value;save();volume();unlock();};mute.onclick=toggleMute;
  box.addEventListener('keydown',e=>e.stopPropagation());
  window.addEventListener('keydown',e=>{if(I18n.isOpen)return;if(!box.contains(e.target)&&e.key.toLowerCase()==='p'){e.preventDefault();e.stopImmediatePropagation();toggleMute();}},true);
  window.addEventListener('pointerdown',unlock,{once:true});window.addEventListener('keydown',unlock,{once:true});
  document.addEventListener('visibilitychange',()=>{if(document.hidden){park(deck);stopVoices();deck?.gain.disconnect();deck=null;}else if(unlocked){ac.resume();tick();}});
  labels();setInterval(tick,90);
  return {tracks:tracks.map(({notes,...t})=>({...t,noteCount:notes.length})),status:()=>({unlocked,track:deck?.track.id,scene:sceneKey,at:deck?Math.round((ac.currentTime-deck.epoch)*10)/10:0,level:deck?.level,scheduled,activeVoices:voices.size,muted:pref.muted,selection:pref.selection}),
    async testRender(id){const t=byId[id],context=new OfflineAudioContext(1,44100*8,44100),gain=context.createGain();gain.gain.value=.2;gain.connect(context.destination);for(const n of t.notes)if(n[0]<7.8)sound(context,gain,n,n[0]+.01,7.8-n[0],t.gain);const b=await context.startRendering(),a=b.getChannelData(0);let sum=0,peak=0;for(const v of a){sum+=v*v;peak=Math.max(peak,Math.abs(v));}return {id,rms:Math.sqrt(sum/a.length),peak};}};
})();
