# Builds the Windows helpers (needs mingw-w64: brew install mingw-w64).
CC = x86_64-w64-mingw32-gcc

all: SocialClubHelper-wrapper.exe fit-fullscreen.exe

SocialClubHelper-wrapper.exe: src/SocialClubHelper-wrapper.c
	$(CC) -O2 -municode -mwindows -o $@ $<

fit-fullscreen.exe: src/fit-fullscreen.c
	$(CC) -O2 -municode -mwindows -o $@ $<

clean:
	rm -f SocialClubHelper-wrapper.exe fit-fullscreen.exe

.PHONY: all clean
