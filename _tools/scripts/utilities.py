import os
import platform
from shutil import copyfile
import string
import subprocess
import sys

def is_linux():
    return platform.system() == 'Linux'

def is_macos():
    return platform.system() == 'Darwin'

def is_windows():
    return platform.system() == 'Windows'

def call_command(command, show_output=True):
    if is_linux() or is_macos():
        cmd = ['zsh', '-c', 'source ~/.zshrc; ' + command.encode()]
        if show_output:
            subprocess.call(cmd)
        else:
            subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if is_windows():
        cmd = ['pwsh', '-ExecutionPolicy', 'Unrestricted', '-Command', '-']

        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        process.stdin.write(command.encode())
        process.stdin.close()

        if show_output:
            while True:
                output = process.stdout.readline()
                if output == b'' and process.poll() is not None:
                    break
                if output:
                    print(output.strip().decode())
            process.stdout.close()

        process.wait()

def call_command_and_capture(command):
    if is_windows():
        cmd = ['pwsh', '-ExecutionPolicy', 'Unrestricted', '-Command', '-']
    else:
        cmd = ['zsh', '-c', 'source ~/.zshrc']

    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    process.stdin.write(command.encode())
    out, err = process.communicate()

    return process.returncode, out.decode().strip(), err.decode().strip()

def create_path(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        print(e)
        sys.exit(1)

def copy_file(src, dest, file):
    try:
        copyfile(src, dest.joinpath(file))
    except Exception as e:
        print(e)
    else:
        print(f"'{file}' created")

def template_file(src, dest, file, additional_text="", **kwargs):
    try:
        with open(src, "r") as f:
            template = string.Template(f.read())
            content = template.safe_substitute(**kwargs)

        with open(dest.joinpath(file), "w") as f:
            f.write(content)
    except Exception as e:
        print(e)
    else:
        print(f"'{file}' generated{additional_text}")
