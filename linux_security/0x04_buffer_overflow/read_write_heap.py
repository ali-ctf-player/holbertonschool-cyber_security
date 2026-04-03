#!/usr/bin/python3
"""
This script locates and replaces a string in the heap of a running process.
"""
import sys


def main():
    """Main execution block"""
    # Basic check to ensure the user provides exactly 3 arguments
    if len(sys.argv) != 4:
        print("Usage: read_write_heap.py pid search_string replace_string")
        sys.exit(1)

    # 1. Get the inputs from the terminal
    pid = sys.argv[1]
    search_string = sys.argv[2].encode('ascii')
    replace_string = sys.argv[3].encode('ascii')

    # 2. Find exactly where the heap is located
    with open(f"/proc/{pid}/maps", 'r') as maps_file:
        for line in maps_file:
            if "[heap]" in line:
                address_range = line.split(' ')[0]
                start_hex, end_hex = address_range.split('-')
                heap_start = int(start_hex, 16)
                heap_end = int(end_hex, 16)
                break

    # 3. Read the memory, find the string, and overwrite it
    with open(f"/proc/{pid}/mem", 'r+b') as mem_file:
        mem_file.seek(heap_start)
        heap_data = mem_file.read(heap_end - heap_start)

        offset = heap_data.find(search_string)
        if offset == -1:
            print("Error: String not found in heap.")
            sys.exit(1)

        mem_file.seek(heap_start + offset)

        # Pad with null bytes if replacement string is shorter
        padded_replace = replace_string.ljust(len(search_string), b'\x00')
        mem_file.write(padded_replace)


if __name__ == "__main__":
    main()
