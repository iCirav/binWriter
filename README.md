# binWriter

`binWriter` is a **CLI-only Python utility** for generating binary files with precise control over their contents.  
It can create files filled with random data, fixed bytes, repeating byte patterns, raw hex input, or structured integer values with configurable endianness.

This tool is useful for:
- Binary format testing
- Firmware / file structure prototyping
- Fuzzing and data generation
- Embedded or reverse-engineering workflows

---

## Requirements

- Python 3.6+

No external dependencies.

---

## Usage

```bash
python binWriter.py -f <output_file> [mode options]
```

## Modes & Examples

1️⃣ Random Fill Mode - Fill a file with cryptographically secure random bytes.
```
python binWriter.py -f random.bin -s 1024 --random
```

---

2️⃣ Single-Byte Fill Mode
Fill a file with a single repeated byte value.

Fills the file with 0x00 bytes.
```
python binWriter.py -f zeros.bin -s 4096 --fill 00
```

Fills the file with 0xFF bytes.
```
python binWriter.py -f ff.bin -s 256 --fill FF
```

---

3️⃣ Pattern Fill Mode (NEW)

Fill a file with a repeating multi-byte hex pattern.
```
python binWriter.py -f pattern.bin -s 1024 --pattern DEADBEEF
```
Spaces in the pattern are allowed:
```
python binWriter.py -f pattern.bin -s 64 --pattern "CA FE BA BE"
```

---

4️⃣ Raw Hex String Input (NEW)

Write an exact sequence of bytes from a hex string.
No padding or size argument is required.

```
python binWriter.py -f raw.bin --hex-input "00 FF 12 34 56 78"
```
The output file will contain exactly those bytes in that order.

---

5️⃣ Endian-Aware Integer Writes (NEW)

Write a list of integers using a fixed byte width and specified endianness.

```
python binWriter.py -f ints_le.bin -I 1 256 65535 --int-bytes 4 --endian little
```

```
python binWriter.py -f ints_be.bin -I 1 256 65535 --int-bytes 4 --endian big
```
Each integer is written using Python’s to_bytes() method.

Notes:

Integers must fit in the selected byte width

Default integer size is 4 bytes

Default endianness is little

---

## Full Argument Reference
Required

-f, --filename
Output file name

Mode Selection (exactly one required)

-R, --random
Fill with random bytes

-F, --fill <hex>
Single-byte hex fill (e.g. 00, FF)

-P, --pattern <hex>
Repeating hex pattern (e.g. DEADBEEF)

-H, --hex-input <hex>
Write raw hex bytes

-I, --integers <int> [int ...]
Write a list of integers

Shared Options

-s, --size <bytes>
Required for random / fill / pattern modes

--int-bytes <n>
Byte width per integer (default: 4)

--endian {little,big}
Endianness for integer writes (default: little)

---

## Examples

Create a 1MB test image filled with a repeating signature:
```
python binWriter.py -f image.bin -s 1048576 -P AABBCCDD
```

Create a binary header from integers:
```
python binWriter.py -f header.bin -I 0xDEADBEEF 1024 64 --int-bytes 4 --endian big
```

Write a magic number followed by version bytes:
```
python binWriter.py -f magic.bin --hex-input "4D 41 47 49 43 01 00"
```

---

## License

MIT License

---

## Author

Originally by iCirav
Enhanced functionality added via community contributions.
