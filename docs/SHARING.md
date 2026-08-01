# Sharing SimJesse!

SimJesse is easiest to share as a tiny preservation story: a 1993 Mac speech toy recovered from an old Zip disk, decoded from classic Mac resources, and made playable in a browser.

## Positioning

**Short pitch:** SimJesse! is a browser re-creation of a 1993 classic Mac freeware app that generated endless pseudo-speeches from digitized Jesse Jackson clips.

**Longer pitch:** This repo preserves SimJesse! 1.0, "The Digital Demagogue," by extracting the original Mac resource fork, decoding MACE 3:1 audio, converting PICT artwork, and porting the original 68k speech-generation algorithm into JavaScript. It includes a faithful single-file recreation plus a modern "Dream Machine" version with compose and remix modes.

## Who it is for

| Audience | Angle |
| --- | --- |
| Classic Mac and retrocomputing fans | A small, playable 1993 Mac app preserved without an emulator |
| Web preservation communities | Resource-fork assets and original behavior carried into static HTML |
| Creative coders and audio hackers | Speech collage, MACE decoding, and Web Audio remix experiments |
| Reverse engineers | Concrete notes on parsing resources and tracing compiled 68k behavior |
| Weird web toy collectors | A zero-install browser oddity with a strong origin story |

## Demo script

1. Open <https://evillollive.github.io/sim-jesse/>.
2. Click **Run, Jesse, Run!** and let the reconstructed speech generator run for 15-20 seconds.
3. Stop it and point out the original "no more!" stop sound.
4. Try **Music** and **Nature** to show the recovered non-speech samples.
5. Open <https://evillollive.github.io/sim-jesse/v2/>.
6. Show the three Dream Machine modes: Classic with vibe filters, Compose with copyable links, and Remix over generated beats.
7. Close with the preservation hook: 123 sounds, 31 PICT images, MACE 3:1 decoding, and seven speech patterns recovered from the original binary.

## Repository topic suggestions

Recommended GitHub topics:

```text
classic-mac
digital-preservation
retrocomputing
web-audio
reverse-engineering
macintosh
javascript
static-site
creative-coding
audio
```

## Channels to share

| Channel | Suggested angle |
| --- | --- |
| Mastodon / Bluesky / X | The quick preservation story plus the live demo link |
| Hacker News / Lobsters | The reverse-engineering and browser-preservation angle |
| Reddit `r/retrobattlestations` or `r/VintageApple` | Classic Mac freeware nostalgia and recovered resource assets |
| Reddit `r/creativecoding` | Speech collage, Web Audio, and remix mode |
| Personal blog | A technical write-up about Mac resource forks, MACE audio, PICT conversion, and tracing 68k code |

## Short social post

I revived SimJesse!, a 1993 classic Mac freeware speech toy, as a static web app. It uses the original recovered sounds/art, decodes old MACE 3:1 audio, and ports the speech algorithm from traced 68k code. Includes a faithful recreation plus a modern remix/compose mode.

Live demo: https://evillollive.github.io/sim-jesse/

## Technical post draft

Title: **Recreating a 1993 Mac speech toy in the browser**

SimJesse! 1.0 was a classic Mac freeware app that assembled digitized Jesse Jackson clips into endless pseudo-speeches. The original app no longer runs on modern machines, but a preserved copy made it possible to rebuild the experience for the web.

The recovery path involved extracting the Mac resource fork from an AppleDouble file, parsing the resource map, decoding 123 `'snd '` resources, converting 31 PICT images, and tracing the compiled 68k code to recover the seven grammar-aware speech patterns. The classic web version is a self-contained HTML file with embedded art and audio; the v2 "Dream Machine" version adds captions, a speech composer, shareable links, and Web Audio remix beats.

The result is part preservation artifact, part weird web toy, and part reverse-engineering note: https://github.com/evillollive/sim-jesse

## Show HN-style draft

**Show HN: SimJesse!, a 1993 Mac speech toy revived in the browser**

I recreated SimJesse! 1.0, a 1993 classic Mac freeware app, as a static web app. The original generated endless pseudo-speeches from digitized Jesse Jackson clips.

This version was built by extracting the original Mac resource fork, decoding MACE 3:1 audio, converting PICT artwork, and tracing the compiled 68k binary to recover the speech-generation algorithm. There is a faithful single-file recreation and a modern v2 with compose/remix modes.

Demo: https://evillollive.github.io/sim-jesse/

Repo: https://github.com/evillollive/sim-jesse

## Trust and safety language

SimJesse is a static preservation project with no backend, no analytics, no user accounts, and no package dependencies. It is a tribute to Jesse Jackson's oratory and to the original 1993 freeware app. The project preserves historical software behavior while making the implementation and asset extraction process inspectable.

## Follow-up backlog

- Capture a real animated GIF or short video of both the classic recreation and Dream Machine modes.
- Add a short blog post with screenshots of resource-fork extraction and 68k tracing.
- Add GitHub Pages links directly to the repository sidebar after metadata updates.
- Consider documenting browser compatibility for local `file://` playback versus static-server playback.
- Consider adding alt-text-rich screenshots if the SVG preview is replaced with real captured media.
