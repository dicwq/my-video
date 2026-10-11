#!/usr/bin/env python3
"""Generate ffmpeg concat file with beat-synced scene durations and flash effects."""
import json

# Scene timing (from beats.json - scenes change on specific beats)
scenes = [
    {"file": "scene_00.png", "duration": 4.679},   # 0-4.679: Opening
    {"file": "scene_01.png", "duration": 4.783},   # 4.679-9.462: 1976 Diffie-Hellman
    {"file": "scene_02.png", "duration": 5.329},   # 9.462-14.791: Public Key
    {"file": "scene_03.png", "duration": 5.306},   # 14.791-20.097: RSA
    {"file": "scene_04.png", "duration": 5.317},   # 20.097-25.414: Digital Signatures
    {"file": "scene_05.png", "duration": 5.318},   # 25.414-30.732: Timestamps
    {"file": "scene_06.png", "duration": 5.317},   # 30.732-36.049: Hash
    {"file": "scene_07.png", "duration": 5.306},   # 36.049-41.355: Merkle Tree
    {"file": "scene_08.png", "duration": 5.317},   # 41.355-46.672: Proof of Work
    {"file": "scene_09.png", "duration": 6.374},   # 46.672-53.046: 2008 Bitcoin
    {"file": "scene_10.png", "duration": 9.567},   # 53.046-62.613: Genesis Block
    {"file": "scene_11.png", "duration": 16.997},  # 62.613-79.61: Chain
    {"file": "scene_12.png", "duration": 17.02},   # 79.61-96.63: Trust Redistributed
    {"file": "scene_13.png", "duration": 46.753},  # 96.63-143.383: Conclusion
    {"file": "scene_14.png", "duration": 2.617},   # 143.383-146.0: End
]

total = sum(s["duration"] for s in scenes)
print(f"Total duration: {total:.3f}s (target: 146.0s)")

# Write concat file for ffmpeg
with open('/workspace/project/scenes/concat.txt', 'w') as f:
    for s in scenes:
        f.write(f"file '{s['file']}'\n")
        f.write(f"duration {s['duration']:.3f}\n")
    # Last file needs to be repeated (ffmpeg concat quirk)
    f.write(f"file '{scenes[-1]['file']}'\n")

# Strong onset times for flash effects
strong_onsets = [0.035,3.088,4.679,5.213,7.338,9.462,20.097,25.414,30.732,31.521,31.788,32.055,36.049,38.963,41.355,43.212,45.604,46.672,53.046,62.88,62.613,66.862,74.304,79.61,80.678,81.734,83.859,96.63,108.042,108.309,119.734,120.535,122.125,129.567,130.101,138.6,139.134,139.401,143.383]

# Build enable expression for brightness flash on strong onsets
# Each flash lasts 0.15s
flash_expr_parts = []
for t in strong_onsets:
    flash_expr_parts.append(f"between(t,{t:.3f},{t+0.15:.3f})")
flash_expr = "+".join(flash_expr_parts)

# Write the ffmpeg filter script
# We use: image2 demuxer with concat, then colorchannelmixer for flash, then add audio
filter_complex = f"""
[0:v]fps=30,setpts=PTS-STARTPTS,scale=1920:1080[v0];
colorchannelmixer@flash=1.0:1.0:1.0:0.0:1.0:1.0:1.0:0.0:1.0:1.0:1.0:0.0:0.0:0.0:0.0:0.0[base];
[base][v0]overlay=0:0[outv];
colorchannelmixer@bright=1.0:0.0:0.0:0.0:0.0:1.0:0.0:0.0:0.0:0.0:1.0:0.0:0.0:0.0:0.0:1.0[bright];
[outv][bright]blend=all_mode=screen:all_opacity=1.0:enable='{flash_expr}'[flashv]
"""

# Actually, let's use a simpler approach with eq filter for brightness flashes
print(f"\nStrong onset count: {len(strong_onsets)}")
print(f"Flash expression length: {len(flash_expr)} chars")

# Save onset data for reference
with open('/workspace/project/evidence/flash_data.json', 'w') as f:
    json.dump({"strong_onsets": strong_onsets, "flash_expr": flash_expr[:200] + "..."}, f, indent=2)

print("Data saved. Ready for ffmpeg render.")
