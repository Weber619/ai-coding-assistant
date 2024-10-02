import venv
import subprocess
import os
import sys

def create_venv_and_install_packages():
    # Use the user's home directory for the virtual environment
    venv_path = os.path.join(os.path.expanduser('~'), 'ai_coding_assistant_env')
    
    # Create virtual environment
    venv.create(venv_path, with_pip=True)
    
    # Determine the path to the Python executable in the virtual environment
    if sys.platform == "win32":
        python_executable = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        python_executable = os.path.join(venv_path, "bin", "python")
    
    # Install packages
    packages = ['pylint', 'flake8', 'rope', 'openai', 'fastapi', 'pydantic', 'asyncpg', 'aiomysql', 'sqlalchemy', 'gitpython']
    install_command = [python_executable, "-m", "pip", "install"] + packages
    
    try:
        subprocess.run(install_command, check=True)
        print(f"Virtual environment created at {venv_path} and packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing packages: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_venv_and_install_packages()