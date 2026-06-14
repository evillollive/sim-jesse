# SimJesse! web re-creation

A faithful, browser-based re-creation of **SimJesse! 1.0 "The Digital Demagogue"**, a Macintosh toy from 1993 (© Mark Hayes, ccmlh@it.bu.edu, freeware). The original was a compiled HyperCard-style application that played digitized Jesse Jackson speech clips, stringing them together in a random but grammar-aware order to generate endless pseudo-speeches.

This repo contains the working web version plus **everything extracted from the original app**, so the project can be picked up and worked on again at any time.

## Run it

Open `index.html` in any modern browser. No build step, no server, no dependencies, every sound and image is embedded in the single HTML file. (It also works as a GitHub Pages site: enable Pages on the repo root and it serves `index.html` directly.)

### Buttons (matching the original three)

- **Run, Jesse, Run!** (left) runs continuously, generating sentences from the speech clips until you press Stop. On Stop, Jesse says *"No more!"*.
- **Music** (middle) loops the instrument/musician samples (tomtom, cymbal, cowbell, bongo, drum solo).
- **Nature** (right) loops the nature samples (splash, wind, bubbles, stream).

The classic Apple / File / Edit menu bar is reproduced from the app's original MENU resources; **About SimJesse!** is under the Apple menu.

## What's in here

```
index.html                     The web app (self-contained: audio + art embedded)
original/
  SimJesse 1.0.zip             The original Mac app. The resource fork is preserved
                               inside the zip as an AppleDouble file (__MACOSX/._SimJesse 1.0).
                               IMPORTANT: keep it zipped — git does not preserve Mac
                               resource forks, so the loose file would lose all its data.
  SimJesse.rsrc                The raw resource fork, extracted (1.3 MB). This is the
                               real payload of the app.
extracted/
  sounds_snd_raw/              All 123 original 'snd ' resources (raw, named by id+name).
  sounds_wav/                  All 123 sounds decoded to WAV (see format notes below).
  images_pict_raw/             All 31 original PICT resources (raw).
  images_png/                  Those PICTs converted to PNG (logo, button icons, portrait, backdrop).
  other_resources/             Everything else by type: CODE, DATA, DITL, DLOG, WIND,
                               MENU, MBAR, BNDL, FREF, SIZE, icl8, ICN#, JesE.
tools/
  1_extract_resource_fork.py   AppleDouble  -> SimJesse.rsrc
  2_dump_resources.py          SimJesse.rsrc -> extracted resource tree
  3_decode_sounds.py           'snd ' resources -> WAV (handles MACE 3:1 + raw PCM)
  4_convert_pict.sh            PICT resources  -> PNG (ImageMagick)
```

## How it was reverse-engineered

1. **Resource fork.** Classic Mac files keep their content in a resource fork. Zipping the app on a Mac preserves the fork as an AppleDouble file. `tools/1` reads that and writes `SimJesse.rsrc`.
2. **Resources.** `tools/2` parses the resource map and dumps every resource by type. (Gotcha: reference-list entries are 12 bytes each — a 2-byte id, 2-byte name offset, a packed 1+3-byte attributes/data offset, and a 4-byte reserved handle. Using 8 bytes instead of 12 silently corrupts everything.)
3. **Sounds.** 120 of the 123 clips are **MACE 3:1** compressed (Apple's old `'snd '` compression, compressionID `3`; the compressed data is exactly `numFrames × 2` bytes). The other 3 are uncompressed 8-bit PCM at ~22 kHz. `tools/3` wraps the MACE data in a small AIFF-C (`MAC3`) container and decodes it with ffmpeg. Decoding to raw PCM and playing the still-compressed bytes is the bug to avoid — it produces fast, distorted noise.
4. **Art.** PICT resources from a resource fork lack the 512-byte header QuickTime expects; `tools/4` prepends it and converts with ImageMagick. The masthead, the three button icons (incl. the red STOP hand), Jesse's portrait, and the landscape backdrop all come from here.
5. **Grammar / sounds map.** The `DATA` resource holds the master sound list. Speech words are listed alphabetically; the 12 non-speech sounds are appended at the end (these feed the Music and Nature buttons). The exact event-to-sound wiring lives in the compiled `CODE` resources, which index the `DATA` list by position.

## Rebuild from scratch

```bash
# 1. unzip the original (on a Mac, or anywhere the AppleDouble survives)
unzip "original/SimJesse 1.0.zip" -d _work

# 2. extract the resource fork and dump resources
python3 tools/1_extract_resource_fork.py "_work/__MACOSX/._SimJesse 1.0" SimJesse.rsrc
python3 tools/2_dump_resources.py SimJesse.rsrc res

# 3. decode sounds (needs ffmpeg) and convert art (needs ImageMagick)
python3 tools/3_decode_sounds.py res/snd wav
tools/4_convert_pict.sh res/PICT png
```

The app's sound data and category mapping live inline in `index.html` in a `<script id="appdata">` JSON block (sound name → base64 WAV, plus the grammar categories and templates). That's the place to edit behavior.

## Fidelity notes (known vs. reconstructed)

**From the original resources (confirmed):** the name "SimJesse! The Digital Demagogue", the "Run, Jesse, Run!" button, the 1993 Mark Hayes credit and Captain Crunch dedication, the three-button layout, all artwork, all 123 sounds, the master sound list and the speech-vs-music/nature grouping, and the *"No more!"* Stop sound.

**Reconstructed (not byte-for-byte the original code):** the exact sentence-generation algorithm. The original logic is compiled machine code; the grammar here reproduces the "random but grammar-aware" feel rather than the precise original sequencing.

**Event sounds:** `intro` ("His name is Jesse Jackson") plays once at launch: in the browser it fires on the first interaction, since browsers block audio before a user gesture. `noNo` ("No more!") plays when you Stop the Jesse loop. Both are reserved from the random pool.

**Reserved / unused clips:** `aw` and `pip` exist in the app but are left out of the random pools (they were kept out of the master speech list in the original too). If their original trigger is ever identified, they can be wired in.

## Credits

Original **SimJesse! 1.0** © 1993 Mark Hayes (ccmlh@it.bu.edu) freeware, *"Please distribute!"* Dedicated to Captain Crunch, the Multicultural Caffeinated Cockatiel. This is a preservation / re-creation project.
