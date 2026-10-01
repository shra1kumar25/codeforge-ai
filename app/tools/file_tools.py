from pathlib import Path


WORKSPACE_ROOT = Path.cwd().resolve()


def safe_path(file_path: str):
    path = (WORKSPACE_ROOT / file_path).resolve()

    if not path.is_relative_to(WORKSPACE_ROOT):
        return None

    return path


def read_file(file_path: str):
    path = safe_path(file_path)

    if path is None:
        return {
            "success": False,
            "error": "Access denied: path is outside the workspace",
        }

    if not path.exists():
        return {
            "success": False,
            "error": f"File not found: {file_path}",
        }

    if not path.is_file():
        return {
            "success": False,
            "error": f"Path is not a file: {file_path}",
        }

    try:
        content = path.read_text(encoding="utf-8")

        return {
            "success": True,
            "file_path": str(path),
            "content": content,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }


def write_file(file_path: str, content: str):
    path = safe_path(file_path)

    if path is None:
        return {
            "success": False,
            "error": "Access denied: path is outside the workspace",
        }

    try:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        return {
            "success": True,
            "file_path": str(path),
            "message": "File written successfully",
        }

    except Exception as exc:
        return {
            "success": False,
            "file_path": str(path),
            "error": str(exc),
        }
