#!/usr/bin/env python3
"""Generate all video frames synced to BGM beats, then ffmpeg combines with audio."""
from PIL import Image, ImageDraw, ImageFont
import json, os, math

W, H = 1920, 1080
FPS = 30
OUT = '/workspace/project/frames'
os.makedirs(OUT, exist_ok=True)

# Load beats
with open('/workspace/project/evidence/beats.json') as f:
    beat_data = json.load(f)

BEATS = beat_data['beat_times']
STRONG_ONSETS = [o['time'] for o in beat_data['top_onsets']]
DURATION = beat_data['duration']

# Scene definitions with timing
SCENES = [
    {"start": 0, "img": "scene_00.png", "caption": "区块链诞生前，人类花了几十年解决「信任」"},
    {"start": 4.679, "img": "scene_01.png", "caption": "1976年 · Diffie-Hellman 密钥交换"},
    {"start": 9.462, "img": "scene_02.png", "caption": "公钥密码学 · 非对称加密"},
    {"start": 14.791, "img": "scene_03.png", "caption": "1977年 · RSA 算法"},
    {"start": 20.097, "img": "scene_04.png", "caption": "数字签名 · 身份证明"},
    {"start": 25.414, "img": "scene_05.png", "caption": "1991年 · 时间戳服务"},
    {"start": 30.732, "img": "scene_06.png", "caption": "哈希函数 · 数据完整性"},
    {"start": 36.049, "img": "scene_07.png", "caption": "默克尔树 · 高效验证"},
    {"start": 41.355, "img": "scene_08.png", "caption": "1992年 · 工作量证明"},
    {"start": 46.672, "img": "scene_09.png", "caption": "2008年 · 比特币白皮书"},
    {"start": 53.046, "img": "scene_10.png", "caption": "2009年 · 创世区块"},
    {"start": 62.613, "img": "scene_11.png", "caption": "区块链 · 信任由数学保证"},
    {"start": 79.61, "img": "scene_12.png", "caption": "信任的重构 · 从中介到数学"},
    {"start": 96.63, "img": "scene_13.png", "caption": "三十二年 · 重新定义信任"},
    {"start": 143.383, "img": "scene_14.png", "caption": "信任，由数学保证"},
]

# Preload scene images
scene_imgs = {}
for s in SCENES:
    img = Image.open(f'/workspace/project/scenes/{s["img"]}').convert('RGB')
    scene_imgs[s["img"]] = img

# Caption font
def get_font(size, bold=False):
    paths = [
        '/usr/share/fonts/truetype/noto/NotoSansSC-Bold.otf' if bold else '/usr/share/fonts/truetype/noto/NotoSansSC-Regular.otf',
        '/usr/share/fonts/opentype/noto/NotoSansSC-Bold.otf' if bold else '/usr/share/fonts/opentype/noto/NotoSansSC-Regular.otf',
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size)

font_caption = get_font(30)
font_progress = get_font(20)

def get_scene(t):
    """Get current scene for time t."""
    current = SCENES[0]
    for s in SCENES:
        if t >= s["start"]:
            current = s
    return current

def get_scene_idx(t):
    idx = 0
    for i, s in enumerate(SCENES):
        if t >= s["start"]:
            idx = i
    return idx

def is_flash(t):
    """Check if there's a flash at time t."""
    for onset in STRONG_ONSETS:
        if onset <= t <= onset + 0.15:
            return True
    return False

def get_flash_intensity(t):
    """Get flash intensity 0-255."""
    for onset in STRONG_ONSETS:
        if onset <= t <= onset + 0.15:
            # Fade out over 0.15s
            progress = (t - onset) / 0.15
            return int(40 * (1 - progress))
    return 0

def get_transition_alpha(t):
    """Get alpha for crossfade at scene start (0-1, 0=old, 1=new)."""
    idx = get_scene_idx(t)
    scene = SCENES[idx]
    time_in_scene = t - scene["start"]
    if time_in_scene < 0.3 and idx > 0:
        # Fading in
        return time_in_scene / 0.3
    return 1.0

total_frames = int(DURATION * FPS)
print(f"Generating {total_frames} frames at {FPS}fps...")

for frame_num in range(total_frames):
    t = frame_num / FPS

    # Get current scene
    idx = get_scene_idx(t)
    scene = SCENES[idx]
    base_img = scene_imgs[scene["img"]].copy()
    draw = ImageDraw.Draw(base_img, 'RGBA')

    # Crossfade: if at scene start, blend with previous scene
    alpha = get_transition_alpha(t)
    if alpha < 1.0 and idx > 0:
        prev_scene = SCENES[idx - 1]
        prev_img = scene_imgs[prev_scene["img"]].copy()
        # Blend
        blended = Image.blend(prev_img, base_img, alpha)
        base_img = blended
        draw = ImageDraw.Draw(base_img, 'RGBA')

    # Flash effect
    flash_intensity = get_flash_intensity(t)
    if flash_intensity > 0:
        flash_overlay = Image.new('RGBA', (W, H), (255, 215, 0, flash_intensity))
        base_img = Image.alpha_composite(base_img.convert('RGBA'), flash_overlay).convert('RGB')
        draw = ImageDraw.Draw(base_img, 'RGBA')

    # Beat pulse (subtle brightness boost every 4th beat)
    # Check if near a beat
    for beat_t in BEATS:
        if beat_t <= t <= beat_t + 0.08:
            beat_idx = BEATS.index(beat_t)
            if beat_idx % 4 == 0:  # Quarter note pulse
                pulse = Image.new('RGBA', (W, H), (255, 255, 255, 8))
                base_img = Image.alpha_composite(base_img.convert('RGBA'), pulse).convert('RGB')
                draw = ImageDraw.Draw(base_img, 'RGBA')
            break

    # Caption bar
    caption = scene["caption"]
    if caption:
        # Semi-transparent bar at bottom
        bar_h = 60
        bar = Image.new('RGBA', (W, bar_h), (0, 0, 0, 180))
        base_img.paste(bar, (0, H - bar_h - 20), bar)
        draw = ImageDraw.Draw(base_img, 'RGBA')
        # Caption text
        bbox = draw.textbbox((0, 0), caption, font=font_caption)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2
        draw.text((x, H - bar_h - 15), caption, font=font_caption, fill=(255, 255, 255, 255))

    # Progress bar
    progress = t / DURATION
    draw.rectangle([0, H - 4, int(W * progress), H], fill=(255, 215, 0))

    # Save frame
    base_img.save(f'{OUT}/frame_{frame_num:05d}.png', format='PNG', optimize=False)

    if frame_num % 300 == 0:
        print(f"  Frame {frame_num}/{total_frames} ({t:.1f}s)")

print(f"\nDone! Generated {total_frames} frames in {OUT}")
