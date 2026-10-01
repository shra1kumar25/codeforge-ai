from pathlib import Path


def create_file(file_path: str):
    path = Path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    path.touch(exist_ok=True)

    return {
        "success": True,
        "file": file_path
    }
