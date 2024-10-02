import subprocess
import os

def init_git_repo():
    # Initialize Git repository
    subprocess.run(['git', 'init'], check=True)
    
    # Create .gitignore file
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual environment
ai_coding_assistant_env/

# IDE
.vscode/
.idea/

# Miscellaneous
.DS_Store
*.log
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content.strip())
    
    # Add .gitignore to Git
    subprocess.run(['git', 'add', '.gitignore'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit: Add .gitignore'], check=True)
    
    print("Git repository initialized and .gitignore configured successfully.")

if __name__ == "__main__":
    init_git_repo()