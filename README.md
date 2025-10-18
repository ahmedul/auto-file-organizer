# Auto File Organizer

A tiny Python CLI tool that tidies a folder by moving files into subfolders by extension. Perfect for keeping "Downloads" or "Desktop" neat.

- No dependencies (standard library only)
- Safe: skips folders, creates categories if missing, and de-duplicates names (adds "(1)")
- Easy to fork and customize categories

## Usage

Run on the current directory:

```bash
python3 file_organizer.py
```

Or specify a target directory:

```bash
python3 file_organizer.py /path/to/folder
```

What it does:
- Creates subfolders like `Images`, `Documents`, `Archives`, `Videos`, `Audio`, `Code`, and `Misc`.
- Moves only top-level files (does not recurse into subfolders).
- Files without extensions are left in place by default (to avoid surprising moves of executables or dotfiles). Adjust in code if you prefer moving them to `Misc`.
- If a file with the same name already exists in the destination, it appends a number like `file (1).ext`.

## Customize Categories

Edit `categories` in `file_organizer.py`. Example: add `"Design": [".psd", ".ai"]`.

## Contributing

PRs welcome! Ideas:
- Recursive mode (`--recursive`)
- Dry run (`--dry-run`) and logging
- Config file for custom categories
- Scheduler/cron integration
- GUI or web UI

## License

MIT — see `LICENSE`.
