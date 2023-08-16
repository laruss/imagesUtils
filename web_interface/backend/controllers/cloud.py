from core.utils import get_root_path


def cloud(method: str = None, provider: str = None):
    import subprocess

    script_path = f"{get_root_path()}/cloud/main.py"

    command = f"python3 {script_path} --method {method} --provider {provider}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()

    return True
