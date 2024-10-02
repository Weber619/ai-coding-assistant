#!/usr/bin/env python3
import os
import sys
import argparse
import asyncio
from typing import Dict, Any
import subprocess
import unittest
import test_ai_coding_assistant
from config import config

def activate_venv():
    # Check if the virtual environment is already activated
    if sys.prefix == os.path.join(os.path.expanduser('~'), 'ai_coding_assistant_env'):
        print("Virtual environment is already activated.")
        return

    venv_path = os.path.join(os.path.expanduser('~'), 'ai_coding_assistant_env')
    
    if sys.platform == "win32":
        activate_this = os.path.join(venv_path, "Scripts", "activate_this.py")
    else:
        activate_this = os.path.join(venv_path, "bin", "activate_this.py")
    
    if not os.path.exists(activate_this):
        print(f"Warning: Virtual environment activation script not found at {activate_this}")
        print("Continuing with the current Python environment.")
        return
    
    exec(open(activate_this).read(), {'__file__': activate_this})

    # Add the virtual environment's site-packages to sys.path
    if sys.platform == "win32":
        site_packages = os.path.join(venv_path, 'Lib', 'site-packages')
    else:
        site_packages = os.path.join(venv_path, 'lib', 'python{}.{}'.format(sys.version_info.major, sys.version_info.minor), 'site-packages')
    sys.path.insert(0, site_packages)

# Activate the virtual environment
activate_venv()

from code_generator import generate_code
from code_analyzer import analyze_code
from code_refactor import refactor_code
from code_optimizer import optimize_code
from git_integration import commit_improved_code
from error_handler import error_handler

@error_handler
async def handle_code_generation(args: argparse.Namespace) -> None:
    api_key = args.api_key or config.OPENAI_API_KEY
    prompt = args.prompt
    
    generated_code = await generate_code(prompt, api_key, model=config.DEFAULT_MODEL)
    print("\nGenerated Code:")
    print(generated_code['code'])
    print("\nExplanation:")
    print(generated_code['explanation'])

@error_handler
async def handle_code_analysis(args: argparse.Namespace) -> None:
    code = args.code.replace('\\n', '\n')  # Replace escaped newlines with actual newlines
    
    analysis_results = await analyze_code(code)
    if analysis_results:
        print("\nAnalysis Results:")
        for issue in analysis_results:
            print(f"{issue['type']} at line {issue['line']}: {issue['message']}")
        print(f"\nTotal issues found: {len(analysis_results)}")
    else:
        print("No issues found.")

@error_handler
async def handle_code_refactoring(args: argparse.Namespace) -> None:
    code = args.code.replace('\\n', '\n')  # Replace escaped newlines with actual newlines
    refactor_type = args.refactor_type
    refactor_args = {k: v for k, v in vars(args).items() if k not in ['command', 'code', 'refactor_type']}
    
    result = await refactor_code(code, refactor_type, **refactor_args)
    print("\nRefactored Code:")
    print(result)

@error_handler
async def handle_code_optimization(args: argparse.Namespace) -> None:
    code = args.code.replace('\\n', '\n')
    
    optimization_result = await optimize_code(code)
    print("\nOriginal Code:")
    print(optimization_result['original_code'])
    print("\nOptimized Code:")
    print(optimization_result['optimized_code'])
    print("\nOptimizations applied:")
    for opt in optimization_result['optimizations']:
        print(f"- {opt}")

    if args.commit:
        repo_path = os.getcwd()
        file_path = args.file_path
        commit_message = f"Optimized code in {file_path}"
        await commit_improved_code(repo_path, file_path, commit_message)

@error_handler
async def handle_continuous_improvement(args: argparse.Namespace) -> None:
    api_key = args.api_key
    initial_prompt = args.prompt
    iterations = args.iterations
    
    current_code = ""
    for i in range(iterations):
        print(f"\nIteration {i+1}/{iterations}")
        
        # Generate code
        generated_result = await generate_code(initial_prompt, api_key, context=current_code)
        current_code = generated_result['code']
        print("\nGenerated Code:")
        print(current_code)
        
        # Analyze code
        analysis_results = await analyze_code(current_code)
        if analysis_results:
            print("\nAnalysis Results:")
            for issue in analysis_results:
                print(f"{issue['type']} at line {issue['line']}: {issue['message']}")
        
        # Refactor code
        refactored_code = await refactor_code(current_code, "rename", old_name="fibonacci", new_name="fib_sequence")
        current_code = refactored_code
        print("\nRefactored Code:")
        print(current_code)
        
        # Optimize code
        optimization_result = await optimize_code(current_code)
        current_code = optimization_result['optimized_code']
        print("\nOptimized Code:")
        print(current_code)
        
        # Update prompt for next iteration
        initial_prompt += f"\nImprove the following code:\n{current_code}"
    
    print("\nFinal Improved Code:")
    print(current_code)

    if args.commit:
        repo_path = os.getcwd()
        file_path = args.file_path
        commit_message = f"Improved code in {file_path} after {iterations} iterations"
        await commit_improved_code(repo_path, file_path, commit_message)

@error_handler
async def handle_run_tests(args: argparse.Namespace) -> None:
    import unittest
    import test_ai_coding_assistant

    suite = unittest.TestLoader().loadTestsFromModule(test_ai_coding_assistant)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Coding Assistant CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Code Generation
    gen_parser = subparsers.add_parser("generate", help="Generate code")
    gen_parser.add_argument("--api-key", required=True, help="OpenAI API key")
    gen_parser.add_argument("--prompt", required=True, help="Code generation prompt")

    # Code Analysis
    analyze_parser = subparsers.add_parser("analyze", help="Analyze code")
    analyze_parser.add_argument("--code", required=True, help="Code to analyze")

    # Code Refactoring
    refactor_parser = subparsers.add_parser("refactor", help="Refactor code")
    refactor_parser.add_argument("--code", required=True, help="Code to refactor")
    refactor_parser.add_argument("--refactor-type", required=True, choices=["rename", "extract_method", "move_module"], help="Type of refactoring")
    refactor_parser.add_argument("--old-name", help="Old name for rename refactoring")
    refactor_parser.add_argument("--new-name", help="New name for rename or extract method refactoring")
    refactor_parser.add_argument("--start-line", type=int, help="Start line for extract method refactoring")
    refactor_parser.add_argument("--end-line", type=int, help="End line for extract method refactoring")
    refactor_parser.add_argument("--destination", help="Destination for move module refactoring")

    # Code Optimization
    optimize_parser = subparsers.add_parser("optimize", help="Optimize code")
    optimize_parser.add_argument("--code", required=True, help="Code to optimize")
    optimize_parser.add_argument("--commit", action="store_true", help="Commit changes to Git")
    optimize_parser.add_argument("--file-path", help="Path to the file being optimized")

    # Continuous Improvement
    improve_parser = subparsers.add_parser("improve", help="Continuously improve code")
    improve_parser.add_argument("--api-key", required=True, help="OpenAI API key")
    improve_parser.add_argument("--prompt", required=True, help="Initial code generation prompt")
    improve_parser.add_argument("--iterations", type=int, default=3, help="Number of improvement iterations")
    improve_parser.add_argument("--commit", action="store_true", help="Commit changes to Git")
    improve_parser.add_argument("--file-path", help="Path to the file being improved")

    # Run Tests
    test_parser = subparsers.add_parser("test", help="Run unit tests")

    # Add a new subparser for configuration
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("--set", nargs=2, metavar=("KEY", "VALUE"), help="Set a configuration value")
    config_parser.add_argument("--get", metavar="KEY", help="Get a configuration value")
    config_parser.add_argument("--list", action="store_true", help="List all configuration values")

    return parser

async def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "generate":
        await handle_code_generation(args)
    elif args.command == "analyze":
        await handle_code_analysis(args)
    elif args.command == "refactor":
        await handle_code_refactoring(args)
    elif args.command == "optimize":
        await handle_code_optimization(args)
    elif args.command == "improve":
        await handle_continuous_improvement(args)
    elif args.command == "test":
        await handle_run_tests(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())