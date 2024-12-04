#task 03

from functools import reduce

def filter_with_reduce(predicate, iterable):

    return reduce(
        lambda acc, x: acc + [x] if predicate(x) else acc,
        iterable,
        []
    )



# Example: Filter even numbers from list
def is_even(n):
    return n % 2 == 0

numbers = [1, 2, 3, 4, 5, 6]
filtered_numbers = filter_with_reduce(is_even, numbers)
print(filtered_numbers)  # Output: [2, 4, 6]

# Example: Filter vowels from list
def is_vowel(char):
    return char in 'aeiou'

letters = ['g', 'e', 'e', 'j', 'k', 's', 'p', 'r']
vowels = filter_with_reduce(is_vowel, letters)
print(vowels)  # Output: ['e', 'e']