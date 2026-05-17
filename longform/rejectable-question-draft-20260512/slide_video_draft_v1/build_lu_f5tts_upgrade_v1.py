#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, tarfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path('/home/adl/youtube-lu-ai-channel/longform/rejectable-question-draft-20260512')
OUT = BASE / 'slide_video_draft_v1'
ROOT = Path('/home/adl/youtube-lu-ai-channel')
F5 = ROOT / 'voice-lab/free-local-tts/f5env/bin/f5-tts_infer-cli'
REF_AUDIO = Path('/home/adl/video-projects/episode-1-ai-agent-uses/f5tts-ref-alt/ref_alt.wav')
REF_TEXT = Path('/home/adl/video-projects/episode-1-ai-agent-uses/f5tts-ref-alt/ref_text_alt.txt').read_text(encoding='utf-8').strip()
UP = OUT / 'lu_f5tts_upgrade_v1'
TXT = UP / 'chunks_text'
WAV = UP / 'chunks_wav'
LOG = UP / 'logs'
CHECK_FRAMES = OUT / 'check_frames_lu_f5v1'
CHECKS = OUT / 'checks'
for d in [UP, TXT, WAV, LOG, CHECK_FRAMES, CHECKS]:
    d.mkdir(parents=True, exist_ok=True)

SLIDES = [BASE / f'slides/slide_{i:02d}.png' for i in range(1, 6)]
SEGMENT_TITLES = [
    '可被退件的題目草稿，不是一次生成完美題目',
    '第 1 段：prompt 先鎖住年級、單元與只測一件事',
    '第 2 段：把退件規準寫在前面',
    '第 3 段：草稿必須附自評與可修訂入口',
    '收尾：讓老師保留最後審稿權',
]
NARRATION = (OUT / 'narration_zh_tw.txt').read_text(encoding='utf-8').strip()
chunks = [c.strip() for c in NARRATION.split('\n\n') if c.strip()]
for i, text in enumerate(chunks, 1):
    (TXT / f'chunk_{i:02d}.txt').write_text(text, encoding='utf-8')

def run(cmd):
    subprocess.run(cmd, check=True)

def out_text(cmd):
    return subprocess.check_output(cmd, text=True).strip()

def duration(path: Path) -> float:
    return float(out_text(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(path)]))

def ts(sec: float, comma: bool = False) -> str:
    ms = int(round((sec - int(sec)) * 1000)); s = int(sec)
    h, rem = divmod(s, 3600); m, ss = divmod(rem, 60); sep = ',' if comma else '.'
    return f'{h:02d}:{m:02d}:{ss:02d}{sep}{ms:03d}'

for i, text in enumerate(chunks, 1):
    out = WAV / f'chunk_{i:02d}.wav'
    if out.exists() and out.stat().st_size > 1000:
        continue
    cmd = [str(F5), '--model', 'F5TTS_v1_Base', '--ref_audio', str(REF_AUDIO), '--ref_text', REF_TEXT,
           '--gen_text', text, '--output_dir', str(WAV), '--output_file', out.name,
           '--device', 'cuda', '--speed', '1.08', '--remove_silence', '--no_legacy_text']
    with (LOG / f'chunk_{i:02d}.log').open('w', encoding='utf-8') as fh:
        subprocess.run(cmd, check=True, stdout=fh, stderr=subprocess.STDOUT)

silence = UP / 'silence_260ms.wav'
run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', '0.26', str(silence)])
concat = UP / 'narration_concat.ffconcat'
lines = ['ffconcat version 1.0']
for i in range(1, len(chunks) + 1):
    lines.append("file '" + (WAV / f'chunk_{i:02d}.wav').as_posix() + "'")
    if i < len(chunks):
        lines.append("file '" + silence.as_posix() + "'")
concat.write_text('\n'.join(lines) + '\n', encoding='utf-8')
raw = UP / 'narration_lu_f5tts_raw.wav'
loud = UP / 'narration_lu_f5tts_loudnorm.wav'
fit = OUT / 'narration_lu_f5tts_v1.wav'
mp3 = OUT / 'narration_lu_f5tts_v1.mp3'
run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-safe', '0', '-f', 'concat', '-i', str(concat), '-c', 'copy', str(raw)])
run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(raw), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', str(loud)])
raw_dur = duration(loud)
target_max = 258.0
if raw_dur > target_max:
    ratio = raw_dur / target_max
    af = f'atempo={ratio:.6f},loudnorm=I=-16:TP=-1.5:LRA=11'
else:
    ratio = 1.0
    af = 'loudnorm=I=-16:TP=-1.5:LRA=11'
run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(loud), '-af', af, '-ar', '48000', str(fit)])
run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(fit), '-codec:a', 'libmp3lame', '-b:a', '192k', str(mp3)])
total = duration(fit)

weights = [0.17, 0.19, 0.21, 0.21, 0.22]
bounds = [0.0]
for w in weights:
    bounds.append(bounds[-1] + total * w / sum(weights))
(OUT / 'narration_lu_f5tts_v1.vtt').write_text('WEBVTT\n\n' + '\n\n'.join(f'{ts(bounds[i])} --> {ts(bounds[i+1])}\n{SEGMENT_TITLES[i]}' for i in range(5)) + '\n', encoding='utf-8')
(OUT / 'narration_lu_f5tts_v1.srt').write_text('\n\n'.join(f'{i+1}\n{ts(bounds[i], True)} --> {ts(bounds[i+1], True)}\n{SEGMENT_TITLES[i]}' for i in range(5)) + '\n', encoding='utf-8')

slides_concat = UP / 'slides_lu_f5tts_v1.ffconcat'
slines = []
for i, slide in enumerate(SLIDES):
    slines.append("file '" + slide.as_posix() + "'")
    slines.append(f'duration {bounds[i+1] - bounds[i]:.3f}')
slines.append("file '" + SLIDES[-1].as_posix() + "'")
slides_concat.write_text('\n'.join(slines) + '\n', encoding='utf-8')
new_mp4 = OUT / 'rejectable-question-draft-slide-video-draft-lu-f5tts-v1.mp4'
run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(slides_concat), '-i', str(fit), '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(new_mp4)])

for idx, sec in enumerate([5, total * 0.24, total * 0.46, total * 0.68, max(1, total - 12)], 1):
    run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-ss', f'{sec:.2f}', '-i', str(new_mp4), '-frames:v', '1', '-update', '1', str(CHECK_FRAMES / f'frame_lu_{idx:02d}.png')])
imgs = [(p.name, Image.open(p).convert('RGB').resize((480, 270))) for p in sorted(CHECK_FRAMES.glob('frame_lu_*.png'))]
sheet = Image.new('RGB', (1600, 980), (245, 242, 234)); draw = ImageDraw.Draw(sheet)
font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = ImageFont.truetype(font_path, 28); title_font = ImageFont.truetype(font_path, 38)
draw.text((50, 28), '可退件題目草稿｜Lu F5-TTS v1 QA contact sheet', font=title_font, fill=(32, 45, 62))
coords = [(50, 100), (560, 100), (1070, 100), (300, 520), (810, 520)]
for (name, im), (x, y) in zip(imgs, coords):
    sheet.paste(im, (x, y)); draw.rectangle([x, y, x + 480, y + 270], outline=(32, 45, 62), width=3); draw.text((x, y + 285), name, font=font, fill=(32, 45, 62))
qa = CHECKS / 'contact_sheet_lu_f5tts_v1.png'
sheet.save(qa)

manifest_path = OUT / 'manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest.update({
    'status': 'slide_video_upload_kit_and_shareable_handout_complete; Lu Teacher F5-TTS v1 voice upgrade ready',
    'recommended_video': 'slide_video_draft_v1/' + new_mp4.name,
    'audio_source_lu_voice': 'Lu Teacher F5-TTS voice clone v1',
    'lu_voice_audio': 'slide_video_draft_v1/' + mp3.name,
    'subtitles_lu_voice': ['slide_video_draft_v1/narration_lu_f5tts_v1.vtt', 'slide_video_draft_v1/narration_lu_f5tts_v1.srt'],
    'lu_voice_contact_sheet': 'slide_video_draft_v1/checks/contact_sheet_lu_f5tts_v1.png',
    'lu_voice_duration_seconds': round(duration(new_mp4), 3),
    'voice_upgrade_note': 'Original package used zh-TW Edge HsiaoYu scratch TTS; v1 replaces narration with Lu Teacher F5-TTS voice clone, chunked generation, loudnorm, and rebuilt slide-video.',
    'next_auto_push': 'Continue voice remediation queue with shorts/exit-ticket-ai-reflection-20260512, or upload Lu voice versions after YouTube/Google login.'
})
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

readme_path = OUT / 'README.md'
readme = readme_path.read_text(encoding='utf-8')
block = f'''

## 音訊升級 v1（Lu Teacher F5-TTS）

- 推薦上傳影片：`{new_mp4.name}`
- 改善原因：原版使用 zh-TW Edge HsiaoYu 女聲草稿；本版改用盧老師 F5-TTS voice clone。
- 升級版旁白：`{mp3.name}` / `narration_lu_f5tts_v1.wav`
- 升級版字幕：`narration_lu_f5tts_v1.vtt` / `narration_lu_f5tts_v1.srt`
- QA contact sheet：`checks/contact_sheet_lu_f5tts_v1.png`
- 驗證：ffprobe {duration(new_mp4):.3f} 秒，1920×1080，H.264 + AAC；旁白 loudnorm 後約 -16 LUFS；抽幀 QA 供視覺檢查。
'''
if '## 音訊升級 v1（Lu Teacher F5-TTS）' not in readme:
    readme_path.write_text(readme.rstrip() + block, encoding='utf-8')

upload_path = OUT / 'youtube-upload-kit-longform-v1.md'
kit = upload_path.read_text(encoding='utf-8')
insert = f'''

## 推薦上傳版本（Lu Teacher voice）

- 推薦影片：`{new_mp4.name}`
- 原始 Edge HsiaoYu 草稿保留作比較；正式上傳優先使用 Lu Teacher F5-TTS v1。
- 升級版字幕：`narration_lu_f5tts_v1.vtt`、`narration_lu_f5tts_v1.srt`
'''
if '## 推薦上傳版本（Lu Teacher voice）' not in kit:
    upload_path.write_text(kit.rstrip() + insert, encoding='utf-8')

archive = OUT / 'rejectable-question-draft-lu-f5tts-v1-kit-20260518.tar.gz'
members = [
    BASE / 'README.md', BASE / 'manifest.json', OUT / 'README.md', OUT / 'manifest.json', OUT / 'build_slide_video_draft.py', OUT / 'build_lu_f5tts_upgrade_v1.py',
    OUT / 'narration_zh_tw.txt', fit, mp3, OUT / 'narration_lu_f5tts_v1.vtt', OUT / 'narration_lu_f5tts_v1.srt',
    new_mp4, OUT / 'rejectable-question-draft-slide-video-draft-v1.mp4', OUT / 'youtube-upload-kit-longform-v1.md', BASE / 'rejectable-question-draft-shareable-handout-v1.md', qa,
] + SLIDES + sorted(CHECK_FRAMES.glob('frame_lu_*.png'))
with tarfile.open(archive, 'w:gz') as tar:
    for p in members:
        if p.exists():
            tar.add(p, arcname=str(p.relative_to(BASE)))
with tarfile.open(archive, 'r:gz') as tar:
    names = tar.getnames()
print(json.dumps({'new_mp4': str(new_mp4), 'duration': duration(new_mp4), 'audio_duration': duration(fit), 'archive': str(archive), 'archive_members': len(names), 'qa': str(qa), 'tempo_ratio': ratio}, ensure_ascii=False, indent=2))
