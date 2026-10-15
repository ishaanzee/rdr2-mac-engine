#!/bin/bash
# Started in the background by before-launch.sh. Waits for RDR2.exe, then runs
# fit-fullscreen.exe in the game's wineserver (see src/fit-fullscreen.c).
# Starting it before the game would launch the wineserver itself, so wait.

ENGINE_DIR="$(cd "$(dirname "$0")" && pwd)"
WINE="$HOME/Library/Application Support/heroic/tools/wine/WineCX24-D3DMetal/Contents/Resources/wine/bin/wine"
export WINEPREFIX="$HOME/Games/Heroic/Prefixes/Red Dead Redemption 2 (CX24)"
export WINEMSYNC=1 WINEESYNC=1 WINEDEBUG=-all  # must match the game's wineserver

for _ in $(seq 600); do  # up to 10 minutes (Rockstar launcher sign-in)
    pgrep -qf 'RedDeadRedemption2.RDR2\.exe' && exec "$WINE" "$ENGINE_DIR/fit-fullscreen.exe"
    sleep 1
done
