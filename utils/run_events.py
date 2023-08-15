import subprocess


def start_shell_script(file_path):
    subprocess.call(["./preprocessing/run-process.sh", "6", file_path])
