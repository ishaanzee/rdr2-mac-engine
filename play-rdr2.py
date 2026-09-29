#!/usr/bin/env python3
"""Launch Red Dead Redemption 2 (Epic) on the WineCX24-D3DMetal engine
without opening Heroic. Heroic itself is set up to do the same thing.

Uses legendary 0.21.1 (wrapper-exe support) so PlayRDR2.exe starts through
Heroic's stand-in EpicGamesLauncher.exe; the Rockstar launcher only hands off
to the game when the Epic launcher is its parent.
"""
import os
import subprocess
import sys

HOME = os.path.expanduser("~")
HEROIC = os.path.join(HOME, "Library/Application Support/heroic")
ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
LEGENDARY = os.path.join(ENGINE_DIR, "legendary")
WINE = os.path.join(HEROIC, "tools/wine/WineCX24-D3DMetal/Contents/Resources/wine/bin/wine")
PREFIX = os.path.join(HOME, "Games/Heroic/Prefixes/Red Dead Redemption 2 (CX24)")
APP_NAME = "Heather"  # Epic's internal id for RDR2


def main():
    subprocess.run([os.path.join(ENGINE_DIR, "before-launch.sh")], check=True)
    env = dict(os.environ,
               LEGENDARY_CONFIG_PATH=os.path.join(HEROIC, "legendaryConfig/legendary"),
               USE_FAKE_EPIC_EXE="true",
               LEGENDARY_WRAPPER_EXE=r"C:\windows\command\EpicGamesLauncher.exe",
               WINEPREFIX=PREFIX, WINEMSYNC="1", WINEESYNC="1",
               WINEDEBUG=os.environ.get("WINEDEBUG", "-all"))
    cmd = [LEGENDARY, "launch", APP_NAME, "--wine", WINE, "--language", "en"] + sys.argv[1:]
    os.execve(LEGENDARY, cmd, env)


if __name__ == "__main__":
    main()
