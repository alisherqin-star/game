// Translation stays at the display boundary. Save data and world names keep stable IDs.
const I18n=(()=>{
 const bank=/* LOCALE_DATA */;
 let lang='zh';try{const saved=localStorage.getItem('eevee-language-v1');if(['zh','ja','en'].includes(saved))lang=saved;}catch{}
 const cache={zh:new Map(),ja:new Map(),en:new Map()},outputs={ja:new Set(),en:new Set()};
 const escape=s=>[...s].map(c=>'.*+?^${}()|[]'.includes(c)||c.charCodeAt(0)===92?String.fromCharCode(92)+c:c).join('');
 const pattern=new RegExp(Object.keys(bank).sort((a,b)=>b.length-a.length).map(escape).join('|'),'g');
 function t(value){const s=String(value??'');if(lang==='zh'||!s||outputs[lang].has(s))return s;if(cache[lang].has(s))return cache[lang].get(s);const result=bank[s]?.[lang]??s.replace(pattern,k=>bank[k][lang]);cache[lang].set(s,result);outputs[lang].add(result);return result;}
 function mark(s){if(lang!=='zh')outputs[lang].add(s);return s;}
 function trackLabel(track){return lang==='zh'?`第 ${track.gen} 世代 · ${track.title}`:lang==='ja'?`第${track.gen}世代 · ${t(track.title)}`:`Gen ${track.gen} · ${t(track.title)}`;}
 const ids={bJ:'跳',bS:'技',bF:'形态',bM:'地图',bI:'背包'};
 function refreshMusic(){
  const box=document.getElementById('eeveeMusic');if(!box)return;
  const s=Music.status();box.querySelector('#eeveeMusicOpen').textContent=t(s.muted?'♫ 已静音':'♫ 音乐');
  box.querySelector('section').setAttribute('aria-label',t('音乐设置'));
  const sel=box.querySelector('select');sel.setAttribute('aria-label',t('选择背景音乐'));sel.options[0].textContent=t('自动 · 随场景切换');
  Music.tracks.forEach((track,i)=>sel.options[i+1].textContent=trackLabel(track));
  const track=Music.tracks.find(x=>x.id===s.track);box.querySelector('#eeveeMusicNow').textContent=track?trackLabel(track):t('首次操作后开始播放');
  box.querySelector('#eeveeMusicMute').textContent=t(s.muted?'开启':'静音');
  const label=box.querySelector('label');label.firstChild.textContent=t('音量 ');label.querySelector('input').setAttribute('aria-label',t('背景音乐音量'));
  box.querySelector('small:last-child').textContent=t('MIDI 改编合成播放 · P 键开关音乐');
 }
 function apply(){
  document.documentElement.lang={zh:'zh-CN',ja:'ja',en:'en'}[lang];document.title=lang==='zh'?'伊布：归途的约定':lang==='ja'?'イーブイ：帰り道の約束':'Eevee: A Promise to Return';
  for(const [id,source]of Object.entries(ids))document.getElementById(id).textContent=t(source);
  const rotate=document.getElementById('rotate');rotate.replaceChildren();const icon=document.createElement('div');icon.style.fontSize='48px';icon.textContent='📱↻';const help=document.createElement('span');help.style.cssText='font-size:14px;opacity:.7';help.textContent=t('左下角移动，右下角跳跃，点左上角物品栏切换形态，右上角地图 / 背包，跳跃键左边是技能');rotate.append(icon,t('请把手机横过来玩'),document.createElement('br'),help);
  document.querySelectorAll('[data-l10n]').forEach(el=>el.textContent=t(el.dataset.l10n));refreshMusic();
 }
 function set(next){if(!['zh','ja','en'].includes(next))return;lang=next;try{localStorage.setItem('eevee-language-v1',lang);}catch{}apply();document.querySelectorAll('[data-language]').forEach(b=>{b.setAttribute('aria-pressed',String(b.dataset.language===lang));});}
 let modal=null,returnFocus=null;
 function close(){if(!modal?.open)return;modal.close();returnFocus?.focus();}
 function open(){
  if(!modal){
   const style=document.createElement('style');style.textContent=`#eeveeSettings{box-sizing:border-box;width:min(410px,92vw);max-height:90dvh;overflow:auto;border:2px solid #aebb8e;border-radius:16px;padding:25px;background:#304e41;color:#f4e6c3;box-shadow:0 14px 70px #152b31a0;font:15px system-ui}#eeveeSettings::backdrop{background:#152b32b8}#eeveeSettings h2{font-size:23px;margin:0 0 22px}#eeveeSettings fieldset{border:0;padding:0;margin:0 0 22px}#eeveeSettings legend{margin-bottom:12px;color:#d1d9b5}#eeveeSettings .languages{display:flex;gap:8px}#eeveeSettings button{font:inherit;border:1px solid #9daf85;border-radius:9px;padding:10px 14px;color:#f3e6c7;background:#426451;cursor:pointer}#eeveeSettings button[aria-pressed=true]{background:#eddbac;color:#3c5744;border-color:#eddbac}#eeveeSettings button:focus-visible,#eeveeSettings input:focus-visible{outline:3px solid #f9dfa0;outline-offset:3px}#eeveeSettings input[type=range]{width:100%;accent-color:#e7d29d;margin:16px 0}#eeveeSettings .footer{display:flex;align-items:center;justify-content:space-between;gap:12px}#eeveeSettings small{display:block;font-size:12px;color:#bbcaaa;margin-top:22px}`;document.head.append(style);
   modal=document.createElement('dialog');modal.id='eeveeSettings';modal.setAttribute('aria-labelledby','settingsTitle');
   modal.innerHTML='<h2 id="settingsTitle" data-l10n="设置"></h2><fieldset><legend data-l10n="语言"></legend><div class="languages"><button type="button" data-language="zh" lang="zh-CN">简体中文</button><button type="button" data-language="ja" lang="ja">日本語</button><button type="button" data-language="en" lang="en">English</button></div></fieldset><label for="settingsVolume" data-l10n="音乐音量"></label><output id="settingsVolumeValue"></output><input id="settingsVolume" type="range" min="0" max="100"><div class="footer"><label><input type="checkbox" id="settingsMute"> <span data-l10n="静音"></span></label><button type="button" id="settingsBack" data-l10n="返回"></button></div><small data-l10n="已自动保存设置"></small>';
   document.body.append(modal);modal.querySelectorAll('[data-language]').forEach(b=>b.onclick=()=>set(b.dataset.language));modal.querySelector('#settingsBack').onclick=close;
   modal.addEventListener('cancel',e=>{e.preventDefault();close();});
   modal.addEventListener('click',e=>{if(e.target===modal){const r=modal.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)close();}});
   modal.querySelector('#settingsVolume').oninput=e=>{const v=e.target.value;const music=document.querySelector('#eeveeMusic input');music.value=v;music.dispatchEvent(new Event('input'));modal.querySelector('output').textContent=' '+v+'%';};
   modal.querySelector('#settingsMute').onchange=e=>{if(Music.status().muted!==e.target.checked)document.querySelector('#eeveeMusicMute').click();};
   // Block game shortcuts while preserving the dialog's native Tab and arrow controls.
   window.addEventListener('keydown',e=>{if(!modal.open)return;e.stopImmediatePropagation();if(e.key==='Escape'){e.preventDefault();close();}},true);
  }
  returnFocus=document.activeElement;for(const key of Object.keys(keys))keys[key]=false;jumpQueued=false;skillQueued=false;
  modal.querySelector('#settingsVolume').value=document.querySelector('#eeveeMusic input').value;modal.querySelector('output').textContent=' '+modal.querySelector('#settingsVolume').value+'%';modal.querySelector('#settingsMute').checked=Music.status().muted;
  set(lang);modal.showModal();modal.querySelector(`[data-language="${lang}"]`).focus();
 }
 document.addEventListener('DOMContentLoaded',apply);
 return {t,mark,set,open,close,apply,refreshMusic,trackLabel,get lang(){return lang;},get isOpen(){return !!modal?.open;}};
})();
