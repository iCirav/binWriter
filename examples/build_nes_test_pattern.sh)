#!/bin/bash
# -----------------------------
# Build NES Test Pattern ROM (Bash)
# -----------------------------

# Filenames
HEADER=header.bin
PRG_PROGRAM=prg_program.bin
PRG_PADDING=prg_padding.bin
PRG_RESET=prg_reset.bin
PRG=prg.bin
CHR=chr.bin
ROM=test_pattern.nes

# 1️⃣ Write iNES header
python binWriter.py --hex-input "4E45531A010100000000000000000000" -f $HEADER

# 2️⃣ Write PRG program (6502 code)
PROGRAM_HEX="78F8A2008E0020A2008E0120A9028D2000A9028D2001A9FF8D2002A9FF8D2003A200A000BD00209D0002CAD0F54C0080"
python binWriter.py --hex-input $PROGRAM_HEX -f $PRG_PROGRAM

# 3️⃣ Calculate PRG padding
PROGRAM_BYTES=$(stat -c%s "$PRG_PROGRAM")
PADDING_SIZE=$((16384 - PROGRAM_BYTES - 2))

# 4️⃣ Create PRG padding
python binWriter.py -s $PADDING_SIZE --fill 00 -f $PRG_PADDING

# 5️⃣ Create reset vector ($8000)
python binWriter.py --hex-input "0080" -f $PRG_RESET

# 6️⃣ Combine PRG ROM
cat $PRG_PROGRAM $PRG_PADDING $PRG_RESET > $PRG

# 7️⃣ Create CHR ROM (8 KB blank tiles)
python binWriter.py -s 8192 --fill 00 -f $CHR

# 8️⃣ Combine full NES ROM
cat $HEADER $PRG $CHR > $ROM

# 9️⃣ Done
ls -lh $ROM
