#!/usr/bin/env python3
"""
Step 2: Parse the Macintosh resource fork and dump every resource to disk,
grouped by 4-char type code (snd , PICT, CODE, DATA, DITL, MENU, ...).

Key detail: each entry in a resource reference list is 12 bytes
(id:2, nameOffset:2, attr+dataOffset:4, reserved handle:4). Missing the
4-byte reserved field is a classic parsing bug.

Usage: python3 2_dump_resources.py SimJesse.rsrc res/
"""
import struct, os, sys

def main(rsrc_path, outdir):
    rf = open(rsrc_path, "rb").read()
    dataOff, mapOff, dataLen, mapLen = struct.unpack(">IIII", rf[0:16])
    m = rf[mapOff:mapOff+mapLen]
    typeListOff, nameListOff = struct.unpack(">HH", m[24:28])
    numTypes = struct.unpack(">H", m[typeListOff:typeListOff+2])[0] + 1
    p = typeListOff + 2
    for _ in range(numTypes):
        t = m[p:p+4].decode("mac_roman", "replace"); p += 4
        cnt = struct.unpack(">H", m[p:p+2])[0] + 1; p += 2
        refOff = struct.unpack(">H", m[p:p+2])[0]; p += 2
        tdir = os.path.join(outdir, t.strip() or "BLANK")
        os.makedirs(tdir, exist_ok=True)
        rp = typeListOff + refOff
        for _ in range(cnt):
            rid, nameOff, attr_dataOff = struct.unpack(">hHI", m[rp:rp+8]); rp += 12
            do = attr_dataOff & 0x00FFFFFF
            name = ""
            if nameOff != 0xFFFF and (nameListOff+nameOff) < len(m):
                no = nameListOff + nameOff; nl = m[no]
                name = m[no+1:no+1+nl].decode("mac_roman", "replace")
            abspos = dataOff + do
            dlen = struct.unpack(">I", rf[abspos:abspos+4])[0]
            body = rf[abspos+4:abspos+4+dlen]
            safe = "".join(c if c.isalnum() else "_" for c in name)[:40]
            fn = os.path.join(tdir, f"{rid}{('_'+safe) if safe else ''}.bin")
            open(fn, "wb").write(body)
    print("done ->", outdir)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
