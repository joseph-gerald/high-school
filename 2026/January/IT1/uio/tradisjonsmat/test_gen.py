import random

def generate_test_data(n, target_sum, filename="test_data.txt"):
    """
    Generates N pairs of numbers that each add up to target_sum.
    """
    numbers = []
    for _ in range(n):
        # Generate a random first element
        val1 = random.randint(1, target_sum - 1)
        val2 = target_sum - val1
        numbers.extend([val1, val2])

    # Shuffle to make the pairs non-obvious
    random.shuffle(numbers)

    with open(filename, "w") as f:
        f.write(f"{n}\n")
        f.write(" ".join(map(str, numbers)) + "\n")

# Example: Generate 5 pairs (10 numbers total) that sum to 50
generate_test_data(n=10, target_sum=100)
