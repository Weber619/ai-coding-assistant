import sys

def check_import(module_name):
    try:
        __import__(module_name)
        print(f"{module_name} is installed and imported successfully.")
    except ImportError:
        print(f"Error: {module_name} is not installed or cannot be imported.")

modules_to_check = [
    'pylint', 'flake8', 'rope', 'openai', 'fastapi', 'pydantic', 
    'asyncpg', 'aiomysql', 'sqlalchemy', 'git'
]

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print("\nChecking required modules:")

for module in modules_to_check:
    check_import(module)