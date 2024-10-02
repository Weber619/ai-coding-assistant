import unittest
import asyncio
import os
from unittest.mock import AsyncMock, patch

from code_generator import generate_code
from code_analyzer import analyze_code
from code_refactor import refactor_code
from code_optimizer import optimize_code

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ.get('OPENAI_API_KEY', 'fake_api_key')

    def async_test(f):
        def wrapper(*args, **kwargs):
            asyncio.run(f(*args, **kwargs))
        return wrapper

    @async_test
    @patch('openai.ChatCompletion.create', new_callable=AsyncMock)
    async def test_full_workflow(self, mock_create):
        # Step 1: Generate Code
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].function_call = AsyncMock()
        mock_response.choices[0].function_call.arguments = '{"code": "def factorial(n):\\n    if n == 0:\\n        return 1\\n    else:\\n        return n * factorial(n-1)", "explanation": "This is a recursive factorial function."}'
        mock_create.return_value = mock_response

        prompt = "Write a function to calculate the factorial of a number"
        generated_result = await generate_code(prompt, self.api_key)
        self.assertIn('def factorial', generated_result['code'])

        # Step 2: Analyze Code
        analysis_result = await analyze_code(generated_result['code'])
        self.assertIsInstance(analysis_result, list)

        # Step 3: Refactor Code (rename function)
        refactored_code = await refactor_code(generated_result['code'], "rename", old_name="factorial", new_name="calculate_factorial")
        self.assertIn('def calculate_factorial', refactored_code)

        # Step 4: Optimize Code
        optimized_result = await optimize_code(refactored_code)
        self.assertIn('optimized_code', optimized_result)
        self.assertIsInstance(optimized_result['optimizations'], list)

    @async_test
    async def test_error_handling(self):
        # Test with invalid code
        invalid_code = "def incomplete_function("
        result = await analyze_code(invalid_code)
        # Check that issues are found
        self.assertNotEqual(result, [{'type': 'info', 'line': '1', 'column': '1', 'message': 'No issues found'}],
                            f"Expected to find issues, but got: {result}")
        # Check that a syntax error is reported
        self.assertTrue(any("syntax error" in issue['message'].lower() for issue in result),
                        f"Expected syntax error in issues, but got: {result}")

        # Test with valid code
        valid_code = "def test(): pass"
        result = await analyze_code(valid_code)
        self.assertEqual(result, [{'type': 'info', 'line': '1', 'column': '1', 'message': 'No issues found'}], 
                         f"Expected no issues, but got: {result}")

        # Test with code containing a warning
        warning_code = "def test():\n    unused_var = 5\n    pass"
        result = await analyze_code(warning_code)
        self.assertTrue(any(issue['type'] == 'warning' for issue in result),
                        f"Expected a warning, but got: {result}")

        # Test with invalid refactoring
        with self.assertRaises(ValueError):
            await refactor_code(valid_code, "non_existent_refactor_type")

    @async_test
    @patch('openai.ChatCompletion.create', new_callable=AsyncMock)
    async def test_multiple_iterations(self, mock_create):
        prompt = "Write a function to find the n-th Fibonacci number"
        code = ""
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].function_call = AsyncMock()
        mock_response.choices[0].function_call.arguments = '{"code": "def fibonacci(n):\\n    if n <= 1:\\n        return n\\n    return fibonacci(n-1) + fibonacci(n-2)", "explanation": "This is a recursive Fibonacci function."}'
        mock_create.return_value = mock_response

        for _ in range(3):  # Simulate 3 iterations of improvement
            generated_result = await generate_code(prompt, self.api_key, context=code)
            code = generated_result['code']
            analysis_result = await analyze_code(code)
            if analysis_result:
                prompt += f"\nImprove the following code and address these issues: {analysis_result}"
            optimized_result = await optimize_code(code)
            code = optimized_result['optimized_code']

        self.assertIn('def', code)  # Ensure we still have a function definition
        self.assertIn('fibonacci', code.lower())  # Check if it's related to Fibonacci

if __name__ == '__main__':
    unittest.main()