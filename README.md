# AI Coding Assistant

This AI Coding Assistant is a powerful tool that helps developers generate, analyze, refactor, and optimize code using advanced AI techniques.

## Features

- Code Generation: Generate code snippets based on natural language prompts.
- Code Analysis: Analyze code for potential issues and improvements.
- Code Refactoring: Perform various refactoring operations on existing code.
- Code Optimization: Optimize code for better performance and readability.
- Continuous Improvement: Iteratively improve code through multiple generations and optimizations.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ai-coding-assistant.git
   cd ai-coding-assistant
   ```

2. Run the setup script to create a virtual environment and install dependencies:
   ```bash
   python setup_environment.py
   ```

3. Activate the virtual environment:
   - On Windows: `%USERPROFILE%\ai_coding_assistant_env\Scripts\activate`
   - On Unix or MacOS: `source ~/ai_coding_assistant_env/bin/activate`

## Usage

Use the CLI tool to interact with the AI Coding Assistant:

```bash
python cli.py [command] [options]
```

Available commands:

1. `generate`: Generate code based on a prompt
   ```bash
   python cli.py generate --prompt "Create a FastAPI route for user registration" --language python
   ```
   Options:
   - `--prompt`: The natural language description of the code to generate (required)
   - `--language`: The programming language for the generated code (default: python)
   - `--output`: File path to save the generated code (optional)

2. `analyze`: Analyze existing code for improvements
   ```bash
   python cli.py analyze --file path/to/your/code.py
   ```
   Options:
   - `--file`: Path to the file to analyze (required)
   - `--verbose`: Display detailed analysis results (flag)

3. `refactor`: Perform code refactoring operations
   ```bash
   python cli.py refactor --file path/to/your/code.py --operation extract_function
   ```
   Options:
   - `--file`: Path to the file to refactor (required)
   - `--operation`: Refactoring operation to perform (e.g., extract_function, rename_variable)
   - `--params`: Additional parameters for the refactoring operation (as JSON string)

4. `optimize`: Optimize code for better performance and readability
   ```bash
   python cli.py optimize --file path/to/your/code.py
   ```
   Options:
   - `--file`: Path to the file to optimize (required)
   - `--level`: Optimization level (1-3, default: 1)

5. `improve`: Continuously improve code through multiple generations
   ```bash
   python cli.py improve --file path/to/your/code.py --iterations 3
   ```
   Options:
   - `--file`: Path to the file to improve (required)
   - `--iterations`: Number of improvement iterations to perform (default: 1)
   - `--focus`: Aspect to focus on during improvement (e.g., performance, readability)

## Examples

1. Generate a FastAPI route for user registration:
   ```bash
   python cli.py generate --prompt "Create a FastAPI route for user registration with email and password" --language python
   ```

2. Analyze a Python file for potential improvements:
   ```bash
   python cli.py analyze --file app/routes/user_routes.py --verbose
   ```

3. Refactor a function to extract a new function:
   ```bash
   python cli.py refactor --file app/utils/helpers.py --operation extract_function --params '{"start_line": 10, "end_line": 20, "new_function_name": "process_data"}'
   ```

4. Optimize a file for better performance:
   ```bash
   python cli.py optimize --file app/services/data_processor.py --level 2
   ```

5. Continuously improve a file with a focus on readability:
   ```bash
   python cli.py improve --file app/models/user_model.py --iterations 3 --focus readability
   ```

## Running Tests

To run the unit tests:

```bash
python
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
