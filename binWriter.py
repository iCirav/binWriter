#!/usr/bin/env python3

import argparse
import os

def binWriter(filename, size, fill_byte=None, use_random=False):

    if use_random:
        # Generate size bytes of random data
        padded_bytes = os.urandom(size)
    else:
        # Fill the entire file with the fill byte
        padded_bytes = bytes([fill_byte]) * size

    with open(filename, "wb") as file_obj:
        file_obj.write(padded_bytes)


def main():
    parser = argparse.ArgumentParser(
        description="Binary file generator.",
        allow_abbrev=True
    )

    parser.add_argument(
        "-f", "--filename",
        required=True,
        help="Name of the file to create"
    )

    parser.add_argument(
        "-s", "--size",
        required=True,
        type=int,
        help="Size of the file in bytes"
    )

    # --- Mutually exclusive options: fill or random ---
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-F", "--fill",
        default="FF",
        help="Hex byte used for padding (default: FF). Example: --fill 00"
    )

    group.add_argument(
        "-R", "--random",
        action="store_true",
        help="Fill the file with random data instead of a fixed byte"
    )

    args = parser.parse_args()

    # If using random, ignore fill
    if args.random:
        fill_byte = None
    else:
        # Convert fill byte from hex to integer
        try:
            fill_byte = int(args.fill, 16)
            if not (0 <= fill_byte <= 0xFF):
                raise ValueError
        except ValueError:
            raise SystemExit("Error: --fill must be a valid hex byte (00–FF).")

    print("Filename:", args.filename)
    print("Size:", args.size)
    print("Mode:", "Random" if args.random else f"Fill byte {args.fill}")

    binWriter(
        filename=args.filename,
        size=args.size,
        fill_byte=fill_byte,
        use_random=args.random
    )

if __name__ == "__main__":
    main()

