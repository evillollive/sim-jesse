# Reverse-engineering notes

This page preserves the implementation detail behind the SimJesse! web re-creation. The short version: the original classic Mac app was recovered from an old Zip disk, its resource fork was extracted, and the speech generator was ported from compiled 68k code into JavaScript.

## What is preserved

**From the original resources:**

- The name **SimJesse! The Digital Demagogue**.
- The **Run, Jesse, Run!** button and three-button layout.
- The 1993 Mark Hayes credit, freeware distribution note, and Captain Crunch dedication.
- All artwork recovered from PICT resources.
- All 123 sound resources.
- The master sound list and speech/music/nature grouping.
- The `noNo` stop sound.

**Reverse-engineered from the original binary:**

- The sentence-generation algorithm inside the compiled 68k Motorola machine code.
- All seven speech patterns.
- Exact sound pools and branching logic.
- The shared coda.
- The startup `lou` sound, now available in Music mode.

## Resource recovery flow

1. **Resource fork.** Classic Mac files keep app resources in a resource fork. Zipping the app on a Mac preserved that fork as an AppleDouble file. `tools/1_extract_resource_fork.py` reads the AppleDouble file and writes `SimJesse.rsrc`.
2. **Resources.** `tools/2_dump_resources.py` parses the resource map and dumps every resource by type. One important gotcha: reference-list entries are 12 bytes each, not 8; missing the 4-byte reserved handle silently corrupts the parse.
3. **Sounds.** 120 of the 123 clips are **MACE 3:1** compressed, Apple's old `'snd '` codec with compression ID `3`. The other three are uncompressed 8-bit PCM at roughly 22 kHz. `tools/3_decode_sounds.py` wraps MACE data in an AIFF-C `MAC3` container and decodes it with `ffmpeg`.
4. **Art.** PICT resources from a resource fork lack the 512-byte header QuickTime expects. `tools/4_convert_pict.sh` prepends that header and converts the images with ImageMagick.
5. **Sound list.** The `DATA` resource holds the master sound list as length-prefixed Pascal strings: speech words listed alphabetically at indices 0-110, followed by 12 non-speech sounds at indices 111-122 for Music and Nature.
6. **Speech engine.** The sentence-generation logic lives in `CODE/2.bin`, an 11 KB compiled 68k code resource. The port traced every `GetNamedResource('snd ', name)` call to map the 123 sound handles to their A5-register offsets, then followed all references through the speech function at `0x0BC6-0x1A40`. The function picks one of seven patterns through a random branch, plays a hardcoded sequence of clips with randomized sub-selections, then runs a shared coda. The startup function at `0x02BE` revealed that `lou` ("Here comes Jesse Jackson") plays once at launch.

## Rebuild from scratch

```bash
# 1. Unzip the original archive. Use macOS, or any environment where AppleDouble survives.
unzip "original/SimJesse 1.0.zip" -d _work

# 2. Extract the resource fork and dump resources.
python3 tools/1_extract_resource_fork.py "_work/__MACOSX/._SimJesse 1.0" SimJesse.rsrc
python3 tools/2_dump_resources.py SimJesse.rsrc res

# 3. Decode sounds and convert artwork.
# Requires ffmpeg for audio and ImageMagick for PICT conversion.
python3 tools/3_decode_sounds.py res/snd wav
tools/4_convert_pict.sh res/PICT png
```

## Fidelity notes

The classic browser version intentionally preserves the original Mac app structure: menu names, buttons, artwork, sounds, and speech behavior are grounded in recovered resources or traced binary behavior. The web version adds browser-focused accessibility and security improvements, including explicit button types, ARIA state on controls, a live caption region, no embedded active third-party content, and a Content Security Policy in `index.html`.

Version 2.0 is intentionally less literal. It reuses the same sound clips and recovered speech patterns, then wraps them in a modern interface with captions, composition, link sharing, and synthesized remix beats.
