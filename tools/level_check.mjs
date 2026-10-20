// 关卡检查：按游戏里的移动和碰撞规则，模拟「手里有哪几种形态」时从出生点能走到哪里。
// 用法：node tools/level_check.mjs          （先跑 python3 tools/build_world.py 生成 levels/world.json）
//       node tools/level_check.mjs --all    （另外列出每个宝物最早在加上哪种形态后拿得到）
//
// 做法：从出生点开始，在每个站立点试一遍各种走、跳、二段跳、滑翔、撞击冲刺的操作，逐帧模拟落到哪里；
// 水伊布在水里可以自由游动，按格子走。木箱、裂墙可以打开也可以留着当垫脚，两种情况都算。
// 物理常数从 index.html 里读；加速度、水里的浮力这些写死在 updatePlayer 里的数，这里照抄，改手感时两边一起改。
// 这是近似模拟：只试有限几种操作，结果偏保守。报「到不了」时先在游戏里试一下，再决定改关卡还是改这里。
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const WORLD = JSON.parse(fs.readFileSync(path.join(root, 'levels', 'world.json'), 'utf8'));
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const num = name => { const m = html.match(new RegExp('\\b' + name + '\\s*=\\s*(-?[\\d.]+)')); if (!m) throw new Error('index.html 里找不到 ' + name); return +m[1]; };
const GRAVITY = num('GRAVITY'), JUMP_V = num('JUMP_V'), RUN = num('RUN'), PW = num('PW'), PH = num('PH'), T = 16;
const TW = WORLD.tw, TH = WORLD.th;

const NAMES = { eevee: '伊布', vaporeon: '水伊布', jolteon: '雷伊布', flareon: '火伊布', leafeon: '叶伊布', glaceon: '冰伊布', espeon: '太阳伊布', umbreon: '月亮伊布', sylveon: '仙子伊布' };
const ORDER = ['eevee', 'vaporeon', 'jolteon', 'flareon', 'leafeon', 'glaceon', 'espeon', 'umbreon', 'sylveon'];

// ---------------- 地形 ----------------
const ORIG = WORLD.rows.map(r => r.split(''));
const grid = ORIG.map(r => r.slice());
const get = (x, y) => (x < 0 || x >= TW || y < 0 || y >= TH) ? '#' : grid[y][x];
const BREAKABLE = new Uint8Array(TW * TH);   // 原本是木箱或裂墙的格子
for (let y = 0; y < TH; y++) for (let x = 0; x < TW; x++) if (ORIG[y][x] === 'W' || ORIG[y][x] === 'K') BREAKABLE[y * TW + x] = 1;
let broke, observed;   // 这次模拟打开了哪些格子（格子 → 烧 / 撞）、碰到过哪些可打开的格子（用来判断缓存还能不能用）
function solidFor(tx, ty, f, vx) {   // 照抄 index.html 的 solidFor
  const t = get(tx, ty);
  if (t === '#' || t === '=' || t === 'r' || t === 'b' || t === 'B') return true;
  if (tx >= 0 && tx < TW && ty >= 0 && ty < TH && BREAKABLE[ty * TW + tx]) observed.add(ty * TW + tx);
  if (t === 'W') { if (f === 'flareon') { broke.set(ty * TW + tx, 'burn'); return false; } if (f === 'jolteon' && Math.abs(vx) > 2.2) { broke.set(ty * TW + tx, 'smash'); return false; } return true; }
  if (t === 'K') { if (f === 'jolteon' && Math.abs(vx) > 2.2) { broke.set(ty * TW + tx, 'smash'); return false; } return true; }
  if (t === 'D') return true;
  if (t === 'S') return f !== 'umbreon';
  if (t === '~') return f === 'glaceon' && get(tx, ty - 1) !== '~';
  return false;
}
function collide(s, f) {   // 照抄 index.html 的 collide
  s.x += s.vx;
  let x0 = Math.floor(s.x / T), x1 = Math.floor((s.x + PW - 0.01) / T), y0 = Math.floor(s.y / T), y1 = Math.floor((s.y + PH - 0.01) / T);
  for (let ty = y0; ty <= y1; ty++) for (let tx = x0; tx <= x1; tx++)
    if (solidFor(tx, ty, f, s.vx)) { if (s.vx > 0) s.x = tx * T - PW; else if (s.vx < 0) s.x = (tx + 1) * T; s.vx = 0; }
  const prevBottom = s.y + PH;
  s.y += s.vy; s.onGround = false;
  x0 = Math.floor(s.x / T); x1 = Math.floor((s.x + PW - 0.01) / T); y0 = Math.floor(s.y / T); y1 = Math.floor((s.y + PH - 0.01) / T);
  for (let ty = y0; ty <= y1; ty++) for (let tx = x0; tx <= x1; tx++) {
    const oneWay = get(tx, ty) === '-' && s.vy > 0 && prevBottom <= ty * T + 0.01;
    if (solidFor(tx, ty, f, s.vx) || oneWay) { if (s.vy > 0) { s.y = ty * T - PH; s.onGround = true; } else if (s.vy < 0) s.y = (ty + 1) * T; s.vy = 0; }
  }
}

// ---------------- 碰到的东西 ----------------
// 物品（金币、进化石、心之碎片……）按 index.html 的拾取范围；宝箱、巨石、石板和村民按各自的对话范围。
const REACH = { c: [11, 14], h: [11, 14], '*': [11, 14], 1: [11, 14], 2: [11, 14], 3: [11, 14], o: [11, 14], g: [11, 14], u: [11, 14], C: [14, 16], m: [24, 20], i: [24, 20] };
const TARGETS = WORLD.entities.map((e, i) => ({ ...e, i, cx: e.x * T + 8, cy: e.y * T + 8, r: REACH[e.t] || [18, 20] }));
const near = new Map();   // 格子 → 附近的实体
for (const e of TARGETS) for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) {
  const k = (e.y + dy) * TW + e.x + dx; if (!near.has(k)) near.set(k, []); near.get(k).push(e);
}
let touched;
function touch(s) {
  const cx = s.x + PW / 2, cy = s.y + PH / 2, list = near.get(Math.floor(cy / T) * TW + Math.floor(cx / T));
  if (list) for (const e of list) if (Math.abs(e.cx - cx) < e.r[0] && Math.abs(e.cy - cy) < e.r[1]) touched.add(e.i);
}

// ---------------- 逐帧模拟（照抄 updatePlayer 的陆地和水里部分） ----------------
function hazard(s, f) {
  const xs = Math.floor(s.x / T), xe = Math.floor((s.x + PW - 0.01) / T), ys = Math.floor(s.y / T), ye = Math.floor((s.y + PH - 0.01) / T);
  for (let ty = ys; ty <= ye; ty++) for (let tx = xs; tx <= xe; tx++) {
    const t = get(tx, ty);
    if ((t === 'E' && f !== 'jolteon') || t === 'L' || t === '_') return true;
  }
  const foot = Math.floor((s.y + PH - 0.01) / T);
  for (let tx = xs; tx <= xe; tx++) if (get(tx, foot) === '^' && s.y + PH > foot * T + 4) return true;
  return false;
}
// inp(t, s) 返回这一帧的操作 { dir, press, hold, skill, landOk }。返回 { end: 'land' | 'swim' | 'fail' | 'stuck' | 'timeout', s }
function simulate(s0, f, inp, maxT = 240) {
  const s = { ...s0 };
  for (let t = 0; t < maxT; t++) {
    const k = inp(t, s);
    if (k.dir) s.facing = k.dir;
    if (k.skill && f === 'eevee' && s.dashCd <= 0) { s.dash = 10; s.dashCd = 30; s.vx = s.facing * 4.2; s.vy = Math.min(s.vy, 0); }
    if (s.dashCd > 0) s.dashCd--;
    if (s.dash > 0) { s.dash--; s.vx = s.facing * 4.2; }
    const cx = Math.floor((s.x + PW / 2) / T), cy = Math.floor((s.y + PH / 2) / T);
    const inWater = get(cx, cy) === '~' && f !== 'glaceon';
    if (inWater && f === 'vaporeon') return { end: 'swim', s, tx: cx, ty: cy };
    let target = (k.dir || 0) * RUN * (f === 'jolteon' ? 1.6 : 1);
    if (inWater) target *= 0.4;
    const accel = s.onGround ? 0.32 : 0.2;
    if (s.dash > 0) { }
    else if (target !== 0) s.vx += Math.sign(target - s.vx) * Math.min(accel, Math.abs(target - s.vx));
    else s.vx += Math.sign(-s.vx) * Math.min(s.onGround ? 0.28 : 0.1, Math.abs(s.vx));
    if (inWater) {   // 不会游泳的形态：慢慢下沉，按跳可以往上扑腾，憋气 150 帧
      s.vy += 0.06; s.vy = Math.min(s.vy, 0.64);
      if (k.press || t % 12 === 0) s.vy = -1.8;
      s.breath -= 1 / 150; if (s.breath <= 0) return { end: 'fail', s };
      s.jumpsLeft = f === 'leafeon' ? 1 : 0;
    } else {
      if (s.onGround) s.breath = Math.min(1, s.breath + 0.02);
      if (k.press) {
        if (s.onGround) { s.vy = JUMP_V * (f === 'jolteon' ? 1.08 : 1); s.jumpsLeft = f === 'leafeon' ? 1 : 0; }
        else if (s.jumpsLeft > 0) { s.jumpsLeft--; s.vy = JUMP_V * 0.92; }
      }
      if (!k.hold && s.vy < -1.6) s.vy = -1.6;
      s.vy += GRAVITY;
      if (f === 'espeon' && s.vy > 0 && k.hold) s.vy = Math.min(s.vy, 0.44);
      s.vy = Math.min(s.vy, 5.6);
    }
    collide(s, f);
    if (s.onGround) s.jumpsLeft = f === 'leafeon' ? 1 : 0;
    s.x = Math.max(0, Math.min(TW * T - PW, s.x));
    if (hazard(s, f)) return { end: 'fail', s };
    touch(s);
    if (k.walk && s.onGround && t > 6 && Math.abs(s.x - s.x0) < 0.5) return { end: 'stuck', s };
    if (s.onGround && t > 0 && k.landOk) return { end: 'land', s };
  }
  return { end: 'timeout', s };
}

// ---------------- 操作清单 ----------------
// 走：朝一边走 8 像素；走下台阶后可以继续按着、松手或者往回拉。
// 跳：先助跑 0 或 14 帧，按住跳 3 / 10 帧或一直按着，空中方向在起跳时或 14 帧后改；叶伊布加二段跳，伊布加撞击冲刺。
function plans(f) {
  const out = [];
  for (const d of [-1, 1]) for (const after of [d, 0, -d]) {
    out.push((t, s) => {
      if (t === 0) s.left = false;
      if (!s.onGround) s.left = true;
      return { dir: s.left ? after : d, walk: true, landOk: s.left || Math.abs(s.x - s.x0) >= 8 };
    });
  }
  const runs = [[0, 0], [-1, 14], [1, 14]];
  const seconds = f === 'leafeon' ? [0, 10, 18, 26] : [0];
  const dashes = f === 'eevee' ? [0, 6, 16] : [0];
  for (const [d0, r] of runs) for (const h of [3, 10, 999]) for (const d1 of [-1, 0, 1]) for (const a of [0, 14]) for (const j2 of seconds) for (const da of dashes) {
    if (a === 14 && d1 === d0) continue;
    if ((j2 || da) && h !== 999) continue;
    out.push((t, s) => {
      if (t < r) return { dir: d0 };
      const u = t - r;
      return { dir: u < a ? d0 : d1, press: u === 0 || (j2 > 0 && u === j2), hold: u < h || (j2 > 0 && u >= j2), skill: da > 0 && u === da, landOk: u > 0 };
    });
  }
  return out;
}
const PLANS = Object.fromEntries(ORDER.map(f => [f, plans(f)]));
const startState = (x, y) => ({ x, y, x0: x, vx: 0, vy: 0, onGround: true, jumpsLeft: 0, facing: 1, dash: 0, dashCd: 0, breath: 1 });

// 水伊布在水里：能放得下身体的水格之间自由移动；在水面可以跳出去（vy = -3.6）。
function boxFree(x, y, f) {
  const x0 = Math.floor(x / T), x1 = Math.floor((x + PW - 0.01) / T), y0 = Math.floor(y / T), y1 = Math.floor((y + PH - 0.01) / T);
  for (let ty = y0; ty <= y1; ty++) for (let tx = x0; tx <= x1; tx++) if (solidFor(tx, ty, f, 0)) return false;
  return true;
}
function swimPos(tx, ty) {
  if (get(tx, ty) !== '~') return null;
  for (const oy of [-1, -8, 6]) for (const ox of [2, -5, 9]) { const x = tx * T + ox, y = ty * T + oy; if (boxFree(x, y, 'vaporeon')) return { x, y }; }
  return null;
}
const standNode = s => ({ kind: 'a', key: 'a' + Math.round(s.x / 6) + ',' + Math.round(s.y), x: s.x, y: s.y });
const swimNode = (tx, ty) => swimPos(tx, ty) ? { kind: 'w', key: 'w' + tx + ',' + ty, tx, ty } : null;

// 一个站立点 / 水格用某个形态能去哪：结果按「碰到过的可打开格子当时开没开」缓存，地形没变就直接用。
const memo = new Map();
let opened = new Uint8Array(TW * TH);
function edges(n, f) {
  const mk = n.key + '|' + f, variants = memo.get(mk) || [];
  for (const v of variants) if (v.obs.every(([i, o]) => opened[i] === o)) return v.res;
  broke = new Map(); observed = new Set(); touched = new Set();
  const nodes = [];
  const take = r => { if (r.end === 'land') nodes.push(standNode(r.s)); else if (r.end === 'swim') { const w = swimNode(r.tx, r.ty); if (w) nodes.push(w); } };
  if (n.kind === 'a') {
    touch({ x: n.x, y: n.y });
    take(simulate(startState(n.x, n.y), f, () => ({ landOk: true }), 200));   // 换成这个形态后原地掉下去（比如冰面上换形态）
    for (const p of PLANS[f]) take(simulate(startState(n.x, n.y), f, p));
  } else if (f === 'vaporeon') {
    touch(swimPos(n.tx, n.ty));
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]) { const w = swimNode(n.tx + dx, n.ty + dy); if (w) nodes.push(w); }
    if (get(n.tx, n.ty - 1) !== '~') {
      for (const ox of [-4, 0, 4]) for (const d of [-1, 0, 1]) for (const h of [999, 4]) {
        const s = startState(n.tx * T + 8 - PW / 2 + ox, n.ty * T - PH / 2 + 1); s.onGround = false; s.vy = -3.6; s.vx = d * RUN;
        if (!boxFree(s.x, s.y, f)) continue;
        collide(s, f);   // 起跳这一帧在水里，vy = -3.6 直接生效；之后身体中心出了水面，按陆地上算
        take(simulate(s, f, t => ({ dir: d, hold: t < h, landOk: t > 2 })));
      }
    }
  }
  const res = { nodes, touched: [...touched], broke: [...broke] };   // broke：[[格子, 烧 / 撞], ...]
  variants.push({ obs: [...observed].map(i => [i, opened[i]]), res }); memo.set(mk, variants);
  return res;
}

function explore(forms) {
  opened = new Uint8Array(TW * TH);
  for (let y = 0; y < TH; y++) for (let x = 0; x < TW; x++) grid[y][x] = ORIG[y][x];
  const all = new Map(), hit = new Set();
  const start = standNode({ x: WORLD.start.x * T, y: WORLD.start.y * T + T - PH });
  let seeds = [start];
  for (;;) {
    const seen = new Set(seeds.map(n => n.key)), queue = seeds.slice(), fresh = new Map();
    for (const n of queue) all.set(n.key, n);
    while (queue.length) {
      const n = queue.pop();
      for (const f of forms) {
        const e = edges(n, f);
        for (const t of e.touched) hit.add(t);
        for (const [b, how] of e.broke) if (!opened[b] && fresh.get(b) !== 'burn') fresh.set(b, how);
        for (const m of e.nodes) if (!seen.has(m.key)) { seen.add(m.key); queue.push(m); all.set(m.key, m); }
      }
    }
    if (!fresh.size) return hit;
    // 打开新碰到的格子：火烧木箱会连着烧，裂墙上下连着一起碎，雷伊布撞木箱只碎撞到的格子；再从已经到过的所有地方接着找
    for (const [k, how] of fresh) {
      const stack = [[k % TW, Math.floor(k / TW)]];
      while (stack.length) {
        const [x, y] = stack.pop(), t = get(x, y); if (t !== 'W' && t !== 'K') continue;
        grid[y][x] = ' '; opened[y * TW + x] = 1;
        const nb = t === 'K' ? [[0, 1], [0, -1]] : how === 'burn' ? [[1, 0], [-1, 0], [0, 1], [0, -1]] : [];
        for (const [dx, dy] of nb) if (get(x + dx, y + dy) === t) stack.push([x + dx, y + dy]);
      }
    }
    seeds = [...all.values()];
  }
}

// ---------------- 报告 ----------------
const roomName = i => WORLD.rooms[i]?.name || '?';
const KIND = { 1: '水之石', 2: '雷之石', 3: '火之石', m: '苔藓岩', i: '冰岩', h: '心之碎片', '*': '闪光石', T: '石板', C: '宝箱', g: '货物包', V: '村民', o: '果子', s: '存档石', G: '大史莱姆', M: '湖蚌', y: '小史莱姆', u: '材料点' };
const label = e => {
  const note = e.t === 'T' ? (e.text.match(/（[^）]+）/) || [''])[0] : e.t === 'C' || e.t === 'V' || e.t === 'u' ? '「' + e.text.split('|')[0] + '」' : '';
  return `${KIND[e.t]}${note}（${roomName(e.room)}）`;
};
const setName = fs_ => fs_.map(f => NAMES[f]).join(' + ');

// 进度门：「只有这几种形态时」必须到得了 / 必须到不了的地方，对应 DESIGN.md 第 2、3.2 节。改关卡时一起改。
const GATES = [
  { forms: ['eevee'], reach: ['1'], block: ['2', '3'], why: '序章：只有伊布时能拿到水之石，湖泊和雷电塔进不去' },
  { forms: ['eevee', 'vaporeon'], reach: ['2', '3'], why: '第一圈：有水伊布就能去湖泊拿雷之石，也能从池塘水底游进塔基，爬到塔顶拿火之石' },
  { forms: ['eevee', 'jolteon'], reach: ['3'], why: '第一圈：雷伊布走塔门电网也能到塔顶（这一条只看雷电塔这一扇门）' },
];
let bad = 0;
const cache = new Map();
const run = forms => { const k = forms.join(); if (!cache.has(k)) cache.set(k, explore(forms)); return cache.get(k); };
for (const g of GATES) {
  const hit = run(g.forms);
  const has = t => TARGETS.some(e => e.t === t && hit.has(e.i));
  const miss = g.reach.filter(t => !has(t)), leak = (g.block || []).filter(t => has(t));
  const ok = !miss.length && !leak.length; if (!ok) bad++;
  console.log(`${ok ? '✓' : '✗'} ${setName(g.forms)}：${g.why}`);
  for (const t of miss) console.log('    到不了：' + TARGETS.filter(e => e.t === t).map(label).join('、'));
  for (const t of leak) console.log('    不该到得了：' + TARGETS.filter(e => e.t === t).map(label).join('、'));
}

// 按推荐顺序一步步加形态，看每处最早在哪一步拿得到；8 种进化全有也拿不到的算错误。
const first = new Map();
for (let i = 1; i <= ORDER.length; i++) {
  const hit = run(ORDER.slice(0, i));
  for (const e of TARGETS) if (!first.has(e.i) && hit.has(e.i)) first.set(e.i, ORDER[i - 1]);
}
const wanted = e => KIND[e.t] && !(e.t === 'V' && e.text.endsWith('|home'));
const lost = TARGETS.filter(e => wanted(e) && !first.has(e.i));
if (lost.length) { bad++; console.log(`✗ 8 种进化全有也拿不到的 ${lost.length} 处：`); for (const e of lost) console.log('    ' + label(e)); }
else console.log('✓ 所有宝物、石板、村民在 8 种进化全有时都拿得到');
const coins = TARGETS.filter(e => e.t === 'c'), coinMiss = coins.filter(e => !first.has(e.i));
console.log(`  金币 ${coins.length - coinMiss.length} / ${coins.length} 枚拿得到` + (coinMiss.length ? '，拿不到的在：' + [...new Set(coinMiss.map(e => roomName(e.room)))].join('、') : ''));
if (process.argv.includes('--all')) {
  console.log('\n每处最早拿得到的一步（按 伊布 → 水 → 雷 → 火 → 叶 → 冰 → 太阳 → 月亮 → 仙子 的顺序加形态）：');
  for (const f of ORDER) {
    const list = TARGETS.filter(e => wanted(e) && first.get(e.i) === f);
    if (list.length) console.log(`  加上${NAMES[f]}：` + list.map(label).join('、'));
  }
}
process.exit(bad ? 1 : 0);
