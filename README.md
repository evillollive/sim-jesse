# SimJesse! web re-creation

A faithful, browser-based re-creation of **SimJesse! 1.0 "The Digital Demagogue"**, a Mac app from 1993 (© Mark Hayes, ccmlh@it.bu.edu, freeware). The original was a compiled classic Mac application that played digitized Jesse Jackson speech clips, stringing them together in a random but grammar-aware order to generate endless pseudo-speeches.

The original app can no longer run on any modern hardware. I've been a fan of SimJesse since it first came out in 1993, and only recently found a copy on an old Zip disk. That's how we were able to revive and modernize it: extracting every resource from the Mac resource fork, decoding the 1993-era MACE 3:1 audio, recovering the artwork, and reverse-engineering the speech algorithm directly from the compiled 68k machine code.

This repo contains the working web version plus **everything extracted from the original app**, so the project can be picked up and worked on again at any time.

## Run it

Open `index.html` in any modern browser. No build step, no server, no dependencies, every sound and image is embedded in the single HTML file. (It also works as a GitHub Pages site: enable Pages on the repo root and it serves `index.html` directly.)

### Buttons (matching the original three)

- **Run, Jesse, Run!** (left) runs continuously, generating sentences from the speech clips until you press Stop. On Stop, Jesse says *"no more!"*.
- **Music** (middle) loops instrument and musician samples.
- **Nature** (right) loops nature sounds seamlessly.

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
5. **Grammar / sounds map.** The `DATA` resource holds the master sound list as length-prefixed Pascal strings: speech words listed alphabetically (indices 0-110), followed by 12 non-speech sounds (indices 111-122) that feed the Music and Nature buttons.
6. **Speech engine.** The sentence-generation logic lives in the compiled 68k Motorola machine code inside `CODE/2.bin` (11 KB). To recover it, we traced every `GetNamedResource('snd ', name)` call to map the 123 sound handles to their A5-register offsets, then followed all references to those handles through the speech function (0x0BC6-0x1A40). The function picks one of 7 patterns via a random branch, plays a hardcoded sequence of clips with randomized sub-selections, then runs a shared "coda" (noise, optional iKnow/and/now/asJesusSaid). The startup function at 0x02BE revealed that `lou` ("Here comes Jesse Jackson") plays once at launch, before `intro`. All 7 patterns, their exact sound pools, and the coda were ported to JavaScript.

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

The app's sound data and category mapping live inline in `index.html` in a `<script id="appdata">` JSON block (sound name to base64 WAV, plus category pools). The speech engine itself is hardcoded JavaScript that faithfully reproduces the original's 7 patterns.

## Fidelity notes (known vs. reconstructed)

**From the original resources (confirmed):** the name "SimJesse! The Digital Demagogue", the "Run, Jesse, Run!" button, the 1993 Mark Hayes credit and Captain Crunch dedication, the three-button layout, all artwork, all 123 sounds, the master sound list and the speech-vs-music/nature grouping, and the *"No more!"* Stop sound.

**Faithfully reverse-engineered from the original binary:** the sentence-generation algorithm was traced through the compiled 68k Macintosh machine code. All 7 speech patterns and the shared coda were identified and ported to JavaScript, using the exact same sound pools and branching logic as the original.

**Event sounds:** `lou` ("Here comes Jesse Jackson") plays as the startup sound in the original app; in the browser it's available in Music mode. `intro` plays once on first interaction, since browsers block audio before a user gesture. `noNo` ("no more!") plays when you Stop the Jesse loop. All three are reserved from the speech pool.

**Reserved / unused clips:** `pip` exists in the app but is left out of the random pools (it was kept out of the master speech list in the original too). `aw` plays in Music mode, matching the original binary where it appears in the music function. If `pip`'s original trigger is ever identified, it can be wired in.

## Credits

Original **SimJesse! 1.0** &copy; 1993 Mark Hayes (ccmlh@it.bu.edu) freeware, *"Please distribute!"* Dedicated to Captain Crunch, the Multicultural Caffeinated Cockatiel. This is a preservation / re-creation project.

## License

This re-creation is licensed under the [GNU Affero General Public License v3.0](LICENSE).
