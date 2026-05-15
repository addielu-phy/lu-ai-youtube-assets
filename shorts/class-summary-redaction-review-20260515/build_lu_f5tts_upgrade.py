#!/usr/bin/env python3
from pathlib import Path
import subprocess, json, shutil, tarfile

PKG = Path('/home/adl/youtube-lu-ai-channel/shorts/class-summary-redaction-review-20260515')
PAGES = Path('/home/adl/pages/lu-ai-youtube-assets/shorts/class-summary-redaction-review-20260515')
ASSETS_PAGES = Path('/home/adl/lu-ai-youtube-assets-pages/shorts/class-summary-redaction-review-20260515')
F5 = Path('/home/adl/youtube-lu-ai-channel/voice-lab/free-local-tts/f5env/bin/f5-tts_infer-cli')
REF_AUDIO = Path('/home/adl/video-projects/episode-1-ai-agent-uses/f5tts-ref-alt/ref_alt.wav')
REF_TEXT = Path('/home/adl/video-projects/episode-1-ai-agent-uses/f5tts-ref-alt/ref_text_alt.txt').read_text(encoding='utf-8').strip()
BASE = PKG / 'lu_f5tts_upgrade_v1'
TXT = BASE / 'chunks_text'
WAV = BASE / 'chunks_wav'
LOG = BASE / 'logs'
for d in [TXT, WAV, LOG, PKG/'checks']:
    d.mkdir(parents=True, exist_ok=True)

# Concise Lu Teacher voice-clone version; chunked for stable pacing and fewer artifacts.
chunks = [
    'AI 幫你整理課堂摘要時，最危險的不是寫得不好，而是寫得太像真的。',
    '第一種先刪：能看出是哪位學生的句子，像座號、特殊事件，或可辨識錯誤。',
    '第二種先刪：把學生貼標籤的句子，像是懶散、粗心、程度差。',
    '第三種先刪：沒有證據的評價，例如全班都不懂，或某組表現最差。',
    '最後，改成匿名、可觀察、可改進的學習線索。摘要才是教學工具，不是學生標籤。',
]
for i, t in enumerate(chunks, 1):
    (TXT / f'chunk_{i:02d}.txt').write_text(t, encoding='utf-8')

for i, t in enumerate(chunks, 1):
    out = WAV / f'chunk_{i:02d}.wav'
    cmd = [str(F5), '--model', 'F5TTS_v1_Base', '--ref_audio', str(REF_AUDIO), '--ref_text', REF_TEXT,
           '--gen_text', t, '--output_dir', str(WAV), '--output_file', out.name,
           '--device', 'cuda', '--speed', '1.05', '--remove_silence', '--no_legacy_text']
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
# Fit to 35 s. If generated speech is a little long, use modest tempo correction; otherwise pad.
if dur > 34.85:
    ratio = dur / 34.75
    af = f'atempo={ratio:.6f},apad,loudnorm=I=-16:TP=-1.5:LRA=11'
else:
    ratio = 1.0
    af = 'apad,loudnorm=I=-16:TP=-1.5:LRA=11'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(loud),'-t','35.000','-af',af,'-ar','48000',str(fit)], check=True)
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(fit),'-codec:a','libmp3lame','-b:a','192k',str(mp3)], check=True)

old_mp4 = PKG / 'class-summary-redaction-review-shorts-35s.mp4'
new_mp4 = PKG / 'class-summary-redaction-review-shorts-35s-lu-f5tts-v1.mp4'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(old_mp4),'-i',str(fit),'-map','0:v:0','-map','1:a:0','-t','35.000','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(new_mp4)], check=True)

segments = [
    (0.0, 5.6, 'AI 摘要最危險：寫得太像真的。'),
    (5.6, 12.8, '先刪可辨識學生的句子。'),
    (12.8, 19.8, '再刪把學生貼標籤的句子。'),
    (19.8, 27.0, '沒有證據的全班評價，也先刪。'),
    (27.0, 35.0, '改成匿名、可觀察、可改進的學習線索。'),
]
def ts(sec, comma=False):
    h=int(sec//3600); m=int((sec%3600)//60); s=int(sec%60); ms=int(round((sec-int(sec))*1000))
    return f'{h:02d}:{m:02d}:{s:02d}{"," if comma else "."}{ms:03d}'
(PKG/'narration_35s_lu_f5tts_v1.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{ts(a)} --> {ts(b)}\n{text}' for a,b,text in segments)+'\n', encoding='utf-8')
(PKG/'narration_35s_lu_f5tts_v1.srt').write_text('\n\n'.join(f'{i}\n{ts(a, True)} --> {ts(b, True)}\n{text}' for i,(a,b,text) in enumerate(segments,1))+'\n', encoding='utf-8')

for name, sec in [('frame_early_lu_f5v1.png','2.0'),('frame_mid_lu_f5v1.png','17.0'),('frame_late_lu_f5v1.png','32.0')]:
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',sec,'-i',str(new_mp4),'-frames:v','1','-update','1',str(PKG/'checks'/name)], check=True)

# Update manifest/readme/upload kit without deleting the old Edge files.
manifest = json.loads((PKG/'manifest.json').read_text(encoding='utf-8'))
manifest.update({
    'mp4_lu_voice': new_mp4.name,
    'audio_source': 'Lu Teacher F5-TTS voice clone v1',
    'narration_lu_voice': mp3.name,
    'subtitles_lu_voice': ['narration_35s_lu_f5tts_v1.vtt','narration_35s_lu_f5tts_v1.srt'],
    'voice_upgrade_note': 'Original package used Edge zh-TW-HsiaoYuNeural; this v1 replaces audio with Lu Teacher F5-TTS voice clone, chunked generation, loudnorm, fitted to 35s.'
})
(PKG/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
readme = (PKG/'README.md').read_text(encoding='utf-8')
append = f'''

## 音訊升級 v1（Lu Teacher F5-TTS）

- 改善原因：原版使用 Edge HsiaoYu 女聲旁白；本版改用盧老師 F5-TTS voice clone。
- 升級版 MP4：`{new_mp4.name}`
- 升級版旁白：`{mp3.name}` / `{fit.name}`
- 升級版字幕：`narration_35s_lu_f5tts_v1.vtt` / `narration_35s_lu_f5tts_v1.srt`
- 音訊處理：F5-TTS chunked generation、0.22 秒短停頓、loudnorm I=-16、AAC 192k、35 秒完整輸出。
'''
if '## 音訊升級 v1（Lu Teacher F5-TTS）' not in readme:
    (PKG/'README.md').write_text(readme + append, encoding='utf-8')

archive = PKG / 'class-summary-redaction-review-lu-f5tts-v1-kit-20260515.tar.gz'
members = ['README.md','manifest.json','build_lu_f5tts_upgrade.py','youtube-upload-kit.md','summary-redaction-teacher-checklist-v1.md',new_mp4.name,'class-summary-redaction-review-shorts-35s.mp4','cover_class_summary_redaction_review_v1.png','narration_35s.txt',mp3.name,fit.name,'narration_35s_lu_f5tts_v1.vtt','narration_35s_lu_f5tts_v1.srt','narration_35s_edge_hsiaoyu.mp3','narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt','class_summary_redaction_review.ffconcat','checks/qa_cover_frames_sheet.png','checks/frame_early_lu_f5v1.png','checks/frame_mid_lu_f5v1.png','checks/frame_late_lu_f5v1.png']
with tarfile.open(archive, 'w:gz') as tar:
    for rel in members:
        p = PKG / rel
        if p.exists():
            tar.add(p, arcname=f'class-summary-redaction-review-20260515/{rel}')
    for p in sorted((PKG/'slides').glob('slide_*.png')):
        tar.add(p, arcname=f'class-summary-redaction-review-20260515/slides/{p.name}')

for dest in [PAGES, ASSETS_PAGES]:
    dest.mkdir(parents=True, exist_ok=True)
    for rel in [new_mp4.name, mp3.name, fit.name, 'narration_35s_lu_f5tts_v1.vtt','narration_35s_lu_f5tts_v1.srt','README.md','manifest.json','youtube-upload-kit.md','build_lu_f5tts_upgrade.py',archive.name]:
        src = PKG / rel
        if src.exists():
            (dest/rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest/rel)
    (dest/'checks').mkdir(exist_ok=True)
    for rel in ['frame_early_lu_f5v1.png','frame_mid_lu_f5v1.png','frame_late_lu_f5v1.png']:
        src = PKG/'checks'/rel
        if src.exists(): shutil.copy2(src, dest/'checks'/rel)

# Basic verification: final MP4 has one video stream and one audio stream, expected duration.
probe = subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=index,codec_type,codec_name','-show_entries','format=duration','-of','json',str(new_mp4)], text=True)
info = {
    'raw_audio_duration': duration(raw),
    'loud_audio_duration': dur,
    'tempo_ratio_if_used': ratio,
    'final_audio_duration': duration(fit),
    'new_mp4_duration': duration(new_mp4),
    'new_mp4': str(new_mp4),
    'mp3': str(mp3),
    'archive': str(archive),
    'probe': json.loads(probe),
}
print(json.dumps(info, ensure_ascii=False, indent=2))
