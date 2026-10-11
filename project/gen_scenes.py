#!/usr/bin/env python3
"""Generate scene images for blockchain trust video, synced to BGM beats."""
from PIL import Image, ImageDraw, ImageFont
import json
import os

W, H = 1920, 1080
OUT = '/workspace/project/scenes'
os.makedirs(OUT, exist_ok=True)

# Load fonts
def get_font(size, bold=False):
    paths = [
        '/usr/share/fonts/truetype/noto/NotoSansSC-Bold.otf' if bold else '/usr/share/fonts/truetype/noto/NotoSansSC-Regular.otf',
        '/usr/share/fonts/opentype/noto/NotoSansSC-Bold.otf' if bold else '/usr/share/fonts/opentype/noto/NotoSansSC-Regular.otf',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    # fallback
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size)

font_title = get_font(72, bold=True)
font_sub = get_font(36)
font_year = get_font(180, bold=True)
font_concept = get_font(56, bold=True)
font_desc = get_font(34)
font_formula = get_font(42)
font_caption = get_font(30)

# Colors
BG_DARK = (5, 5, 16)
BG_GRAD = (18, 18, 42)
GOLD = (255, 215, 0)
CYAN = (0, 200, 255)
RED = (255, 68, 102)
WHITE = (241, 231, 216)
GRAY = (170, 170, 204)
DIM = (100, 100, 120)

def draw_gradient(draw, w, h, c1, c2):
    for y in range(h):
        r = int(c1[0] + (c2[0] - c1[0]) * y / h)
        g = int(c1[1] + (c2[1] - c1[1]) * y / h)
        b = int(c1[2] + (c2[2] - c1[2]) * y / h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def text_center(draw, text, font, y, color, max_w=W-200):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=font, fill=color)
    return bbox[3] - bbox[1]

def draw_multiline_center(draw, lines, font, y_start, color, line_h=None):
    y = y_start
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2
        draw.text((x, y), line, font=font, fill=color)
        y += line_h if line_h else (bbox[3] - bbox[1] + 10)

def make_scene(idx, draw_fn):
    img = Image.new('RGB', (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_fn(img, draw)
    img.save(f'{OUT}/scene_{idx:02d}.png')
    print(f'Saved scene_{idx:02d}.png')

# Scene 0: Opening Title
def s0(img, draw):
    draw_gradient(draw, W, H, BG_GRAD, BG_DARK)
    # glow circle
    for r in range(300, 0, -10):
        alpha = int(15 * (1 - r/300))
        draw.ellipse([W//2-r, H//2-r, W//2+r, H//2+r], fill=(alpha, alpha+10, alpha+20))
    draw_multiline_center(draw, ['区块链诞生前', '人类如何重建信任？'], font_title, H//2 - 120, GOLD, 90)
    draw_multiline_center(draw, ['没有密码学，就没有数字世界的身份证明'], font_sub, H//2 + 80, GRAY)

# Scene 1: 1976
def s1(img, draw):
    draw_gradient(draw, W, H, (10, 10, 26), (18, 18, 42))
    draw.text((W-450, 80), '1976', font=font_year, fill=(255,255,255,30) if False else (25, 25, 50))
    draw_multiline_center(draw, ['Diffie-Hellman 密钥交换'], font_concept, 200, GOLD)
    lines = ['Whitfield Diffie 和 Martin Hellman 发表', '《密码学新方向》', '首次提出公钥密码学——', '陌生人可以在公开信道上建立共享秘密']
    draw_multiline_center(draw, lines, font_desc, 320, WHITE, 50)

# Scene 2: Public Key
def s2(img, draw):
    draw_gradient(draw, W, H, (8, 8, 24), (12, 12, 32))
    draw.text((W-400, 80), 'PKC', font=font_year, fill=(20, 40, 60))
    draw_multiline_center(draw, ['非对称加密'], font_concept, 180, CYAN)
    # box
    draw.rounded_rectangle([360, 300, 1560, 680], radius=12, outline=(0, 200, 255), width=2, fill=(0, 20, 40))
    draw.text((460, 340), '公钥 加密 → 私钥 解密', font=font_formula, fill=GOLD)
    lines = ['每个人拥有两把钥匙', '公钥公开，私钥保密', '解决了"如何信任陌生人"的第一步']
    draw_multiline_center(draw, lines, font_desc, 430, WHITE, 45)

# Scene 3: RSA
def s3(img, draw):
    draw_gradient(draw, W, H, (10, 10, 26), (18, 18, 42))
    draw.text((W-400, 80), '1977', font=font_year, fill=(40, 30, 0))
    draw_multiline_center(draw, ['RSA 算法'], font_concept, 200, GOLD)
    lines = ['Rivest、Shamir、Adleman 提出', '第一个实用的公钥加密算法', '大整数分解的数学难题', '成为数字安全的基石']
    draw_multiline_center(draw, lines, font_desc, 320, WHITE, 50)

# Scene 4: Digital Signatures
def s4(img, draw):
    draw_gradient(draw, W, H, (8, 8, 24), (12, 12, 32))
    draw.text((W-350, 80), '签名', font=font_year, fill=(20, 40, 60))
    draw_multiline_center(draw, ['数字签名'], font_concept, 180, CYAN)
    draw.rounded_rectangle([360, 300, 1560, 680], radius=12, outline=(0, 200, 255), width=2, fill=(0, 20, 40))
    draw.text((460, 340), '私钥 签名 → 公钥 验证', font=font_formula, fill=RED)
    lines = ['证明了"这条消息确实来自你"', '不可伪造，不可抵赖', '数字世界有了身份证明']
    draw_multiline_center(draw, lines, font_desc, 430, WHITE, 45)

# Scene 5: Timestamps
def s5(img, draw):
    draw_gradient(draw, W, H, (10, 10, 26), (18, 18, 42))
    draw.text((W-450, 80), '1991', font=font_year, fill=(25, 50, 50))
    draw_multiline_center(draw, ['时间戳服务'], font_concept, 200, CYAN)
    lines = ['Haber & Stornetta 提出', '链式时间戳', '把数据哈希按时间顺序链接', '证明历史未被篡改']
    draw_multiline_center(draw, lines, font_desc, 320, WHITE, 50)

# Scene 6: Hash
def s6(img, draw):
    draw_gradient(draw, W, H, (8, 8, 24), (12, 12, 32))
    draw.text((W-450, 80), 'Hash', font=font_year, fill=(20, 40, 60))
    draw_multiline_center(draw, ['哈希函数'], font_concept, 180, CYAN)
    draw.rounded_rectangle([360, 300, 1560, 680], radius=12, outline=(0, 200, 255), width=2, fill=(0, 20, 40))
    draw.text((460, 340), 'SHA-256("信任") → e3b0c4...', font=font_formula, fill=GOLD)
    lines = ['任意输入 → 固定长度输出', '单向不可逆，碰撞极难', '为数据完整性提供数学保证']
    draw_multiline_center(draw, lines, font_desc, 430, WHITE, 45)

# Scene 7: Merkle Tree
def s7(img, draw):
    draw_gradient(draw, W, H, (8, 8, 24), (12, 12, 32))
    draw.text((W-400, 80), 'Merkle', font=font_year, fill=(20, 40, 60))
    draw_multiline_center(draw, ['默克尔树'], font_concept, 180, CYAN)
    draw.rounded_rectangle([360, 300, 1560, 680], radius=12, outline=(0, 200, 255), width=2, fill=(0, 20, 40))
    draw.text((460, 340), 'H(H(A)+H(B)) + H(H(C)+H(D))', font=font_formula, fill=GOLD)
    lines = ['将大量数据组织为树形哈希', '验证任意一片数据只需 O(log n)', '高效证明数据完整性']
    draw_multiline_center(draw, lines, font_desc, 430, WHITE, 45)

# Scene 8: Proof of Work
def s8(img, draw):
    draw_gradient(draw, W, H, (26, 10, 10), (42, 18, 18))
    draw.text((W-400, 80), '1992', font=font_year, fill=(50, 20, 20))
    draw_multiline_center(draw, ['工作量证明'], font_concept, 200, RED)
    lines = ['Dwork & Naor 提出', '计算成本作为信任基础', '让作弊变得不经济', '为后来的共识机制埋下伏笔']
    draw_multiline_center(draw, lines, font_desc, 320, WHITE, 50)

# Scene 9: 2008 Bitcoin
def s9(img, draw):
    draw_gradient(draw, W, H, BG_GRAD, BG_DARK)
    for r in range(300, 0, -10):
        alpha = int(15 * (1 - r/300))
        draw.ellipse([W//2-r, H//2-r-100, W//2+r, H//2+r-100], fill=(alpha, alpha+10, alpha+20))
    draw_multiline_center(draw, ['2008'], get_font(200, bold=True), 150, (40, 35, 0))
    draw_multiline_center(draw, ['中本聪发表比特币白皮书'], get_font(56, bold=True), 420, GOLD)
    lines = ['将公钥密码学、时间戳、哈希、默克尔树、工作量证明', '组合成第一个无需信任中介的电子现金系统']
    draw_multiline_center(draw, lines, font_sub, 520, GRAY, 50)

# Scene 10: Genesis Block
def s10(img, draw):
    draw_gradient(draw, W, H, (8, 8, 24), (12, 12, 32))
    draw.text((W-400, 80), 'Genesis', font=font_year, fill=(40, 30, 0))
    draw_multiline_center(draw, ['创世区块'], font_concept, 180, GOLD)
    draw.rounded_rectangle([360, 300, 1560, 720], radius=12, outline=(255, 215, 0), width=2, fill=(40, 30, 0))
    draw.text((460, 340), 'Block #0 ← previous: null', font=font_formula, fill=GOLD)
    lines = ['2009年1月3日', 'The Times 03/Jan/2009', 'Chancellor on brink of second bailout for banks', '第一条链上信息，铭刻在不可篡改的历史中']
    draw_multiline_center(draw, lines, font_desc, 430, WHITE, 45)

# Scene 11: Chain
def s11(img, draw):
    draw_gradient(draw, W, H, (8, 8, 24), (12, 12, 32))
    draw.text((W-350, 80), 'Chain', font=font_year, fill=(20, 40, 60))
    draw_multiline_center(draw, ['区块链'], font_concept, 180, CYAN)
    draw.rounded_rectangle([360, 300, 1560, 720], radius=12, outline=(0, 200, 255), width=2, fill=(0, 20, 40))
    draw.text((560, 340), 'Block₁ → Block₂ → Block₃ → ...', font=font_formula, fill=GOLD)
    draw.text((460, 400), '每个区块包含 前一个区块的哈希', font=get_font(32), fill=CYAN)
    lines = ['篡改任何一个区块', '将导致后续所有区块的哈希失效', '信任不再依赖中介，而是依赖数学']
    draw_multiline_center(draw, lines, font_desc, 470, WHITE, 45)

# Scene 12: Trust Redistributed
def s12(img, draw):
    draw_gradient(draw, W, H, (10, 10, 26), (18, 18, 42))
    draw_multiline_center(draw, ['TRUST'], get_font(120, bold=True), 100, (30, 30, 50))
    draw_multiline_center(draw, ['信任的重构'], font_concept, 280, GOLD)
    lines = ['从"信任某个机构"', '到"信任数学与代码"', '', '密码学证明了身份', '时间戳证明了历史', '工作量证明了诚实', '', '陌生人之间，终于可以相信彼此']
    draw_multiline_center(draw, lines, font_desc, 400, WHITE, 42)

# Scene 13: Conclusion
def s13(img, draw):
    draw_gradient(draw, W, H, BG_GRAD, BG_DARK)
    for r in range(300, 0, -10):
        alpha = int(15 * (1 - r/300))
        draw.ellipse([W//2-r, H//2-r, W//2+r, H//2+r], fill=(alpha, alpha+10, alpha+20))
    lines = ['从1976到2008', '三十二年，一群人', '重新定义了信任']
    draw_multiline_center(draw, lines, get_font(60, bold=True), 250, GOLD, 80)
    lines2 = ['没有密码学就没有数字身份', '没有时间戳就难以证明历史未被改写', '区块链不是凭空诞生——它是信任问题的最终答案']
    draw_multiline_center(draw, lines2, font_sub, 550, GRAY, 50)

# Scene 14: End
def s14(img, draw):
    draw_gradient(draw, W, H, BG_GRAD, BG_DARK)
    for r in range(300, 0, -10):
        alpha = int(15 * (1 - r/300))
        draw.ellipse([W//2-r, H//2-r, W//2+r, H//2+r], fill=(alpha, alpha+10, alpha+20))
    draw_multiline_center(draw, ['信任，由数学保证'], get_font(80, bold=True), H//2 - 50, GOLD)

scenes = [s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14]
for i, fn in enumerate(scenes):
    make_scene(i, fn)

print(f'\nGenerated {len(scenes)} scene images in {OUT}')
