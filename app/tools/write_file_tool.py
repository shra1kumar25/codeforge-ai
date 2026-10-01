from pathlib import Path


def write_file(file_path: str, content: str):
    path = Path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(content)

    return {
        "success": True,
        "file": file_path
    }
