#!/usr/bin/env python3
from pathlib import Path
import subprocess, json, tarfile, shutil

PKG = Path('/home/adl/youtube-lu-ai-channel/shorts/parent-message-draft-only-20260515')
PAGES_ROOTS = [
    Path('/home/adl/pages/lu-ai-youtube-assets/shorts/parent-message-draft-only-20260515'),
    Path('/home/adl/lu-ai-youtube-assets-pages/shorts/parent-message-draft-only-20260515'),
]
F5 = Path('/home/adl/youtube-lu-ai-channel/voice-lab/free-local-tts/f5env/bin/f5-tts_infer-cli')
REF_AUDIO = Path('/home/adl/video-projects/episode-1-ai-agent-uses/f5tts-ref-alt/ref_alt.wav')
REF_TEXT = Path('/home/adl/video-projects/episode-1-ai-agent-uses/f5tts-ref-alt/ref_text_alt.txt').read_text(encoding='utf-8').strip()
BASE = PKG / 'lu_f5tts_upgrade_v1'
TXT = BASE / 'chunks_text'
WAV = BASE / 'chunks_wav'
LOG = BASE / 'logs'
for d in [TXT, WAV, LOG, PKG / 'checks']:
    d.mkdir(parents=True, exist_ok=True)

chunks = [
    'AI 可以幫老師寫家長訊息，但第一版只能當草稿。',
    '送出前，先過三關。第一關：事實有沒有確認？',
    '第二關：語氣是不是從指責，改成一起解決問題？',
    '第三關：有沒有拿掉學生個資、病況，或可被回推出來的細節？',
    '最後請 AI 幫你把訊息退件一次；能通過三關，才交給老師本人送出。',
]
for i, text in enumerate(chunks, 1):
    (TXT / f'chunk_{i:02d}.txt').write_text(text, encoding='utf-8')

for i, text in enumerate(chunks, 1):
    out = WAV / f'chunk_{i:02d}.wav'
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

old_mp4 = PKG / 'parent-message-draft-only-shorts-35s.mp4'
new_mp4 = PKG / 'parent-message-draft-only-shorts-35s-lu-f5tts-v1.mp4'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(old_mp4),'-i',str(fit),'-map','0:v:0','-map','1:a:0','-t','35.000','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(new_mp4)], check=True)

segments = [
    (0.0, 5.8, 'AI 可起草家長訊息，但第一版只能當草稿。'),
    (5.8, 12.3, '第一關：事實有沒有確認？'),
    (12.3, 19.0, '第二關：語氣是不是改成一起解決問題？'),
    (19.0, 27.5, '第三關：拿掉個資與可回推細節。'),
    (27.5, 35.0, '通過三關，才交給老師本人送出。'),
]
def ts(sec, comma=False):
    h = int(sec // 3600); m = int((sec % 3600) // 60); s = int(sec % 60); ms = int(round((sec - int(sec)) * 1000))
    return f'{h:02d}:{m:02d}:{s:02d}{"," if comma else "."}{ms:03d}'
(PKG/'narration_35s_lu_f5tts_v1.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{ts(a)} --> {ts(b)}\n{text}' for a,b,text in segments)+'\n', encoding='utf-8')
(PKG/'narration_35s_lu_f5tts_v1.srt').write_text('\n\n'.join(f'{i}\n{ts(a, True)} --> {ts(b, True)}\n{text}' for i,(a,b,text) in enumerate(segments,1))+'\n', encoding='utf-8')

for name, sec in [('frame_early_lu_f5v1.png','2.0'),('frame_mid_lu_f5v1.png','17.0'),('frame_late_lu_f5v1.png','32.0')]:
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',sec,'-i',str(new_mp4),'-frames:v','1','-update','1',str(PKG/'checks'/name)], check=True)

manifest = json.loads((PKG/'manifest.json').read_text(encoding='utf-8'))
manifest.update({
    'status': '35s Shorts MP4/upload kit complete; Lu Teacher F5-TTS v1 voice upgrade ready',
    'mp4_lu_voice': new_mp4.name,
    'audio_source': 'Lu Teacher F5-TTS voice clone v1',
    'narration_lu_voice': mp3.name,
    'subtitles_lu_voice': ['narration_35s_lu_f5tts_v1.vtt','narration_35s_lu_f5tts_v1.srt'],
    'voice_upgrade_note': 'Original package used zh-TW-YunJheNeural male scratch TTS; v1 replaces audio with Lu Teacher F5-TTS voice clone, chunked generation, loudnorm, fitted to 35s.',
    'recommended_video': new_mp4.name,
    'next_auto_push': 'publish/upload the Lu Teacher voice version if YouTube login is ready; otherwise continue one-by-one voice remediation for the next queue item',
})
(PKG/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
readme = (PKG/'README.md').read_text(encoding='utf-8')
append = f'''

## 音訊升級 v1（Lu Teacher F5-TTS）

- 改善原因：原版使用 zh-TW YunJhe 男聲草稿；本版改用盧老師 F5-TTS voice clone。
- 推薦版 MP4：`{new_mp4.name}`
- 升級版旁白：`{mp3.name}` / `{fit.name}`
- 升級版字幕：`narration_35s_lu_f5tts_v1.vtt` / `narration_35s_lu_f5tts_v1.srt`
- 音訊處理：F5-TTS chunked generation、0.22 秒短停頓、loudnorm I=-16、AAC 192k、35 秒完整輸出。
'''
if '## 音訊升級 v1（Lu Teacher F5-TTS）' not in readme:
    (PKG/'README.md').write_text(readme.rstrip() + append + '\n', encoding='utf-8')

upload = (PKG/'youtube-upload-kit.md').read_text(encoding='utf-8')
if 'parent-message-draft-only-shorts-35s-lu-f5tts-v1.mp4' not in upload:
    insert = '\n## 推薦上傳版本（Lu Teacher voice）\n\n- 推薦影片：`parent-message-draft-only-shorts-35s-lu-f5tts-v1.mp4`\n- 原始男聲草稿保留作比較；正式上傳優先使用 Lu Teacher F5-TTS v1。\n'
    (PKG/'youtube-upload-kit.md').write_text(upload.rstrip() + insert + '\n', encoding='utf-8')

archive = PKG / 'parent-message-draft-only-lu-f5tts-v1-kit-20260516.tar.gz'
members = ['README.md','manifest.json','build_lu_f5tts_upgrade_v1.py','youtube-upload-kit.md','parent-message-review-checklist-v1.md',new_mp4.name,'parent-message-draft-only-shorts-35s.mp4','cover_parent_message_draft_only_v1.png','narration_35s.txt',mp3.name,fit.name,'narration_35s_lu_f5tts_v1.vtt','narration_35s_lu_f5tts_v1.srt','narration_35s_yunjhe.mp3','narration_35s_yunjhe.vtt','checks/qa_sheet_mp4.png','checks/frame_early_lu_f5v1.png','checks/frame_mid_lu_f5v1.png','checks/frame_late_lu_f5v1.png']
with tarfile.open(archive, 'w:gz') as tar:
    for rel in members:
        p = PKG / rel
        if p.exists():
            tar.add(p, arcname=f'parent-message-draft-only-20260515/{rel}')
    for p in sorted((PKG/'slides').glob('slide_*.png')):
        tar.add(p, arcname=f'parent-message-draft-only-20260515/slides/{p.name}')
with tarfile.open(archive, 'r:gz') as tar:
    names = tar.getnames()
    assert any(new_mp4.name in n for n in names)
    assert any('README.md' in n for n in names)

for dest in PAGES_ROOTS:
    dest.mkdir(parents=True, exist_ok=True)
    for rel in [new_mp4.name, mp3.name, fit.name, 'narration_35s_lu_f5tts_v1.vtt','narration_35s_lu_f5tts_v1.srt','README.md','manifest.json','youtube-upload-kit.md','build_lu_f5tts_upgrade_v1.py',archive.name]:
        src = PKG / rel
        if src.exists():
            (dest/rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest/rel)
    (dest/'checks').mkdir(exist_ok=True)
    for rel in ['frame_early_lu_f5v1.png','frame_mid_lu_f5v1.png','frame_late_lu_f5v1.png']:
        src = PKG/'checks'/rel
        if src.exists(): shutil.copy2(src, dest/'checks'/rel)

probe = subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=index,codec_type,codec_name,width,height,r_frame_rate','-show_entries','format=duration,size','-of','json',str(new_mp4)], text=True)
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
}
print(json.dumps(info, ensure_ascii=False, indent=2))
