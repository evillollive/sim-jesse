# SimJesse! web re-creation

A faithful, browser-based re-creation of **SimJesse! 1.0 "The Digital Demagogue"**, a Mac app from 1993 (© Mark Hayes, ccmlh@it.bu.edu, freeware). The original was a compiled classic Mac application that played digitized Jesse Jackson speech clips, stringing them together in a random but grammar-aware order to generate endless pseudo-speeches.

The original app can no longer run on any modern hardware. I've been a fan of SimJesse since it first came out in 1993, and only recently found a copy on an old Zip disk. That's how we were able to revive and modernize it: extracting every resource from the Mac resource fork, decoding the 1993-era MACE 3:1 audio, recovering the artwork, and reverse-engineering the speech algorithm directly from the compiled 68k machine code.

This project is a tribute to the enduring power of Jesse Jackson's oratory. Even scrambled into random fragments, the conviction and rhythm of his voice come through.

## Run it

Open `index.html` in any modern browser. No build step, no server, no dependencies. Every sound and image is embedded in the single HTML file. It also works as a GitHub Pages site: enable Pages on the repo root and it serves `index.html` directly.

The classic Apple / File / Edit menu bar is reproduced from the app's original MENU resources. **About SimJesse!** is under the Apple menu. The three buttons match the original:

- **Run, Jesse, Run!** generates continuous speeches until you press Stop. On Stop, Jesse says "no more!"
- **Music** loops instrument and musician samples.
- **Nature** loops nature sounds seamlessly.

## What's in here

```
index.html                     The original re-creation (self-contained, audio + art embedded)
v2/index.html                  Version 2.0 "The Dream Machine" (see below)
original/
  SimJesse 1.0.zip             The original Mac app, with resource fork preserved
  SimJesse.rsrc                The raw resource fork, extracted (1.3 MB)
extracted/
  sounds_snd_raw/              All 123 original 'snd ' resources (raw, named by id+name)
  sounds_wav/                  All 123 sounds decoded to WAV
  images_pict_raw/             All 31 original PICT resources (raw)
  images_png/                  Those PICTs converted to PNG
  other_resources/             Everything else: CODE, DATA, DITL, DLOG, WIND, MENU, etc.
tools/
  1_extract_resource_fork.py   AppleDouble  -> SimJesse.rsrc
  2_dump_resources.py          SimJesse.rsrc -> extracted resource tree
  3_decode_sounds.py           'snd ' resources -> WAV (handles MACE 3:1 + raw PCM)
  4_convert_pict.sh            PICT resources  -> PNG (ImageMagick)
```

## How it was reverse-engineered

1. **Resource fork.** Classic Mac files keep their content in a resource fork. Zipping the app on a Mac preserves the fork as an AppleDouble file. `tools/1` reads that and writes `SimJesse.rsrc`.
2. **Resources.** `tools/2` parses the resource map and dumps every resource by type. (Gotcha: reference-list entries are 12 bytes each, not 8. Missing the 4-byte reserved handle silently corrupts everything.)
3. **Sounds.** 120 of the 123 clips are **MACE 3:1** compressed (Apple's old `'snd '` codec, compressionID `3`). The other 3 are uncompressed 8-bit PCM at ~22 kHz. `tools/3` wraps the MACE data in an AIFF-C (`MAC3`) container and decodes with ffmpeg.
4. **Art.** PICT resources from a resource fork lack the 512-byte header QuickTime expects. `tools/4` prepends it and converts with ImageMagick. The portrait, backdrop, button icons, and masthead all come from here.
5. **Sound list.** The `DATA` resource holds the master sound list as length-prefixed Pascal strings: speech words listed alphabetically (indices 0-110), followed by 12 non-speech sounds (indices 111-122) that feed the Music and Nature buttons.
6. **Speech engine.** The sentence-generation logic lives in the compiled 68k Motorola machine code inside `CODE/2.bin` (11 KB). To recover it, we traced every `GetNamedResource('snd ', name)` call to map the 123 sound handles to their A5-register offsets, then followed all references through the speech function (0x0BC6-0x1A40). The function picks one of 7 patterns via a random branch, plays a hardcoded sequence of clips with randomized sub-selections, then runs a shared coda. The startup function at 0x02BE revealed that `lou` ("Here comes Jesse Jackson") plays once at launch. All 7 patterns, their exact sound pools, and the coda were ported to JavaScript.

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

## Fidelity notes

**From the original resources (confirmed):** the name "SimJesse! The Digital Demagogue", the "Run, Jesse, Run!" button, the 1993 Mark Hayes credit and Captain Crunch dedication, the three-button layout, all artwork, all 123 sounds, the master sound list and the speech-vs-music/nature grouping, and the "no more!" stop sound.

**Faithfully reverse-engineered from the original binary:** the sentence-generation algorithm was traced through the compiled 68k machine code. All 7 speech patterns and the shared coda were identified and ported to JavaScript, using the exact same sound pools and branching logic as the original.

**Event sounds:** `lou` ("Here comes Jesse Jackson") is the original startup sound, now available in Music mode. `noNo` ("no more!") plays when you stop the Jesse loop. Both are reserved from the speech pool.

---

## Version 2.0: "The Dream Machine"

As an experiment and tribute to the fun and creativity of the classic app, we built a modern reimagining at `v2/index.html`. Same 123 original sound clips, same 7 speech patterns from the 1993 binary, but wrapped in a new experience with three modes:

- **Run, Jesse, Run!** The classic speech generator with scrolling animated captions and a vibe selector that shifts the mood (Hopeful, Fired Up, Reflective, Celebration).
- **Compose.** Build your own Jesse speech by tapping clips onto a timeline. Play it back, then share your creation via link.
- **Remix.** Jesse's speeches play over synthesized beats. Four genres (Gospel, Lo-fi, Jazz, Hip-hop), each with kick, snare, hi-hat, bass, and the original percussion samples layered on top. A tempo slider lets you dial the BPM.

Version 2.0 loads audio from the extracted WAV files rather than embedding base64. No build step, no dependencies, no server. Just open the HTML file.

---

## Credits

Original **SimJesse! 1.0** &copy; 1993 Mark Hayes (ccmlh@it.bu.edu) freeware, "Please distribute!" Dedicated to Captain Crunch, the Multicultural Caffeinated Cockatiel.

## License

This re-creation is licensed under the [GNU Affero General Public License v3.0](LICENSE).
