# Builds the SocialClubHelper wrapper (needs mingw-w64: brew install mingw-w64).
CC = x86_64-w64-mingw32-gcc

SocialClubHelper-wrapper.exe: src/SocialClubHelper-wrapper.c
	$(CC) -O2 -municode -mwindows -o $@ $<

clean:
	rm -f SocialClubHelper-wrapper.exe

.PHONY: clean
