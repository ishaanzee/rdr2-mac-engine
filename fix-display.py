#!/usr/bin/env python3
"""Make RDR2 fill the screen on macOS: borderless window at the desktop size.

Wine on macOS doesn't switch the Mac's display mode, so a fullscreen
resolution smaller than the desktop (RDR2 picks the first mode, e.g.
1147x745) renders small inside a black screen. Borderless at the desktop
resolution avoids the mode switch entirely.

Run with the game closed (RDR2 rewrites system.xml on exit).
usage: fix-display.py [WIDTHxHEIGHT]   (default: current desktop size)
"""
import os
import re
import shutil
import subprocess
import sys

SYSTEM_XML = os.path.expanduser(
    "~/Documents/Rockstar Games/Red Dead Redemption 2/Settings/system.xml")


def desktop_size():
    bounds = subprocess.run(
        ["osascript", "-e", 'tell application "Finder" to get bounds of window of desktop'],
        check=True, capture_output=True, text=True).stdout
    _, _, width, height = (int(v) for v in bounds.split(","))
    return width, height


def main():
    if len(sys.argv) > 1:
        width, height = (int(v) for v in sys.argv[1].lower().split("x"))
    else:
        width, height = desktop_size()

    settings = {
        "screenWidth": width, "screenHeight": height,
        "screenWidthWindowed": width, "screenHeightWindowed": height,
        "windowed": 2,  # 0 fullscreen, 1 windowed, 2 borderless
    }

    with open(SYSTEM_XML, newline="") as f:  # keep the CRLF line endings
        xml = f.read()
    for key, value in settings.items():
        xml, count = re.subn(r'(<%s value=")[^"]*(" />)' % key, r"\g<1>%s\g<2>" % value, xml)
        if count != 1:
            sys.exit(f"{key} not found in {SYSTEM_XML}")

    shutil.copy2(SYSTEM_XML, SYSTEM_XML + ".bak")
    with open(SYSTEM_XML, "w", newline="") as f:
        f.write(xml)
    print(f"RDR2 set to borderless {width}x{height} (backup: system.xml.bak)")


if __name__ == "__main__":
    main()
