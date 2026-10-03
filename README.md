# RDR2 (Epic) on Apple Silicon — custom engine

Status (2026-10-03): works. Launches from Heroic, auto-signs in to Rockstar,
and the game is playable on Apple Silicon.

## Setup (files not in git)
- `make` — builds `SocialClubHelper-wrapper.exe` (needs `brew install mingw-w64`)
- legendary 0.21.1: download `legendary_macOS.zip` from
  https://legendary.gl/release/0.21.1, put `legendary_macOS_arm64` here as
  `legendary`
- Engine binaries (Wine, D3DMetal, DXMT) aren't redistributed here; D3DMetal
  comes from Apple's Game Porting Toolkit under Apple's license.

## Play
- Heroic → Red Dead Redemption 2 → Play. (First Heroic start takes ~2 min.)
- Without Heroic: `./play-rdr2.py`

## Fullscreen
Wine on macOS doesn't change the Mac's display mode, so RDR2's fullscreen
at a smaller resolution (it defaults to 1147x745) shows a small picture in a
black screen. Use borderless at the desktop resolution: run
`./fix-display.py` with the game closed, or in-game set Screen Type =
Windowed Borderless and Resolution = your desktop size (e.g. 1800x1169).
Don't use the macOS green fullscreen button. Use FSR if FPS drops.

## Pieces
- Engine: `~/Library/Application Support/heroic/tools/wine/WineCX24-D3DMetal`
  - Wine 9.0 from CrossOver 24.0.7 sources (Sikarugir `WS12WineCX24.0.7_7`)
  - Apple D3DMetal 3.0 (from GPTK 3.0-3) for d3d11/d3d12/dxgi — used by RDR2.exe
  - Rebuilt `d2d1.dll` (src/wine-d2d1-dc-render-target-readback.patch) and
    `user32.dll` (src/wine-user32-IsWindowArranged.patch); originals in
    `lib/wine/cx-original/`
  - DXMT v0.80 `winemetal` unix/PE parts
- Prefix: `~/Games/Heroic/Prefixes/Red Dead Redemption 2 (CX24)`
  - system32 d3d10core/d3d11/dxgi = DXMT, unstamped (d3d11 patched with
    src/dxmt-d3d11-SwapDeviceContextState.py); only `Launcher.exe` uses them
    (AppDefaults); everything else is pinned to builtin (D3DMetal)
  - `Launcher.exe`: d3d12, nvapi64, nvapi, atidxx64, nvngx disabled
    (D3DMetal's NVAPI shim crashes without D3DMetal's dxgi)
  - native Microsoft ucrtbase in system32 (Wine lacks `_strerror_s`)
  - Social Club installed; `SocialClubHelper.exe` = wrapper
    (src/SocialClubHelper-wrapper.c) → `SocialClubHelper.real.exe` with
    `--no-sandbox --disable-features=CalculateNativeWinOcclusion
    --disable-backgrounding-occluded-windows --use-gl=angle --use-angle=d3d11`
- `legendary` 0.21.1 (Heroic `altLegendaryBin`): launches via Heroic's stand-in
  EpicGamesLauncher.exe; Rockstar only hands off to the game when the Epic
  launcher is its parent.
- `before-launch.sh` (Heroic before-launch script): reinstalls the wrapper if a
  Social Club update overwrote it.

## Don't
- Enable DXVK / change the Wine version in Heroic for this game (overwrites the
  DLL setup). Heroic config backups: `*.before-cx24` next to the originals.

## Notes for next time
- Rebuilding Wine DLLs: CrossOver 24.0.7 source, `arch -x86_64` configure with
  `--enable-archs=x86_64`, mingw-w64 from Homebrew; a stub `distversion.h` is
  needed in include/ and programs/winedbg/; newer binutils make `.idata`
  read-only — set IMAGE_SCN_MEM_WRITE on it after linking.
- Useful logs: `~/Documents/Rockstar Games/Launcher/launcher.log`,
  `~/Documents/Rockstar Games/Social Club/`, add `--enable-logging
  --log-file=C:\cef.log` to the wrapper for Chromium logs.
