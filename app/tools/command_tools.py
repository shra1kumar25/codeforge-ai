import shlex
import subprocess


ALLOWED_COMMANDS = {
    "python",
    "pytest",
    "pip",
    "uvicorn",
    "echo",
    "ls",
    "pwd",
    "cat",
}


def run_command(command: str):
    try:
        parts = shlex.split(command)

        if not parts:
            return {
                "success": False,
                "error": "Empty command",
            }

        executable = parts[0]

        if executable not in ALLOWED_COMMANDS:
            return {
                "success": False,
                "command": command,
                "error": f"Command not allowed: {executable}",
            }

        result = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            timeout=60,
        )

        return {
            "success": result.returncode == 0,
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "command": command,
            "error": "Command timed out after 60 seconds",
        }

    except Exception as exc:
        return {
            "success": False,
            "command": command,
            "error": str(exc),
        }
