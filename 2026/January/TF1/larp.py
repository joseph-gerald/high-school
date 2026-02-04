import matplotlib.pyplot as plt
import argparse
import sys
import time

def load_data(filename):
    """Reads the file and returns a list of integers."""
    data = []
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                line = line.strip()
                if line.isdigit():
                    data.append(int(line))
                else:
                    # Handle cases where line might be empty or non-numeric
                    if line: 
                        print(f"Warning: Skipping non-integer value at line {i}: '{line}'")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    return data

def main():
    # 1. Setup Command Line Arguments
    parser = argparse.ArgumentParser(description='Simulate Arduino Analog Replay from a text file.')
    
    parser.add_argument('--file', type=str, default='larp.txt', 
                        help='The text file containing analog values (default: larp.txt)')
    parser.add_argument('--start', type=int, default=0, 
                        help='Starting index of the data (default: 0)')
    parser.add_argument('--end', type=int, default=None, 
                        help='Ending index of the data (default: End of file)')
    parser.add_argument('--delay', type=float, default=0.005, 
                        help='Delay in seconds between updates (default: 0.05)')
    parser.add_argument('--window', type=int, default=100, 
                        help='How many points to show on screen at once (scrolling width). Set 0 to show all.')

    args = parser.parse_args()

    # 2. Load and Slice Data
    full_data = load_data(args.file)
    
    # Handle array slicing
    start_idx = max(0, args.start)
    end_idx = args.end if args.end is not None else len(full_data)
    
    # Validate bounds
    if start_idx >= len(full_data):
        print(f"Error: Start index {start_idx} is out of bounds (File has {len(full_data)} lines).")
        sys.exit(1)
        
    subset_data = full_data[start_idx:end_idx]
    
    print(f"Loaded {len(full_data)} points.")
    print(f"Replaying range [{start_idx}:{end_idx}] ({len(subset_data)} points).")
    print("Press Ctrl+C in the terminal to stop.")

    # 3. Setup the Plot
    plt.ion() # Turn on interactive mode
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'g-', linewidth=1.5) # 'g-' = green line
    
    # Setup static chart properties
    ax.set_ylim(0, 1024) # Analog range
    ax.set_ylabel('Analog Value (0-1024)')
    ax.set_xlabel('Sample Index')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    x_data = []
    y_data = []

    # 4. Animation Loop
    try:
        for i, value in enumerate(subset_data):
            # The actual index relative to the original file
            real_index = start_idx + i
            
            x_data.append(real_index)
            y_data.append(value)

            # Update Line Data
            line.set_data(x_data, y_data)
            
            # Handle Windowing/Scrolling
            # If window is set (greater than 0) and we have more points than the window
            if args.window > 0 and len(x_data) > args.window:
                ax.set_xlim(real_index - args.window, real_index)
                # Optional: Remove old data from memory to keep it fast if running for hours
                # x_data.pop(0)
                # y_data.pop(0)
            else:
                # Expand x-axis to fit data
                ax.set_xlim(start_idx, max(start_idx + args.window, real_index + 1))

            ax.set_title(f"Live Replay - Index: {real_index} | Value: {value}")
            
            # Draw and Pause
            # pause() updates the GUI events
            plt.pause(args.delay)

    except KeyboardInterrupt:
        print("\nReplay stopped by user.")
    
    print("Replay finished.")
    plt.ioff() # Turn off interactive mode
    plt.show() # Keep the window open after script finishes

if __name__ == "__main__":
    main()