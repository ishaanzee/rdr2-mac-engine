/* Pass-through wrapper for Rockstar's SocialClubHelper.exe (Chromium/CEF).
 * Chromium's Windows sandbox can't create its restricted child processes under
 * Wine, so the browser process CHECK-fails. This starts the real helper
 * (SocialClubHelper.real.exe) with the original arguments plus:
 *  - --no-sandbox;
 *  - native window occlusion tracking off (it relies on DWM/virtual desktop
 *    APIs Wine lacks, so Chromium thinks its window is hidden);
 *  - ANGLE on D3D11: Rockstar's --use-gl=swiftshader is no longer a valid GL
 *    implementation in this Chromium, which leaves it with no GPU at all.
 * It waits for the helper and returns its exit code. */
#include <windows.h>
#include <wchar.h>

static const wchar_t *skip_argv0(const wchar_t *cmd)
{
    if (*cmd == L'"')
    {
        cmd++;
        while (*cmd && *cmd != L'"') cmd++;
        if (*cmd) cmd++;
    }
    else
    {
        while (*cmd && *cmd != L' ' && *cmd != L'\t') cmd++;
    }
    return cmd;
}

int WINAPI wWinMain(HINSTANCE inst, HINSTANCE prev, LPWSTR unused, int show)
{
    static const wchar_t extra[] = L" --no-sandbox --disable-features=CalculateNativeWinOcclusion --disable-backgrounding-occluded-windows --use-gl=angle --use-angle=d3d11";
    wchar_t exe[MAX_PATH], *slash, *cmdline;
    const wchar_t *args = skip_argv0(GetCommandLineW());
    PROCESS_INFORMATION pi;
    STARTUPINFOW si;
    DWORD code = 1;
    size_t len;

    GetModuleFileNameW(NULL, exe, MAX_PATH);
    if (!(slash = wcsrchr(exe, L'\\'))) return 1;
    wcscpy(slash + 1, L"SocialClubHelper.real.exe");

    len = wcslen(exe) + wcslen(args) + wcslen(extra) + 4;
    if (!(cmdline = HeapAlloc(GetProcessHeap(), 0, len * sizeof(wchar_t)))) return 1;
    wcscpy(cmdline, L"\"");
    wcscat(cmdline, exe);
    wcscat(cmdline, L"\"");
    wcscat(cmdline, args);
    wcscat(cmdline, extra);

    GetStartupInfoW(&si);
    if (!CreateProcessW(exe, cmdline, NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi))
        return GetLastError();

    WaitForSingleObject(pi.hProcess, INFINITE);
    GetExitCodeProcess(pi.hProcess, &code);
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    return code;
}
