#!/usr/bin/env python3
"""
Step 3: Decode the classic Mac 'snd ' resources to WAV.

Most SimJesse clips (120 of 123) are MACE 3:1 compressed (an old Apple
codec, compressionID == 3). The remaining 3 are uncompressed 8-bit PCM.

For MACE clips we rebuild a tiny AIFF-C container with compression type
'MAC3' and let ffmpeg's mace3 decoder do the work. ffmpeg is required.

Usage: python3 3_decode_sounds.py res/snd/ wav/
"""
import struct, glob, os, subprocess, wave, re, sys

def u16(b,o): return struct.unpack('>H', b[o:o+2])[0]
def u32(b,o): return struct.unpack('>I', b[o:o+4])[0]
def s16(b,o): return struct.unpack('>h', b[o:o+2])[0]

def sound_header_offset(b):
    fmt = u16(b,0); p = 2
    if fmt == 1: ndf = u16(b,p); p += 2 + ndf*6
    else: p += 2
    nc = u16(b,p); p += 2
    for _ in range(nc):
        cmd = u16(b,p); par2 = u32(b,p+4); p += 8
        if (cmd & 0x7FFF) in (0x50, 0x51): return par2   # soundCmd / bufferCmd
    return None

def make_aifc(frames, rate_ext10, data):
    comm = struct.pack('>h',1)+struct.pack('>I',frames)+struct.pack('>h',8)+rate_ext10+b'MAC3'
    cn = bytes([11])+b'MACE 3-to-1';  cn += b'\x00' if len(cn)%2 else b''
    comm += cn
    fver = b'FVER'+struct.pack('>I',4)+struct.pack('>I',0xA2805140)
    comm_chunk = b'COMM'+struct.pack('>I',len(comm))+comm
    ssnd_body = struct.pack('>I',0)*2+data;  ssnd_body += b'\x00' if len(ssnd_body)%2 else b''
    ssnd = b'SSND'+struct.pack('>I',len(ssnd_body))+ssnd_body
    fb = b'AIFC'+fver+comm_chunk+ssnd
    return b'FORM'+struct.pack('>I',len(fb))+fb

def main(snd_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    ok = 0
    for f in sorted(glob.glob(os.path.join(snd_dir, '*.bin'))):
        clean = re.sub(r'^\d+_?', '', os.path.basename(f)[:-4])
        b = open(f,'rb').read(); h = sound_header_offset(b)
        if h is None: continue
        enc = b[h+20]; rate = u32(b,h+8)/65536.0
        out = os.path.join(out_dir, clean+'.wav')
        if enc == 0x00:                                   # standard 8-bit PCM
            length = u32(b,h+4); pcm = b[h+22:h+22+length]
            w = wave.open(out,'wb'); w.setnchannels(1); w.setsampwidth(1)
            w.setframerate(int(round(rate))); w.writeframes(pcm); w.close(); ok += 1
        elif enc == 0xFE and s16(b,h+56) == 3:            # MACE 3:1
            nf = u32(b,h+22); data = b[h+64:h+64+nf*2]; rate_ext = b[h+26:h+36]
            open('_tmp.aifc','wb').write(make_aifc(nf*6, rate_ext, data))
            subprocess.run(['ffmpeg','-y','-v','error','-i','_tmp.aifc','-ac','1',
                            '-acodec','pcm_u8', out], check=True)
            ok += 1
    if os.path.exists('_tmp.aifc'): os.remove('_tmp.aifc')
    print(f"decoded {ok} sounds -> {out_dir}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
