import subprocess

TRACE_NUMBER = 100


def start_shell_script(file_path):
    subprocess.call(["./utils/run-process.sh", str(TRACE_NUMBER), file_path])
