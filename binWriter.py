#!/usr/bin/env python3
import argparse
import os
import sys

def write_pattern(file_obj, size, pattern_bytes):
    # Repeat the pattern to fill exactly `size` bytes
    length = len(pattern_bytes)
    if length == 0:
        return
    full_repeats = size // length
    remainder = size % length
    file_obj.write(pattern_bytes * full_repeats + pattern_bytes[:remainder])

def write_hex_string(file_obj, hex_string):
    # Write raw bytes from a hex string (any length)
    # strip spaces & convert
    clean = hex_string.replace(" ", "")
    try:
        data = bytes.fromhex(clean)
    except ValueError:
        raise SystemExit("Error: Invalid hex string for --hex-input")
    file_obj.write(data)

def write_integers(file_obj, integers, length, endian):
    # Write each integer with .to_bytes()
    for num in integers:
        if num < 0 or num >= (1 << (8 * length)):
            raise SystemExit(
                f"Error: Integer {num} doesn't fit in {length} bytes"
            )
        file_obj.write(num.to_bytes(length, byteorder=endian))

def main():
    parser = argparse.ArgumentParser(
        description="Binary file generator (enhanced).",
        allow_abbrev=True,
    )

    parser.add_argument(
        "-f", "--filename", required=True, help="Output file name"
    )

    group_mode = parser.add_mutually_exclusive_group(required=True)

    # Original fill/random options
    group_mode.add_argument(
        "-R", "--random",
        action="store_true",
        help="Fill the file with random bytes"
    )
    group_mode.add_argument(
        "-F", "--fill",
        help="Hex byte used for single-byte fill (e.g. 00, FF)"
    )

    # New modes
    group_mode.add_argument(
        "-P", "--pattern",
        help="Hex pattern to repeat for file (e.g. DEADBEEF)"
    )
    group_mode.add_argument(
        "-H", "--hex-input",
        help="Write raw hex string to file (no padding)"
    )
    group_mode.add_argument(
        "-I", "--integers", nargs="+",
        type=int,
        help="List of integers to write"
    )

    # Shared options
    parser.add_argument(
        "-s", "--size", type=int,
        help="Size of file in bytes (required for fill/random/pattern modes)"
    )

    parser.add_argument(
        "--int-bytes", type=int, default=4,
        help="Byte length per integer (for --integers) (default: 4)"
    )
    parser.add_argument(
        "--endian", choices=["little", "big"], default="little",
        help="Endian for integer writes (default: little)"
    )

    args = parser.parse_args()

    # Ensure size is valid for modes that need it
    if args.random or args.fill or args.pattern:
        if args.size is None:
            raise SystemExit("Error: --size is required for this mode")

    with open(args.filename, "wb") as f:

        # Random fill
        if args.random:
            f.write(os.urandom(args.size))
            print(f"Written {args.size} random bytes.")

        # Single-byte fill
        elif args.fill:
            # Parse fill byte
            try:
                b = int(args.fill, 16)
                if b < 0 or b > 0xFF:
                    raise ValueError
            except ValueError:
                raise SystemExit("Error: --fill must be hex 00–FF")
            write_pattern(f, args.size, bytes([b]))
            print(f"Written {args.size} bytes of fill {args.fill}.")

        # Pattern mode
        elif args.pattern:
            # pattern string -> bytes
            clean = args.pattern.replace(" ", "")
            try:
                pattern_bytes = bytes.fromhex(clean)
            except ValueError:
                raise SystemExit("Error: Invalid hex pattern")
            write_pattern(f, args.size, pattern_bytes)
            print(f"Written {args.size} bytes of repeating pattern {args.pattern}.")

        # Raw hex input
        elif args.hex_input:
            write_hex_string(f, args.hex_input)
            print(f"Written raw hex input.")

        # Integer list write
        elif args.integers:
            write_integers(
                f, args.integers, args.int_bytes, args.endian
            )
            print(
                f"Written {len(args.integers)} ints "
                f"({args.int_bytes} bytes each, {args.endian} endian)."
            )

    print("Done!")

if __name__ == "__main__":
    main()
