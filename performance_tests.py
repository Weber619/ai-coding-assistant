import timeit
import asyncio
from code_generator import generate_code
from code_analyzer import analyze_code
from code_refactor import refactor_code
from code_optimizer import optimize_code

async def performance_test_generate_code():
    start_time = timeit.default_timer()
    await generate_code("Create a function to calculate the fibonacci sequence", "fake_api_key")
    end_time = timeit.default_timer()
    return end_time - start_time

async def performance_test_analyze_code():
    code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    """
    start_time = timeit.default_timer()
    await analyze_code(code)
    end_time = timeit.default_timer()
    return end_time - start_time

async def performance_test_refactor_code():
    code = """
def old_name(x, y):
    return x + y
    """
    start_time = timeit.default_timer()
    await refactor_code(code, "rename", old_name="old_name", new_name="add_numbers")
    end_time = timeit.default_timer()
    return end_time - start_time

async def performance_test_optimize_code():
    code = """
result = ''
for i in range(1000):
    result += str(i)
    """
    start_time = timeit.default_timer()
    await optimize_code(code)
    end_time = timeit.default_timer()
    return end_time - start_time

async def run_performance_tests():
    generate_time = await performance_test_generate_code()
    analyze_time = await performance_test_analyze_code()
    refactor_time = await performance_test_refactor_code()
    optimize_time = await performance_test_optimize_code()

    print(f"Generate Code: {generate_time:.4f} seconds")
    print(f"Analyze Code: {analyze_time:.4f} seconds")
    print(f"Refactor Code: {refactor_time:.4f} seconds")
    print(f"Optimize Code: {optimize_time:.4f} seconds")

if __name__ == "__main__":
    asyncio.run(run_performance_tests())