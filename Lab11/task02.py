#task 02

def group_by(f, target_list):

    result = {}
    for item in target_list:
        key = f(item)  # Apply the function to get grouping key
        if key not in result:
            result[key] = []  # Initialize list for key
        result[key].append(item)  # Add item to correct group
    return result



# Example
example_list = ["hi", "dog", "me", "bad", "good"]
grouped_result = group_by(len, example_list)

print(grouped_result)
# Output: {2: ["hi", "me"], 3: ["dog", "bad"], 4: ["good"]}

example_list = ["hi", "dog", "me", "bad", "good"]
print(group_by(len, example_list))
# Output: {2: ["hi", "me"], 3: ["dog", "bad"], 4: ["good"]}

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(group_by(lambda x: x % 2, numbers))
# Output: {1: [1, 3, 5, 7, 9], 0: [2, 4, 6, 8]}