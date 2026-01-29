import sys
from collections import Counter

def validate_response(input_data_str, output_data_str):
    # 1. Parse Input
    try:
        lines = [line for line in input_data_str.strip().split('\n') if line.strip()]
        if not lines:
            return False, "Input data is empty."
            
        # FIX: lines is a list; we need the first element for n
        n = int(lines[0]) 
        
        if len(lines) < 2:
            return False, "Input data format is incorrect: missing the list of numbers."
            
        # FIX: lines[1] contains the actual numbers
        input_numbers = list(map(int, lines[1].strip().split()))
        
        if len(input_numbers) != 2 * n:
            return False, f"Input error: expected {2*n} numbers, got {len(input_numbers)}."
    except (ValueError, IndexError) as e:
        return False, f"Error parsing input numbers: {e}"
    except Exception as e:
        return False, f"An unexpected error occurred during input parsing: {e}"

    # 2. Parse Output
    output_lines = [line for line in output_data_str.strip().split('\n') if line.strip()]
    if output_lines == ['-1']:
        return True, "Valid output format for an impossible pairing."

    output_pairs = []
    try:
        for line in output_lines:
            pair = list(map(int, line.strip().split()))
            if len(pair) != 2:
                return False, f"Output format error: expected 2 numbers, got {len(pair)}: '{line}'"
            output_pairs.append(pair)
    except ValueError as e:
        return False, f"Error parsing output numbers: {e}"

    # 3. Validate Number of Pairs
    if len(output_pairs) != n:
        return False, f"Invalid number of pairs: expected {n}, got {len(output_pairs)}."

    # 4. Validate Consistent Sum
    if not output_pairs:
        return False, "No pairs found in output."
        
    # FIX: target_sum should be the sum of the FIRST pair, not the list of pairs
    target_sum = sum(output_pairs[0])
    for pair in output_pairs:
        if sum(pair) != target_sum:
            return False, f"Inconsistent pair sum: expected {target_sum}, but got {sum(pair)} for pair {pair}."

    # 5. Validate Elements Usage
    output_numbers = []
    for pair in output_pairs:
        output_numbers.extend(pair)
    
    if Counter(output_numbers) != Counter(input_numbers):
        return False, "Output numbers do not match input numbers exactly."

    return True, f"Response is **VALID**. All {n} pairs sum to {target_sum}."

def run_validator_from_files(input_filename="test_data.txt", output_filename="output.txt"):
    """
    Reads input from test_data.txt and output from output.txt, then validates.
    """
    try:
        with open(input_filename, 'r') as f:
            input_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        sys.exit(1)

    try:
        with open(output_filename, 'r') as f:
            output_content = f.read()
    except FileNotFoundError:
        # If output file is missing, we cannot validate.
        print(f"Error: Output file '{output_filename}' not found. Cannot validate response.")
        sys.exit(1)

    is_valid, message = validate_response(input_content, output_content)
    print(f"--- Validation Result ---")
    print(f"Input used: \n{input_content.strip()}")
    print(f"Output used: \n{output_content.strip()}")
    print(f"\nResult: {is_valid}, Message: {message}")

if __name__ == "__main__":
    run_validator_from_files()
