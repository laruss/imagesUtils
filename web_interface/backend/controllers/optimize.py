from core.utils import get_root_path


def optimize(method: str):
    import subprocess

    script_path = f"{get_root_path()}/optimize/main.py"

    command = f"python3 {script_path} --method {method}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()

    return True
