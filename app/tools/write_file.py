from app.tools.file_tools import safe_path


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
