# Binary File Generator

A simple Python script to generate binary files of a specified size, either filled with a fixed byte or with random data. Useful for testing, padding, or simulating binary data.

![Screenshot of help screen](/assets/images/help.png)

---

## Features

- Generate a binary file of any size (in bytes)
- Fill the file with a specific byte (hexadecimal)
- Optionally fill the file with random data
- Simple command-line interface

---

## Requirements

- Python 3.x

No additional libraries are required beyond the Python standard library.

---

## Usage

Run the script from the command line:

```bash
python bin_generator.py -f <filename> -s <size> [--fill <hex_byte> | --random]
```

## Examples

Create a 1 KB file filled with 0xFF (default):
```
python bin_generator.py -f output.bin -s 1024
```

Create a 512-byte file filled with 0x00:
```
python bin_generator.py -f zero.bin -s 512 --fill 00
```

Create a 2 MB file with random data:
```
python bin_generator.py -f random.bin -s 2097152 --random
```
