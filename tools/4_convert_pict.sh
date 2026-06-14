#!/usr/bin/env bash
# Step 4: Convert classic PICT resources to PNG using ImageMagick.
# Resource-fork PICTs lack the 512-byte file header that QuickTime expects,
# so we prepend 512 zero bytes before handing each one to `convert`.
# Usage: ./4_convert_pict.sh res/PICT png
set -e
IN="$1"; OUT="$2"; mkdir -p "$OUT"
for f in "$IN"/*.bin; do
  id=$(basename "$f" .bin)
  head -c 512 /dev/zero > _hdr.bin
  cat _hdr.bin "$f" > _cur.pict
  convert _cur.pict "$OUT/$id.png" 2>/dev/null || echo "skip $id"
done
rm -f _hdr.bin _cur.pict
echo "PICTs -> $OUT"
