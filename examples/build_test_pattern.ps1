# -----------------------------
# Build NES Test Pattern ROM (PowerShell)
# -----------------------------

# Paths
$headerFile = "header.bin"
$prgProgramFile = "prg_program.bin"
$prgPaddingFile = "prg_padding.bin"
$prgResetFile = "prg_reset.bin"
$prgFile = "prg.bin"
$chrFile = "chr.bin"
$romFile = "test_pattern.nes"

# 1️⃣ Write iNES header (16 bytes)
python binWriter.py --hex-input "4E45531A010100000000000000000000" -f $headerFile

# 2️⃣ Write PRG program (6502 code for grid + beep)
$programHex = "78F8A2008E0020A2008E0120A9028D2000A9028D2001A9FF8D2002A9FF8D2003A200A000BD00209D0002CAD0F54C0080"
python binWriter.py --hex-input $programHex -f $prgProgramFile

# 3️⃣ Calculate PRG padding
$programBytes = (Get-Item $prgProgramFile).Length
$paddingSize = 16384 - $programBytes - 2  # 16KB PRG - program - reset vector

# 4️⃣ Create PRG padding
python binWriter.py -s $paddingSize --fill 00 -f $prgPaddingFile

# 5️⃣ Create reset vector ($8000)
python binWriter.py --hex-input "0080" -f $prgResetFile

# 6️⃣ Combine PRG ROM
$program = [System.IO.File]::ReadAllBytes($prgProgramFile)
$padding = [System.IO.File]::ReadAllBytes($prgPaddingFile)
$reset   = [System.IO.File]::ReadAllBytes($prgResetFile)
$prg = $program + $padding + $reset
[System.IO.File]::WriteAllBytes($prgFile, $prg)

# 7️⃣ Create CHR ROM (8 KB blank tiles)
python binWriter.py -s 8192 --fill 00 -f $chrFile

# 8️⃣ Combine full NES ROM
$header = [System.IO.File]::ReadAllBytes($headerFile)
$chr    = [System.IO.File]::ReadAllBytes($chrFile)
$rom    = $header + $prg + $chr
[System.IO.File]::WriteAllBytes($romFile, $rom)

# 9️⃣ Done
Write-Host "NES ROM created: $romFile"
Write-Host "Size:" (Get-Item $romFile).Length "bytes"
