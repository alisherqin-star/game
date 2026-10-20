# 原创背景音乐：写成标准 MIDI 文件放进 audio/midi/，再由 tools/embed_music.py 嵌进游戏。
# 用法：python3 tools/compose_music.py && python3 tools/embed_music.py
#
# 五首曲子（都由 Claude 为本作原创，不来自任何已有作品）：
#   orig_oak    橡树下      F 大调 3/4 拍  84  长笛主旋律、尼龙吉他分解和弦；标题、村子、序章收尾
#   orig_lake   湖面        D 大调 4/4 拍  76  钢琴流水琶音、长笛长音、钟琴水滴；湖泊水面
#   orig_tower  雷电塔      A 小调 4/4 拍 132  八分音符贝斯固定音型、电吉他主旋律、鼓；雷电塔
#   orig_burrow 地洞        E 小调 4/4 拍 100  马林巴跳音、贝斯断奏、轻鼓；草原地下
#   orig_storm  风里的声音  F 小调 3/4 拍  60  慢弦乐，长笛用小调吹「橡树下」的主题；第一章收尾
# 音色用 General MIDI 的程序号（从 0 数），播放器按范围归成六种：
#   0 钢琴  8～15 钟琴类  24～31 吉他  32～39 贝斯  40～55 弦乐  72～79 长笛；第 10 通道（9）是鼓，只用 35/36 底鼓、38/40 军鼓、41～50 通鼓。
# 每首都写满整数小节，最后一小节有伴奏一直响到结尾，循环时拍子接得上。
import os, struct

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
NAMES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

def P(name):
    """音名 → MIDI 音高，例如 'C4' = 60，'Bb3'、'F#5'。"""
    base = NAMES[name[0]]; i = 1
    while name[i] in '#b': base += 1 if name[i] == '#' else -1; i += 1
    return base + 12 * (int(name[i:]) + 1)

def vlq(n):
    out = [n & 127]; n >>= 7
    while n: out.append((n & 127) | 128); n >>= 7
    return bytes(reversed(out))

def write_mid(path, bpm, parts, total_beats):
    """parts：[(通道, 程序号, [(拍, 时值拍, 音名或音高, 力度), ...])]，写成 format 0。"""
    div = 480; events = [(0, 0, b'\xff\x51\x03' + struct.pack('>I', round(60_000_000 / bpm))[1:])]
    for ch, prog, notes in parts:
        if ch != 9: events.append((0, 1, bytes([0xC0 | ch, prog])))
        for beat, dur, pitch, vel in notes:
            p = P(pitch) if isinstance(pitch, str) else pitch
            assert beat < total_beats, (path, beat)
            dur = min(dur, total_beats - beat)   # 最后一个音不越过循环点
            on, off = round(beat * div), max(round(beat * div) + 1, round((beat + dur) * div) - 1)
            events.append((on, 3, bytes([0x90 | ch, p, vel]))); events.append((off, 2, bytes([0x80 | ch, p, 0])))
    events.sort(key=lambda e: (e[0], e[1]))
    data, last = b'', 0
    for tick, _, ev in events: data += vlq(tick - last) + ev; last = tick
    data += vlq(round(total_beats * div) - last) + b'\xff\x2f\x00'   # 轨道结束正好落在循环点上
    with open(path, 'wb') as f:
        f.write(b'MThd' + struct.pack('>IHHH', 6, 0, 1, div) + b'MTrk' + struct.pack('>I', len(data)) + data)

def bars(chords, beats_per_bar, fn):
    """对每个小节调用 fn(小节号, 和弦, 小节起点拍)，把返回的音符拼起来。"""
    out = []
    for i, c in enumerate(chords): out += fn(i, c, i * beats_per_bar)
    return out

def melody(lines, beats_per_bar, start_bar=0, shift=0, vel=None):
    """lines：每小节一组 (拍, 时值, 音名)；shift 移八度（半音数），vel 统一力度。"""
    out = []
    for i, bar in enumerate(lines):
        for beat, dur, name in bar:
            out.append(((start_bar + i) * beats_per_bar + beat, dur, P(name) + shift, vel or 88))
    return out

# =================== 橡树下（F 大调 3/4）===================
def oak():
    chords = ['F', 'C/E', 'Dm', 'Bb', 'F', 'Gm7', 'C', 'C7', 'F', 'C/E', 'Dm', 'Bb', 'Gm', 'C', 'F', 'F'] * 2
    gtr = {'F': 'F3 C4 F4 A4', 'C/E': 'E3 C4 E4 G4', 'Dm': 'D3 A3 D4 F4', 'Bb': 'Bb2 F3 Bb3 D4', 'Gm7': 'G3 D4 F4 Bb4', 'C': 'C3 G3 C4 E4', 'C7': 'C3 G3 Bb3 E4', 'Gm': 'G3 D4 G4 Bb4'}
    bass = {'F': 'F2', 'C/E': 'E2', 'Dm': 'D2', 'Bb': 'Bb1', 'Gm7': 'G2', 'C': 'C2', 'C7': 'C2', 'Gm': 'G2'}
    pad = {'F': 'A3 C4 F4', 'C/E': 'G3 C4 E4', 'Dm': 'A3 D4 F4', 'Bb': 'Bb3 D4 F4', 'Gm7': 'Bb3 D4 F4', 'C': 'G3 C4 E4', 'C7': 'Bb3 E4 G4', 'Gm': 'Bb3 D4 G4'}
    guitar = bars(chords, 3, lambda i, c, b0: [(b0 + k * 0.5, 0.5, gtr[c].split()[j], 62 if k == 0 else 50) for k, j in enumerate([0, 1, 2, 3, 2, 1])])
    low = bars(chords, 3, lambda i, c, b0: [(b0, 2.5, bass[c], 66)])
    strings = bars(chords, 3, lambda i, c, b0: [(b0, 3, n, 30) for n in pad[c].split()])
    tune = [
        [(0, 1.5, 'C5'), (1.5, 0.5, 'A4'), (2, 1, 'F4')], [(0, 2, 'G4'), (2, 1, 'E4')], [(0, 1, 'F4'), (1, 1, 'A4'), (2, 1, 'D5')], [(0, 3, 'C5')],
        [(0, 1.5, 'C5'), (1.5, 0.5, 'A4'), (2, 1, 'F4')], [(0, 2, 'Bb4'), (2, 0.5, 'A4'), (2.5, 0.5, 'G4')], [(0, 1, 'G4'), (1, 1, 'A4'), (2, 1, 'Bb4')], [(0, 3, 'G4')],
        [(0, 1.5, 'C5'), (1.5, 0.5, 'A4'), (2, 1, 'F4')], [(0, 2, 'G4'), (2, 1, 'C5')], [(0, 1.5, 'D5'), (1.5, 0.5, 'C5'), (2, 1, 'A4')], [(0, 2, 'Bb4'), (2, 1, 'D5')],
        [(0, 1, 'C5'), (1, 1, 'Bb4'), (2, 1, 'A4')], [(0, 1.5, 'G4'), (1.5, 0.5, 'F4'), (2, 1, 'E4')], [(0, 3, 'F4')], []]
    flute = melody(tune, 3, 0, vel=84) + melody(tune, 3, 16, vel=84)
    celesta = melody(tune, 3, 16, shift=12, vel=40)   # 第二遍：钟琴在高八度跟着唱
    return 84, [(0, 24, guitar), (1, 73, flute), (2, 33, low), (3, 48, strings), (4, 8, celesta)], len(chords) * 3

# =================== 湖面（D 大调 4/4）===================
def lake():
    chords = ['Dmaj7', 'Gmaj7', 'Bm7', 'Asus', 'Dmaj7', 'Gmaj7', 'Em7', 'A', 'Bm7', 'Gmaj7', 'Dmaj7', 'A', 'Bm7', 'Gmaj7', 'Em7', 'Asus']
    arp = {'Dmaj7': 'D3 A3 C#4 E4 F#4 E4 C#4 A3', 'Gmaj7': 'G3 D4 F#4 A4 B4 A4 F#4 D4', 'Bm7': 'B2 F#3 A3 D4 F#4 D4 A3 F#3',
           'A': 'A2 E3 A3 C#4 E4 C#4 A3 E3', 'Asus': 'A2 E3 A3 D4 E4 D4 C#4 E3', 'Em7': 'E3 B3 D4 G4 B4 G4 D4 B3'}
    roots = {'Dmaj7': 'D2', 'Gmaj7': 'G2', 'Bm7': 'B1', 'A': 'A1', 'Asus': 'A1', 'Em7': 'E2'}
    pad = {'Dmaj7': 'F#3 A3 C#4', 'Gmaj7': 'F#3 B3 D4', 'Bm7': 'F#3 A3 D4', 'A': 'E3 A3 C#4', 'Asus': 'E3 A3 D4', 'Em7': 'G3 B3 D4'}
    piano = bars(chords, 4, lambda i, c, b0: [(b0 + k * 0.5, 0.9, n, 56 if k % 4 == 0 else 46) for k, n in enumerate(arp[c].split())])
    low = bars(chords, 4, lambda i, c, b0: [(b0, 4, roots[c], 60)])
    strings = bars(chords, 4, lambda i, c, b0: [(b0, 4, n, 26) for n in pad[c].split()])
    tune = [[(0, 4, 'F#5')], [(0, 2, 'E5'), (2, 2, 'D5')], [(0, 3, 'F#5'), (3, 1, 'A5')], [(0, 2, 'E5'), (2, 2, 'C#5')],
            [(0, 2, 'F#5'), (2, 2, 'A5')], [(0, 3, 'B5'), (3, 1, 'A5')], [(0, 2, 'G5'), (2, 2, 'F#5')], [(0, 4, 'E5')],
            [(0, 2, 'D5'), (2, 2, 'F#5')], [(0, 4, 'E5')], [(0, 2, 'F#5'), (2, 1, 'E5'), (3, 1, 'D5')], [(0, 4, 'C#5')],
            [(0, 2, 'B4'), (2, 2, 'D5')], [(0, 2, 'F#5'), (2, 2, 'E5')], [(0, 4, 'D5')], [(0, 2, 'E5'), (2, 2, 'C#5')]]
    flute = melody(tune, 4, vel=74)
    drops = [(b * 4 + 3.5, 0.5, P(n), 38) for b, n in [(1, 'A6'), (5, 'F#6'), (9, 'B6'), (13, 'E6')]]   # 水滴
    return 76, [(0, 0, piano), (1, 73, flute), (2, 33, low), (3, 48, strings), (4, 8, drops)], len(chords) * 4

# =================== 雷电塔（A 小调 4/4）===================
def tower():
    chords = ['Am', 'Am', 'F', 'G', 'Am', 'Am', 'F', 'E', 'Dm', 'Am', 'F', 'G', 'Am', 'F', 'E', 'E'] * 2
    root = {'Am': 'A2', 'F': 'F2', 'G': 'G2', 'E': 'E2', 'Dm': 'D2'}
    triad = {'Am': 'A3 C4 E4', 'F': 'A3 C4 F4', 'G': 'B3 D4 G4', 'E': 'G#3 B3 E4', 'Dm': 'A3 D4 F4'}
    pad = {'Am': 'E3 A3 C4', 'F': 'F3 A3 C4', 'G': 'G3 B3 D4', 'E': 'E3 G#3 B3', 'Dm': 'D3 F3 A3'}
    def bassline(i, c, b0):
        r = P(root[c]); steps = [0, 0, 12, 0, 7, 0, 12, 7]
        return [(b0 + k * 0.5, 0.45, r + s, 92 if k in (0, 4) else 72) for k, s in enumerate(steps)]
    low = bars(chords, 4, bassline)
    stabs = bars(chords, 4, lambda i, c, b0: [(b0 + t, 0.25, n, 58) for t in (1.5, 3.5) for n in triad[c].split()])
    riff = [
        [(0, 0.5, 'E5'), (1, 0.5, 'A5'), (2, 0.5, 'G5'), (2.5, 0.5, 'E5'), (3, 0.5, 'D5'), (3.5, 0.5, 'E5')],
        [(0, 1.5, 'C5'), (1.5, 0.5, 'D5'), (2, 1, 'E5'), (3, 1, 'G5')],
        [(0, 0.5, 'A5'), (1, 0.5, 'C6'), (2, 0.5, 'A5'), (2.5, 0.5, 'G5'), (3, 1, 'F5')],
        [(0, 1.5, 'G5'), (1.5, 0.5, 'F5'), (2, 1, 'D5'), (3, 1, 'B4')],
        [(0, 0.5, 'E5'), (1, 0.5, 'A5'), (2, 0.5, 'G5'), (2.5, 0.5, 'E5'), (3, 0.5, 'D5'), (3.5, 0.5, 'E5')],
        [(0, 1.5, 'C5'), (1.5, 0.5, 'D5'), (2, 1, 'E5'), (3, 1, 'A5')],
        [(0, 1, 'C6'), (1, 1, 'A5'), (2, 1, 'F5'), (3, 1, 'A5')],
        [(0, 2, 'G#5'), (2, 1, 'B5'), (3, 1, 'E5')],
        [(0, 1, 'F5'), (1, 0.5, 'E5'), (1.5, 0.5, 'D5'), (2, 2, 'A5')],
        [(0, 1, 'E5'), (1, 0.5, 'D5'), (1.5, 0.5, 'C5'), (2, 2, 'E5')],
        [(0, 1, 'F5'), (1, 1, 'A5'), (2, 1, 'C6'), (3, 1, 'A5')],
        [(0, 2, 'B5'), (2, 1, 'G5'), (3, 1, 'D5')],
        [(0, 0.5, 'E5'), (0.5, 0.5, 'A5'), (1, 0.5, 'C6'), (1.5, 0.5, 'A5'), (2, 1, 'E5'), (3, 1, 'A5')],
        [(0, 2, 'C6'), (2, 1, 'A5'), (3, 1, 'F5')],
        [(0, 1, 'E5'), (1, 1, 'G#5'), (2, 1, 'B5'), (3, 1, 'D6')],
        [(0, 3, 'E6')]]
    lead = melody(riff, 4, 0, shift=-12, vel=84) + melody(riff, 4, 16, shift=-12, vel=88)
    sparkle = melody(riff, 4, 16, vel=36)   # 第二遍：钟琴在高八度叠上去
    strings = bars(chords[16:], 4, lambda i, c, b0: [(b0 + 64, 4, n, 34) for n in pad[c].split()])   # 第二遍加弦乐
    def kit(i, c, b0):
        hits = [(b0, 36, 96), (b0 + 1, 38, 70), (b0 + 2, 36, 90), (b0 + 3, 38, 70)]
        if i % 4 == 3: hits.append((b0 + 2.5, 36, 80))
        if i % 16 == 15: hits = [(b0, 36, 96), (b0 + 1, 38, 70)] + [(b0 + 2 + k * 0.5, t, 80) for k, t in enumerate([50, 48, 45, 43])]   # 过门
        return [(t, 0.2, n, v) for t, n, v in hits]
    drums = bars(chords, 4, kit)
    return 132, [(0, 0, stabs), (1, 27, lead), (2, 33, low), (3, 48, strings), (4, 9, sparkle), (9, 0, drums)], len(chords) * 4

# =================== 地洞（E 小调 4/4）===================
def burrow():
    chords = ['Em', 'Em', 'C', 'D', 'Em', 'Em', 'Am', 'B7', 'C', 'D', 'Em', 'Em', 'Am', 'B7', 'Em', 'B7'] * 2
    walk = {'Em': 'E2 G2 B2 G2', 'C': 'C2 E2 G2 E2', 'D': 'D2 F#2 A2 F#2', 'Am': 'A2 C3 E3 C3', 'B7': 'B1 D#2 F#2 A2'}
    low = bars(chords, 4, lambda i, c, b0: [(b0 + k, 0.4, n, 70) for k, n in enumerate(walk[c].split())])
    tune = [
        [(0, 0.5, 'E5'), (1, 0.5, 'G5'), (1.5, 0.5, 'A5'), (3, 0.5, 'B5')], [(0.5, 0.5, 'A5'), (1, 0.5, 'G5'), (2, 0.5, 'E5'), (3, 1, 'D5')],
        [(0, 0.5, 'E5'), (1, 0.5, 'G5'), (1.5, 0.5, 'A5'), (2.5, 0.5, 'B5'), (3, 0.5, 'A5')], [(0, 1, 'F#5'), (1.5, 0.5, 'A5'), (2, 1, 'D5')],
        [(0, 0.5, 'E5'), (1, 0.5, 'G5'), (1.5, 0.5, 'A5'), (3, 0.5, 'B5')], [(0.5, 0.5, 'A5'), (1, 0.5, 'B5'), (2, 0.5, 'D6'), (3, 1, 'B5')],
        [(0, 0.5, 'C6'), (0.5, 0.5, 'B5'), (1, 0.5, 'A5'), (2, 1, 'E5')], [(0, 1, 'D#5'), (1, 1, 'F#5'), (2, 1, 'A5'), (3, 1, 'B5')],
        [(0, 1, 'G5'), (1.5, 0.5, 'E5'), (2, 1, 'C5')], [(0, 1, 'A5'), (1.5, 0.5, 'F#5'), (2, 1, 'D5')],
        [(0, 0.5, 'E5'), (0.5, 0.5, 'G5'), (1, 0.5, 'B5'), (1.5, 0.5, 'E6'), (2, 1, 'B5')], [(1, 0.5, 'G5'), (2, 0.5, 'E5')],
        [(0, 0.5, 'A5'), (1, 0.5, 'C6'), (2, 0.5, 'E6'), (3, 0.5, 'C6')], [(0, 0.5, 'B5'), (1, 0.5, 'A5'), (2, 0.5, 'F#5'), (3, 0.5, 'D#5')],
        [(0, 2, 'E5')], [(2, 0.5, 'B4'), (3, 0.5, 'D#5')]]
    marimba = melody(tune, 4, 0, vel=86) + melody(tune, 4, 16, vel=86)
    celesta = melody(tune, 4, 16, shift=12, vel=34) + [(b * 4 + t, 0.5, P(n), 32) for b, t, n in [(2, 3.5, 'E6'), (6, 2.5, 'B6'), (10, 3.5, 'G6'), (14, 1.5, 'B6')]]
    drums = bars(chords, 4, lambda i, c, b0: [(b0, 0.2, 45, 52), (b0 + 2.5, 0.2, 41, 44)] + ([(b0 + 3.5, 0.2, 48, 40)] if i % 2 else []))
    return 100, [(1, 12, marimba), (2, 33, low), (4, 8, celesta), (9, 0, drums)], len(chords) * 4

# =================== 风里的声音（F 小调 3/4，引用「橡树下」）===================
def storm():
    chords = ['Fm', 'Db', 'Bbm', 'C', 'Fm', 'Db', 'Eb', 'C', 'Fm', 'Db', 'Bbm', 'C', 'Db', 'Bbm', 'C', 'C']
    pad = {'Fm': 'F3 Ab3 C4', 'Db': 'F3 Ab3 Db4', 'Bbm': 'F3 Bb3 Db4', 'C': 'E3 G3 C4', 'Eb': 'G3 Bb3 Eb4'}
    roots = {'Fm': 'F2', 'Db': 'Db2', 'Bbm': 'Bb1', 'C': 'C2', 'Eb': 'Eb2'}
    strings = bars(chords, 3, lambda i, c, b0: [(b0, 3, n, 44) for n in pad[c].split()])
    low = bars(chords, 3, lambda i, c, b0: [(b0, 3, roots[c], 52)])
    tune = [
        [(0, 1.5, 'C5'), (1.5, 0.5, 'Ab4'), (2, 1, 'F4')], [(0, 2, 'Ab4'), (2, 1, 'F4')], [(0, 1, 'F4'), (1, 1, 'Ab4'), (2, 1, 'Db5')], [(0, 3, 'C5')],
        [(0, 1.5, 'C5'), (1.5, 0.5, 'Ab4'), (2, 1, 'F4')], [(0, 2, 'Bb4'), (2, 0.5, 'Ab4'), (2.5, 0.5, 'G4')], [(0, 1, 'G4'), (1, 1, 'Ab4'), (2, 1, 'Bb4')], [(0, 3, 'G4')],
        [(0, 1.5, 'C5'), (1.5, 0.5, 'Ab4')], [], [(0, 1, 'F4'), (1, 1, 'Ab4'), (2, 1, 'Db5')], [(0, 2, 'C5')], [], [(1, 2, 'F4')], [(0, 3, 'E4')], []]
    flute = melody(tune, 3, vel=66)
    chimes = [(b * 3 + t, 1, P(n), 30) for b, t, n in [(0, 2, 'C6'), (2, 1.5, 'Ab5'), (5, 2.5, 'Eb6'), (8, 0.5, 'F6'), (9, 2, 'C6'), (12, 1, 'Ab5'), (13, 2.5, 'Bb5'), (15, 1, 'G5')]]
    return 60, [(1, 73, flute), (2, 33, low), (3, 48, strings), (4, 8, chimes)], len(chords) * 3

PIECES = {'orig_oak': oak, 'orig_lake': lake, 'orig_tower': tower, 'orig_burrow': burrow, 'orig_storm': storm}

if __name__ == '__main__':
    import hashlib, json
    src = os.path.join(ROOT, 'audio', 'sources.json'); sources = json.load(open(src, encoding='utf-8'))
    for name, fn in PIECES.items():
        bpm, parts, beats = fn(); path = os.path.join(ROOT, 'audio', 'midi', name + '.mid')
        write_mid(path, bpm, parts, beats)
        for t in sources['tracks']:   # sources.json 里的校验值跟着更新
            if t['id'] == name: t['sha256'] = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        print(f'{name}: {beats / bpm * 60:.1f} 秒，{sum(len(n) for _, _, n in parts)} 个音')
    with open(src, 'w', encoding='utf-8') as f: f.write(json.dumps(sources, ensure_ascii=False, indent=2) + '\n')
