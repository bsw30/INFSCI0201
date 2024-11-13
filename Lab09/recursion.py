def product_of_digits(x):
    x = abs(x)
    if x < 10:
        return x
    return (x % 10) * product_of_digits(x // 10)

def array_to_string(a, index=0):
    if not a:
        return ""
    if index == len(a) - 1:
        return str(a[index])
    return str(a[index]) + "," + array_to_string(a, index + 1)

def floored_log(value, base, count=0):
    if value <= 0 or base <= 1:
        raise ValueError("Value must be greater than 0 and base must be greater than 1.")
    if value < base:
        return count
    return floored_log(value // base, base, count + 1)



#test usage
def test_product_of_digits():
    assert product_of_digits(234) == 24, "Test case 1 failed for product_of_digits"
    assert product_of_digits(12) == 2, "Test case 2 failed for product_of_digits"
    assert product_of_digits(-12) == 2, "Test case 3 failed for product_of_digits"
    assert product_of_digits(0) == 0, "Test case 4 failed for product_of_digits"
    assert product_of_digits(9) == 9, "Test case 5 failed for product_of_digits"
    print("All tests passed for product_of_digits")

def test_array_to_string():
    assert array_to_string([1, 2, 3, 4]) == "1,2,3,4", "Test case 1 failed for array_to_string"
    assert array_to_string([7, 8, 9]) == "7,8,9", "Test case 2 failed for array_to_string"
    assert array_to_string([5]) == "5", "Test case 3 failed for array_to_string"
    assert array_to_string([]) == "", "Test case 4 failed for array_to_string"
    print("All tests passed for array_to_string")

def test_floored_log():
    assert floored_log(123456, 10) == 5, "Test case 1 failed for floored_log"
    assert floored_log(64, 2) == 6, "Test case 2 failed for floored_log"
    assert floored_log(4567, 10) == 3, "Test case 3 failed for floored_log"
    assert floored_log(1, 2) == 0, "Test case 4 failed for floored_log"
    try:
        floored_log(-1, 10)
    except ValueError:
        pass
    else:
        print("Test case 5 failed for floored_log: should raise ValueError for invalid input")

    try:
        floored_log(100, 1)
    except ValueError:
        pass
    else:
        print("Test case 6 failed for floored_log: should raise ValueError for invalid input")

    print("All tests passed for floored_log")

def run_all_tests():
    test_product_of_digits()
    test_array_to_string()
    test_floored_log()
    print("All tests passed successfully!")

# Run all tests
run_all_tests()