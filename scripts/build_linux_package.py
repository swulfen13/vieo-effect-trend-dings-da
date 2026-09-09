import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = "video-effect"
OUTPUT_ZIP = PROJECT_ROOT / "dist" / "video-effect-linux.zip"

EXECUTABLE_FILES = {"install.sh", "run.sh"}

INCLUDE_FILES = [
    "README.md",
    "hand_landmarker.task",
    "install.sh",
    "main.py",
    "requirements.txt",
    "run.sh",
]

INCLUDE_DIRS = ["src"]


def _zipinfo_for(relative_path: Path) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{relative_path.as_posix()}")
    is_executable = relative_path.name in EXECUTABLE_FILES
    unix_mode = 0o755 if is_executable else 0o644
    info.external_attr = (unix_mode & 0xFFFF) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def main():
    OUTPUT_ZIP.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in INCLUDE_FILES:
            src_path = PROJECT_ROOT / name
            rel_path = Path(name)
            zf.writestr(_zipinfo_for(rel_path), src_path.read_bytes())

        for dir_name in INCLUDE_DIRS:
            for src_path in sorted((PROJECT_ROOT / dir_name).rglob("*.py")):
                rel_path = src_path.relative_to(PROJECT_ROOT)
                zf.writestr(_zipinfo_for(rel_path), src_path.read_bytes())

    print(f"Geschrieben: {OUTPUT_ZIP} ({OUTPUT_ZIP.stat().st_size / 1_000_000:.1f} MB)")


if __name__ == "__main__":
    main()
