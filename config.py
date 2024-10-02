import os

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DEFAULT_MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # Pylint configuration
    PYLINT_ARGS = [
        '--disable=C0111',  # Missing docstring
        '--max-line-length=100',
    ]
    
    # Optimization settings
    OPTIMIZATION_LEVEL = 2  # 1: Basic, 2: Intermediate, 3: Advanced
    
    # Git integration settings
    GIT_AUTO_COMMIT = False
    GIT_COMMIT_MESSAGE_TEMPLATE = "AI Assistant: {action} in {file}"

config = Config()