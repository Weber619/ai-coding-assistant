import asyncio
import tempfile
import os
from typing import List, Dict
from pylint.lint import Run
from pylint.reporters import CollectingReporter
import logging

# Suppress Pylint output in tests
logging.getLogger('pylint').setLevel(logging.CRITICAL)

async def analyze_code(code: str) -> list:
    issues = []

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
        tmp_file.write(code)
        tmp_file_path = tmp_file.name

    try:
        reporter = CollectingReporter()
        Run([tmp_file_path], reporter=reporter, exit=False)

        for msg in reporter.messages:
            # Adjust message for syntax errors
            if msg.symbol == 'syntax-error' or msg.msg_id == 'E0001':
                message = f"Syntax Error: {msg.msg}"
                issues.append({
                    'type': 'error',
                    'line': str(msg.line),
                    'column': str(msg.column),
                    'message': message
                })
            elif msg.category in ['error', 'warning']:
                issues.append({
                    'type': msg.category,
                    'line': str(msg.line),
                    'column': str(msg.column),
                    'message': msg.msg or msg.symbol
                })
            # Ignore convention and refactor messages

        if not issues:
            issues = [{'type': 'info', 'line': '1', 'column': '1', 'message': 'No issues found'}]
    except Exception as e:
        # If Pylint raises an exception, capture it as a syntax error
        issues.append({
            'type': 'error',
            'line': '1',
            'column': '1',
            'message': f"Syntax Error: {str(e)}"
        })
    finally:
        os.unlink(tmp_file_path)

    return issues

def parse_pylint_output(output: str) -> List[Dict[str, str]]:
    issues = []
    for line in output.split('\n'):
        if ':' in line:
            parts = line.split(':')
            if len(parts) >= 4:
                issue = {
                    "type": parts[0].strip(),
                    "line": parts[1].strip(),
                    "column": parts[2].strip(),
                    "message": ':'.join(parts[3:]).strip()
                }
                issues.append(issue)
    return issues if issues else [{"type": "info", "line": "1", "column": "1", "message": "No issues found"}]

async def main():
    code = input("Enter the Python code to analyze:\n")
    use_custom_rules = input("Do you want to use custom rules? (y/n): ").lower() == 'y'
    
    custom_rules = None
    if use_custom_rules:
        custom_rules = {
            "max-line-length": 100,
            "disable": ["C0111", "C0103"],
            "enable": ["W0611", "W0612"]
        }
    
    try:
        analysis_results = await analyze_code(code)
        if analysis_results:
            print("\nAnalysis Results:")
            for issue in analysis_results:
                print(f"{issue['type']} at line {issue['line']}, column {issue['column']}: {issue['message']}")
        else:
            print("No issues found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())