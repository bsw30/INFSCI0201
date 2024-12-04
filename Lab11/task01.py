#task01

def zipmap(key_list, value_list, override=False):
    # If False, check duplicate keys and return empty if found
    if not override and len(set(key_list)) != len(key_list):
        return {}

    result = dict(map(lambda pair: (pair[0], pair[1]), zip(key_list, value_list)))

    if len(key_list) > len(value_list):
        extra_keys = key_list[len(value_list):]
        result.update({key: None for key in extra_keys})

    return result



# Example 1
list_1 = ['a', 'b', 'c', 'd', 'e', 'f']
list_2 = [1, 2, 3, 4, 5, 6]
print(zipmap(list_1, list_2))
# Output: {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}

# Example 2
print(zipmap([1, 2, 3, 2], [4, 5, 6, 7], True))
# Output: {1: 4, 2: 7, 3: 6}

# Example 3
print(zipmap([1, 2, 3], [4, 5, 6, 7, 8]))
# Output: {1: 4, 2: 5, 3: 6}

# Example 4
print(zipmap([1, 3, 5, 7], [2, 4, 6]))
# Output: {1: 2, 3: 4, 5: 6, 7: None}