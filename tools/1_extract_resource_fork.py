#!/usr/bin/env python3
"""
Step 1: Extract the Macintosh resource fork from the original app.

Classic Mac apps store everything in a "resource fork". When the file is
zipped on a Mac, the fork is preserved inside an AppleDouble file named
"._SimJesse 1.0" under the __MACOSX folder. This reads that AppleDouble
container and writes the raw resource fork to SimJesse.rsrc.

Usage: python3 1_extract_resource_fork.py "._SimJesse 1.0" SimJesse.rsrc
"""
import struct, sys

def main(ad_path, out_path):
    data = open(ad_path, "rb").read()
    magic, = struct.unpack(">I", data[0:4])
    assert magic == 0x00051607, "not an AppleDouble file"
    nent, = struct.unpack(">H", data[24:26])
    off = 26
    for _ in range(nent):
        eid, eoff, elen = struct.unpack(">III", data[off:off+12]); off += 12
        if eid == 2:  # entry id 2 = resource fork
            open(out_path, "wb").write(data[eoff:eoff+elen])
            print(f"wrote {out_path} ({elen} bytes)")
            return
    print("no resource fork found")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
