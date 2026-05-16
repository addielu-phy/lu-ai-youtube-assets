#!/usr/bin/env python3
from pathlib import Path
import subprocess, json, tarfile
from PIL import Image, ImageDraw, ImageFont

PKG = Path('/home/adl/youtube-lu-ai-channel/shorts/remedial-double-lock-20260513')
F5 = Path('/home/adl/youtube-lu-ai-channel/voice-lab/free-local-tts/f5env/bin/f5-tts_infer-cli')
REF_AUDIO = Path('/home/adl/video-projects/episode-1-ai-agent-uses/f5tts-ref-alt/ref_alt.wav')
REF_TEXT = Path('/home/adl/video-projects/episode-1-ai-agent-uses/f5tts-ref-alt/ref_text_alt.txt').read_text(encoding='utf-8').strip()
BASE = PKG / 'lu_f5tts_upgrade_v1'
TXT = BASE / 'chunks_text'
WAV = BASE / 'chunks_wav'
LOG = BASE / 'logs'
CHECKS = PKG / 'checks'
for d in [TXT, WAV, LOG, CHECKS]:
    d.mkdir(parents=True, exist_ok=True)

chunks = [
    '補救教學不是把題目變簡單，而是對準錯因。',
    '請 AI 幫忙出補救題前，我會先鎖住兩件事。',
    '第一鎖，是錯因：學生到底是概念想錯、步驟亂掉，還是圖文公式對不起來？',
    '第二鎖，是難度階梯：先做辨認題，再做半引導題，最後才做獨立題。',
    '如果 AI 直接生出一整串漂亮題目，就請它說明每一題對應哪個錯因、位在哪一層階梯。補救不是題海，是有方向的再練一次。',
]
for i, text in enumerate(chunks, 1):
    (TXT / f'chunk_{i:02d}.txt').write_text(text, encoding='utf-8')

for i, text in enumerate(chunks, 1):
    out = WAV / f'chunk_{i:02d}.wav'
    if out.exists() and out.stat().st_size > 1000:
        continue
    cmd = [str(F5), '--model', 'F5TTS_v1_Base', '--ref_audio', str(REF_AUDIO), '--ref_text', REF_TEXT,
           '--gen_text', text, '--output_dir', str(WAV), '--output_file', out.name,
           '--device', 'cuda', '--speed', '1.08', '--remove_silence', '--no_legacy_text']
    with (LOG / f'chunk_{i:02d}.log').open('w', encoding='utf-8') as fh:
        subprocess.run(cmd, check=True, stdout=fh, stderr=subprocess.STDOUT)

silence = BASE / 'silence_220ms.wav'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','lavfi','-i','anullsrc=r=24000:cl=mono','-t','0.22',str(silence)], check=True)
concat = BASE / 'narration_concat.ffconcat'
lines = ['ffconcat version 1.0']
for i in range(1, len(chunks)+1):
    lines.append(f"file '{(WAV/f'chunk_{i:02d}.wav').as_posix()}'")
    if i < len(chunks):
        lines.append(f"file '{silence.as_posix()}'")
concat.write_text('\n'.join(lines)+'\n', encoding='utf-8')
raw = BASE / 'narration_lu_f5tts_raw.wav'
loud = BASE / 'narration_lu_f5tts_loudnorm.wav'
fit = PKG / 'narration_35s_lu_f5tts_v1.wav'
mp3 = PKG / 'narration_35s_lu_f5tts_v1.mp3'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-safe','0','-f','concat','-i',str(concat),'-c','copy',str(raw)], check=True)
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(raw),'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000',str(loud)], check=True)

def duration(p: Path) -> float:
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)], text=True).strip())

dur = duration(loud)
if dur > 34.85:
    ratio = dur / 34.75
    af = f'atempo={ratio:.6f},apad,loudnorm=I=-16:TP=-1.5:LRA=11'
else:
    ratio = 1.0
    af = 'apad,loudnorm=I=-16:TP=-1.5:LRA=11'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(loud),'-t','35.000','-af',af,'-ar','48000',str(fit)], check=True)
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(fit),'-codec:a','libmp3lame','-b:a','192k',str(mp3)], check=True)

old_mp4 = PKG / 'remedial-double-lock-shorts-35s.mp4'
new_mp4 = PKG / 'remedial-double-lock-shorts-35s-lu-f5tts-v1.mp4'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(old_mp4),'-i',str(fit),'-map','0:v:0','-map','1:a:0','-t','35.000','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(new_mp4)], check=True)

segments = [
    (0.0, 5.2, '補救不是把題目變簡單，而是對準錯因。'),
    (5.2, 10.0, '請 AI 出補救題前，先鎖住兩件事。'),
    (10.0, 18.0, '第一鎖：錯因，是概念、步驟，還是圖文公式對不起來？'),
    (18.0, 26.2, '第二鎖：難度階梯，辨認、半引導、最後才獨立題。'),
    (26.2, 35.0, '請 AI 標註每題對應錯因與階梯；補救不是題海。'),
]
def ts(sec, comma=False):
    h = int(sec // 3600); m = int((sec % 3600) // 60); s = int(sec % 60); ms = int(round((sec - int(sec)) * 1000))
    return f'{h:02d}:{m:02d}:{s:02d}{"," if comma else "."}{ms:03d}'
(PKG/'narration_35s_lu_f5tts_v1.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{ts(a)} --> {ts(b)}\n{text}' for a,b,text in segments)+'\n', encoding='utf-8')
(PKG/'narration_35s_lu_f5tts_v1.srt').write_text('\n\n'.join(f'{i}\n{ts(a, True)} --> {ts(b, True)}\n{text}' for i,(a,b,text) in enumerate(segments,1))+'\n', encoding='utf-8')

frame_names = []
for name, sec in [('frame_early_lu_f5v1.png','2.0'),('frame_mid_lu_f5v1.png','17.0'),('frame_late_lu_f5v1.png','32.0')]:
    out = CHECKS / name
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',sec,'-i',str(new_mp4),'-frames:v','1','-update','1',str(out)], check=True)
    frame_names.append(name)
imgs = [Image.open(PKG/'cover_remedial_double_lock_v1.png').convert('RGB')] + [Image.open(CHECKS/n).convert('RGB') for n in frame_names]
thumb_w, thumb_h = 270, 480
font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = ImageFont.truetype(font_path, 26)
sheet = Image.new('RGB', (thumb_w*2 + 60, (thumb_h+70)*2 + 40), '#111827')
draw = ImageDraw.Draw(sheet)
labels = ['cover','2s','17s','32s']
for idx, img in enumerate(imgs):
    img.thumbnail((thumb_w, thumb_h))
    x = 20 + (idx % 2) * (thumb_w + 20)
    y = 20 + (idx // 2) * (thumb_h + 70)
    sheet.paste(img, (x, y))
    draw.text((x, y + thumb_h + 8), labels[idx], fill='#e5e7eb', font=font)
sheet.save(CHECKS/'qa_lu_f5v1_sheet.png')

manifest = json.loads((PKG/'manifest.json').read_text(encoding='utf-8'))
manifest.update({
    'status': '35s Shorts MP4/upload kit/teacher checklist complete; Lu Teacher F5-TTS v1 voice upgrade ready',
    'mp4_lu_voice': new_mp4.name,
    'audio_source': 'Lu Teacher F5-TTS voice clone v1',
    'narration_lu_voice': mp3.name,
    'subtitles_lu_voice': ['narration_35s_lu_f5tts_v1.vtt','narration_35s_lu_f5tts_v1.srt'],
    'voice_upgrade_note': 'Original package used zh-TW Edge HsiaoYu scratch TTS; v1 replaces audio with Lu Teacher F5-TTS voice clone, chunked generation, loudnorm, fitted to 35s.',
    'recommended_video': new_mp4.name,
    'next_auto_push': 'publish/upload the Lu Teacher voice version if YouTube login is ready; otherwise continue one-by-one voice remediation for the next queue item',
})
(PKG/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
readme = (PKG/'README.md').read_text(encoding='utf-8')
append = f'''

## 音訊升級 v1（Lu Teacher F5-TTS）

- 改善原因：原版使用 zh-TW Edge HsiaoYu 女聲草稿；本版改用盧老師 F5-TTS voice clone。
- 推薦版 MP4：`{new_mp4.name}`
- 升級版旁白：`{mp3.name}` / `{fit.name}`
- 升級版字幕：`narration_35s_lu_f5tts_v1.vtt` / `narration_35s_lu_f5tts_v1.srt`
- QA sheet：`checks/qa_lu_f5v1_sheet.png`
- 音訊處理：F5-TTS chunked generation、0.22 秒短停頓、loudnorm I=-16、AAC 192k、35 秒完整輸出。
'''
if '## 音訊升級 v1（Lu Teacher F5-TTS）' not in readme:
    (PKG/'README.md').write_text(readme.rstrip() + append + '\n', encoding='utf-8')
upload = (PKG/'youtube-upload-kit.md').read_text(encoding='utf-8')
if new_mp4.name not in upload:
    insert = f'\n## 推薦上傳版本（Lu Teacher voice）\n\n- 推薦影片：`{new_mp4.name}`\n- 原始 Edge HsiaoYu 草稿保留作比較；正式上傳優先使用 Lu Teacher F5-TTS v1。\n- 升級版字幕：`narration_35s_lu_f5tts_v1.vtt`、`narration_35s_lu_f5tts_v1.srt`\n'
    (PKG/'youtube-upload-kit.md').write_text(upload.rstrip() + insert + '\n', encoding='utf-8')
archive = PKG / 'remedial-double-lock-lu-f5tts-v1-kit-20260516.tar.gz'
members = ['README.md','manifest.json','build_lu_f5tts_upgrade_v1.py','youtube-upload-kit.md','remedial-double-lock-teacher-checklist-v1.md',new_mp4.name,'remedial-double-lock-shorts-35s.mp4','cover_remedial_double_lock_v1.png','narration_35s.txt',mp3.name,fit.name,'narration_35s_lu_f5tts_v1.vtt','narration_35s_lu_f5tts_v1.srt','narration_35s_edge_hsiaoyu.mp3','narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt','checks/qa_lu_f5v1_sheet.png','checks/frame_early_lu_f5v1.png','checks/frame_mid_lu_f5v1.png','checks/frame_late_lu_f5v1.png','checks/qa_sheet_mp4.png']
with tarfile.open(archive, 'w:gz') as tar:
    for rel in members:
        p = PKG / rel
        if p.exists():
            tar.add(p, arcname=f'remedial-double-lock-20260513/{rel}')
    for p in sorted((PKG/'slides').glob('slide_*.png')):
        tar.add(p, arcname=f'remedial-double-lock-20260513/slides/{p.name}')
with tarfile.open(archive, 'r:gz') as tar:
    names = tar.getnames()
    assert any(new_mp4.name in n for n in names)
    assert any('qa_lu_f5v1_sheet.png' in n for n in names)
    assert any('README.md' in n for n in names)
probe = subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=index,codec_type,codec_name,width,height,r_frame_rate','-show_entries','format=duration,size','-of','json',str(new_mp4)], text=True)
vol = subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(fit),'-af','volumedetect','-f','null','-'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
info = {
    'raw_audio_duration': duration(raw),
    'loud_audio_duration': dur,
    'tempo_ratio_if_used': ratio,
    'final_audio_duration': duration(fit),
    'new_mp4_duration': duration(new_mp4),
    'new_mp4': str(new_mp4),
    'mp3': str(mp3),
    'archive': str(archive),
    'archive_members': len(names),
    'probe': json.loads(probe),
    'volumedetect_tail': '\n'.join(vol.splitlines()[-6:]),
}
print(json.dumps(info, ensure_ascii=False, indent=2))
