# Demo assets

This folder contains a copy-paste demo script and tips to record/share a quick preview.

## 1) Run this demo locally

```bash
# Reset sandbox
rm -rf /tmp/organizer-sandbox && mkdir -p /tmp/organizer-sandbox && cd /tmp/organizer-sandbox

# Create mixed files (top-level + nested)
printf 'img' > photo.JPG
printf 'pdf' > doc.pdf
printf 'zip' > archive.zip
printf 'vid' > video.MP4
printf 'aud' > song.mp3
printf 'code' > script.py
printf 'unknown' > unknown.xyz
printf 'noext' > noext
printf 'pdf1' > 'doc (1).pdf'
printf 'pdf2' > doc.pdf
mkdir -p sub/deep
printf 'img' > sub/x.jpg
printf 'pdf' > sub/deep/y.pdf

# Dry-run preview (no changes)
python3 '/home/akabir/git/my project/auto-file-organizer/file_organizer.py' /tmp/organizer-sandbox --recursive --dry-run

# Apply
python3 '/home/akabir/git/my project/auto-file-organizer/file_organizer.py' /tmp/organizer-sandbox --recursive

# Result snapshot
find /tmp/organizer-sandbox -maxdepth 2 -type f | sort
```

## 2) Watch or record a terminal demo

- Option A: Play the included asciinema cast
  - `asciinema play assets/demo.cast`

- Option B: Record your own with asciinema (recommended)
  - Install: https://asciinema.org
  - Record: `asciinema rec assets/demo.cast`
  - Re-run the demo commands above, then Ctrl-D to finish.
  - Share: upload the `.cast` to asciinema or include it in your README using a GIF/MP4 conversion.

- Option C: GIF via ttyrec/agg/peek/obs
  - Use Peek or OBS to capture a short 10–15s clip running the dry-run and apply.

## 3) Convert asciinema cast to GIF/MP4 (optional)

- Use `agg` or `asciinema-player` + a screen recorder.
- Example with `agg` (if installed):
```bash
# install agg (optional): https://github.com/asciinema/agg
agg assets/demo.cast assets/demo.gif
```

## 4) Before/After visuals

- Before: list of mixed files in sandbox root
- After: subfolders with files moved (Images, Documents, Archives, Videos, Audio, Code, Misc)
- Add small overlay stickers in your editor:
  - "No deps"
  - "Dry run first"
  - "One command cleanup"
  - "v0.1.0"
