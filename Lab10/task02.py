# Task 02
import time
from functools import wraps

# Custom caching decorator
def cache_decorator(func):
    cache = {}

    @wraps(func)
    def wrapper(n):
        if n in cache:
            return cache[n]
        result = func(n)
        cache[n] = result
        return result
    return wrapper

# recursive Fibonacci
def recur_fib(n):
    if n <= 1:
        return n
    return recur_fib(n - 1) + recur_fib(n - 2)

# Decorated recursive Fibonacci
@cache_decorator
def recur_fib_cached(n):
    if n <= 1:
        return n
    return recur_fib_cached(n - 1) + recur_fib_cached(n - 2)

# Measure execution time for original and decorated functions
def measure_execution_time():
    n = 35

    print("Calculating Fibonacci using original recursive method:")
    start_time = time.perf_counter()
    result = recur_fib(n)
    print(f"Result: {result}")
    print(f"Execution time: {time.perf_counter() - start_time:.6f} seconds\n")

    print("Calculating Fibonacci using cached recursive method:")
    start_time = time.perf_counter()
    result = recur_fib_cached(n)
    print(f"Result: {result}")
    print(f"Execution time: {time.perf_counter() - start_time:.6f} seconds\n")

# Example usage:
if __name__ == "__main__":
    measure_execution_time()