import tempfile
from pathlib import Path

from file_organizer import organize_files


def test_basic_moves_and_dedup():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        # Create sample files
        (p / "photo.JPG").write_bytes(b"img")  # case-insensitive
        (p / "doc.pdf").write_bytes(b"pdf")
        (p / "archive.zip").write_bytes(b"zip")
        (p / "video.MP4").write_bytes(b"vid")
        (p / "song.mp3").write_bytes(b"aud")
        (p / "script.py").write_text("print('hi')")
        (p / "unknown.xyz").write_text("?")
        (p / "noext").write_text("noext")  # left in place by default
        # Duplicate to drive dedup logic
        (p / "doc (1).pdf").write_text("pdf2")
        (p / "doc.pdf").write_bytes(b"pdf3")

        moved = organize_files(tmp)
        assert moved >= 7

        # Verify destinations
        assert (p / "Images" / "photo.JPG").exists()
        assert (p / "Documents" / "doc (2).pdf").exists() or (p / "Documents" / "doc (1).pdf").exists()
        assert (p / "Archives" / "archive.zip").exists()
        assert (p / "Videos" / "video.MP4").exists()
        assert (p / "Audio" / "song.mp3").exists()
        assert (p / "Code" / "script.py").exists()
        assert (p / "Misc" / "unknown.xyz").exists()
        # noext remains in place
        assert (p / "noext").exists()
