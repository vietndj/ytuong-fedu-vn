# Siren Vibe – Prompt cho Gemini (Create music / Lyria 3)

## 0. Thông số gốc của "Siren" (đo bằng librosa)
| Chỉ số | Siren (gốc) | midnight_tide (lỗi) |
|---|---|---|
| Tempo | **~89 BPM** | 123 BPM (lạc sang House) |
| Spectral Centroid | **~1340 Hz** (ấm, tối) | ~1990 Hz (quá sáng) |
| Rolloff | ~2680 Hz | ~4360 Hz |

→ Mỏ neo bắt buộc: **89 BPM · trầm ấm · cắt bớt treble · groove Afro chậm · giọng nam mượt dùng như nhạc cụ.**

## 1. Vì sao prompt trước không ra nhạc trên Gemini
1. **Sai định dạng:** Box "Style" + Lyrics với `[Verse]`, `(ad-libs)` là cú pháp của Suno/Udio. Gemini đọc prompt như một bản brief bằng câu văn tự nhiên; khối thẻ ngoặc dễ bị hiểu là văn bản/lời, hoặc không kích hoạt tool tạo nhạc.
2. **Phải bật tool "Create music"** (hoặc mở đầu bằng "Create a track…"), nếu không Gemini chỉ trả lời bằng chữ.
3. **Mâu thuẫn yêu cầu:** "không có lời" nhưng prompt lại bắt hát verse/chorus → model bị rối. Cách hiểu đúng: **giọng nam chỉ ngân nga (hum / ooh / mmm / vocal chops), không thành từ.**
4. **Thiếu chặn âm (negative):** không cấm EDM/house beat/synth sáng → model trôi lên 123 BPM.

## 2. Ba prompt – 3 hướng tiếp cận

### Hướng A – Producer Brief (khóa kỹ thuật, ổn định nhất)
```
Create an instrumental slow Afrobeats / Afro-R&B track at 89 BPM. No lyrics and no spoken words.
Mood: warm, intimate, late-night, sensual and relaxed.
Instruments: deep round sub-bass, soft Rhodes electric piano chords, muted plucked guitar, gentle shakers and a soft log drum, with a laid-back syncopated Afro groove (soft kick, rimshot snare).
A smooth, soulful male voice appears only as wordless humming, "ooh" and "mmm" ad-libs and airy vocal chops drenched in reverb, used like an instrument.
Warm, dark mix with rolled-off highs. No bright synths, no EDM, no four-on-the-floor house beat, no fast tempo.
```

### Hướng B – Cinematic Scene (để model tự cảm không khí, đầu ra đa dạng nhất)
```
Create music that scores this scene: 1 a.m. on a quiet rooftop in Lagos after the rain, blurry city lights in the distance, warm humid air, then a slow drive home with the windows down.
The music is an unhurried Afro-fusion groove around 90 BPM that makes you sway, not dance. Warm electric piano, a deep bass you feel more than hear, soft hand percussion and shakers.
A low, velvety male voice hums and sings wordless melodies in the background, never forming words.
Dark, intimate, hypnotic and nostalgic. Instrumental, no lyrics.
```
> Mẹo: đính kèm thêm 1 ảnh đêm thành phố/xe chạy đêm – Lyria dùng màu sắc ảnh để định mood.

### Hướng C – Arrangement Timeline (kiểm soát cấu trúc, hợp bản dài 1–3 phút)
```
Create an instrumental Afro-R&B track, 89 BPM, minor key, warm and dark.
Intro: Rhodes chords alone with soft room ambience and a distant male hum.
Groove: deep sub-bass and a relaxed syncopated Afro drum pattern with shakers come in.
Hook: a smooth male voice sings a catchy wordless "oh-oh" melody with soft layered harmonies, answered by a muted guitar riff.
Breakdown: drums drop out, only bass, piano and echoing vocal ad-libs remain.
Outro: the groove returns briefly, then fades on shakers and reverb tails.
No lyrics, no rap, no bright synth leads, no fast tempo.
```

## 3. Cách dùng lại nhiều lần mà vẫn random
Giữ nguyên mỏ neo (**89 BPM, warm dark mix, wordless male voice, no EDM**), mỗi lần chỉ đổi **1 biến**:
- Nhạc cụ dẫn: `muted guitar` → `kalimba` / `soft saxophone` / `wooden flute` / `talking drum`
- Cảnh (hướng B): rooftop Lagos → beach bar at midnight / hotel lounge / rainy taxi ride
- Màu hợp âm: `minor key` → `dreamy major seventh chords`
- Sau khi có bản ưng: chat tiếp "keep the same vibe, make the bass warmer / slow it down slightly".
