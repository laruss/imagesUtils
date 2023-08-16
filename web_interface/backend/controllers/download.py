from core.utils import get_root_path


def download(items: int, source: str, prompt: str):
    import subprocess

    script_path = f"{get_root_path()}/download/main.py"

    command = f"python3 {script_path} --source {source} --limit {items} --prompt {prompt}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()

    return True

