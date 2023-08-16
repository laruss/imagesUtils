from core.utils import get_root_path


def describe(method: str, gpt_model: str, used_gpt: str):
    import subprocess

    script_path = f"{get_root_path()}/description/main.py"

    command = f"python3 {script_path} --method {method} --gpt-model {gpt_model} --used-gpt {used_gpt}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()

    return True
