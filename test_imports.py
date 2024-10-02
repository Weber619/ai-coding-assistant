import sys
import openai
import pydantic
import pylint

print(f"Python version: {sys.version}")
print(f"OpenAI version: {openai.__version__}")
print(f"Pydantic version: {pydantic.__version__}")
print(f"Pylint version: {pylint.__version__}")