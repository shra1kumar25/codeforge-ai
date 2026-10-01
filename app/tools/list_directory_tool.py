from pathlib import Path


def list_directory(path="."):
    return [
        item.name
        for item in Path(path).iterdir()
    ]
