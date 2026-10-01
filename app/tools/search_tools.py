from pathlib import Path


def search_code(
    search_term: str,
    project_path: str = ".",
):
    results = []

    root = Path(project_path)

    for file_path in root.rglob("*"):

        if not file_path.is_file():
            continue

        if any(
            part in {"venv", ".git", "__pycache__"}
            for part in file_path.parts
        ):
            continue

        # Search by filename first
        if search_term.lower() in file_path.name.lower():
            results.append(
                {
                    "file": str(file_path),
                    "line": 0,
                    "content": "filename_match",
                }
            )

        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except Exception:
            continue

        for line_number, line in enumerate(
            content.splitlines(),
            start=1,
        ):
            if search_term.lower() in line.lower():
                results.append(
                    {
                        "file": str(file_path),
                        "line": line_number,
                        "content": line.strip(),
                    }
                )

    return {
        "success": True,
        "search_term": search_term,
        "results": results,
    }
