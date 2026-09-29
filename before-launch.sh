#!/bin/bash
# Heroic "before launch" script for RDR2 on the WineCX24-D3DMetal engine.
#
# Social Club updates replace SocialClubHelper.exe with Rockstar's original,
# which would drop our wrapper (--no-sandbox, occlusion off, ANGLE/D3D11) and
# bring back the blank sign-in window. Put the wrapper back if that happened.

ENGINE_DIR="$(cd "$(dirname "$0")" && pwd)"
PREFIX="$HOME/Games/Heroic/Prefixes/Red Dead Redemption 2 (CX24)"
SC="$PREFIX/drive_c/Program Files/Rockstar Games/Social Club"
WRAPPER="$ENGINE_DIR/SocialClubHelper-wrapper.exe"

[ -f "$SC/SocialClubHelper.exe" ] || exit 0
[ -f "$WRAPPER" ] || { echo "before-launch: $WRAPPER missing, run make" >&2; exit 1; }

# Any build of the wrapper references SocialClubHelper.real.exe (UTF-16);
# Rockstar's helper doesn't. Only move the helper aside when it's Rockstar's,
# otherwise we'd overwrite the real helper with an old wrapper.
is_wrapper() { LC_ALL=C grep -qa 'r.e.a.l.\..e.x.e' "$1"; }

if ! is_wrapper "$SC/SocialClubHelper.exe"; then
    mv -f "$SC/SocialClubHelper.exe" "$SC/SocialClubHelper.real.exe"
    cp "$WRAPPER" "$SC/SocialClubHelper.exe"
    echo "before-launch: reinstalled SocialClubHelper wrapper"
elif ! cmp -s "$SC/SocialClubHelper.exe" "$WRAPPER"; then
    cp "$WRAPPER" "$SC/SocialClubHelper.exe"
    echo "before-launch: updated SocialClubHelper wrapper"
fi
