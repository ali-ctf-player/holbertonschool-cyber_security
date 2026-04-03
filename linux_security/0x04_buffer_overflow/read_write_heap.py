#!/usr/bin/python3
import sys
"""It is bufffer overflow"""

def usage():
    print("Usage:python3 read_write_heap.py [PID] [SEARCH_STRING] [REPLACE_STRING]")


def main():
    if len(sys.argv) != 4:
        usage()
    
    pid = sys.argv[1]
    search_string = sys.argv[2]
    replace_string = sys.argv[3]

    maps = f"/proc/{pid}/maps"
    mem = f"/proc/{pid}/mem"

    heap_s = None
    heap_e = None


    try:
        with open(maps, 'r') as map:
            for line in map:
                if "[heap]" in line:
                    addr_range = line.split(' ')[0]
                    start_str, end_str = addr_range.split('-')
                    heap_s = int(start_str,16)
                    heap_e = int(end_str,16)

                    break
    except Exception as e:
        sys.exit(1)

    
    if heap_s is None:
        sys.exit(1)
    

    try:
        with open(mem,'rb+') as mem_file:
            mem_file.seek(heap_s)

            heap_data = mem_file.read(heap_e - heap_s)

            search_bytes = search_string.encode('ascii')
            offset = heap_data.find(search_bytes)

            if offset == -1:
                sys.exit(1)

            absolute_addr = heap_s + offset

            print(f"[*] Found '{search_string}' at offset {hex(offset)}")
            print(f"[*] Absolute memory address: {hex(absolute_addr)}")

            replace_bytes = replace_string.encode('ascii')

            if len(replace_bytes) > len(search_bytes):
                replace_bytes = replace_bytes[:len(search_bytes)]

            elif len(replace_bytes) < len(search_bytes):
                replace_bytes += b'\x00' * (len(search_bytes) - len(replace_bytes))
            
            mem_file.seek(absolute_addr)
            mem_file.write(replace_bytes)
    except PermissionError:
        sys.exit(1)

    except Exception as e:
        sys.exit(1)


if __name__ == "__main__":
    main()
