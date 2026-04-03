#!/usr/bin/env python3

"""

Locates and replaces a string in the heap of a running process.

Usage: ./read_write_heap.py pid search_string replace_string

"""


import sys


def print_usage_and_exit():

    """Prints usage information and exits with status 1."""

    print("Usage: read_write_heap.py pid search_string replace_string")

    sys.exit(1)


def main():

    # Validate arguments

    if len(sys.argv) != 4:

        print_usage_and_exit()


    pid = sys.argv[1]

    search_string = sys.argv[2]

    replace_string = sys.argv[3]


    maps_file = f"/proc/{pid}/maps"

    mem_file = f"/proc/{pid}/mem"


    heap_start = None

    heap_end = None


    # Step 1: Parse the maps file to find the heap boundaries

    try:

        with open(maps_file, 'r') as m:

            for line in m:

                if "[heap]" in line:

                    # The line looks like: 01000000-01021000 rw-p 00000000 00:00 0 [heap]

                    address_range = line.split(' ')[0]

                    start_str, end_str = address_range.split('-')

                    heap_start = int(start_str, 16)

                    heap_end = int(end_str, 16)

                    break

    except Exception as e:

        print(f"Error reading {maps_file}: {e}")

        sys.exit(1)


    if heap_start is None:

        print("Error: Could not find [heap] in the maps file.")

        sys.exit(1)


    print(f"[*] Found heap bounds: {hex(heap_start)} - {hex(heap_end)}")


    # Step 2: Open the mem file to read and write

    try:

        # Open in binary read/write mode

        with open(mem_file, 'rb+') as mem:

            # Seek to the start of the heap

            mem.seek(heap_start)

            

            # Read the entire heap

            heap_data = mem.read(heap_end - heap_start)


            # Step 3: Search for the string in the heap data

            search_bytes = search_string.encode('ascii')

            offset = heap_data.find(search_bytes)


            if offset == -1:

                print(f"Error: Can't find '{search_string}' in the heap.")

                sys.exit(1)


            absolute_address = heap_start + offset

            print(f"[*] Found '{search_string}' at offset {hex(offset)}")

            print(f"[*] Absolute memory address: {hex(absolute_address)}")


            # Step 4: Prepare the replacement bytes

            replace_bytes = replace_string.encode('ascii')

            

            # To prevent memory corruption (buffer overflow), handle length differences

            if len(replace_bytes) > len(search_bytes):

                # Truncate if the new string is longer than the old buffer

                replace_bytes = replace_bytes[:len(search_bytes)]

                print("[!] Warning: Replace string truncated to fit buffer.")

            elif len(replace_bytes) < len(search_bytes):

                # Pad with null bytes if the new string is shorter

                # This ensures we don't leave trailing garbage characters (e.g., "marouaon")

                replace_bytes += b'\x00' * (len(search_bytes) - len(replace_bytes))


            # Step 5: Write the new string back to memory

            mem.seek(absolute_address)

            mem.write(replace_bytes)

            

            print(f"[*] Successfully replaced '{search_string}' with '{replace_string}'.")


    except PermissionError:

        print(f"Error: Permission denied. Did you run with sudo?")

        sys.exit(1)

    except Exception as e:

        print(f"Error accessing {mem_file}: {e}")

        sys.exit(1)


if __name__ == "__main__":

    main()
