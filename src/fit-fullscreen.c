/* Keeps RDR2's borderless/fullscreen window covering its monitor.
 * The Wine Mac driver only switches the Mac's display mode while Wine is the
 * active app; otherwise it defers the switch until Wine is activated. RDR2
 * sets its fullscreen mode at startup while Heroic/Terminal is still in
 * front, so DXGI sizes the window to the old desktop (e.g. 1800x1169 at
 * 260,184 for 1280x800). When the mode switch lands, nothing resizes the
 * window and the screen shows a cropped, offset corner of the picture.
 * This polls the game window and, while it has no caption (Fullscreen or
 * Windowed Borderless), moves it to exactly cover its monitor. Windowed mode
 * is left alone. Exits when the game window goes away. */
#include <windows.h>

#define POLL_MS 250
#define FIND_TIMEOUT_MS (15 * 60 * 1000)

int WINAPI wWinMain(HINSTANCE inst, HINSTANCE prev, LPWSTR cmd, int show)
{
    DWORD waited = 0;
    HWND hwnd;

    while (!(hwnd = FindWindowW(L"sgaWindow", NULL)))
    {
        if (waited >= FIND_TIMEOUT_MS) return 1;
        Sleep(POLL_MS);
        waited += POLL_MS;
    }

    while (IsWindow(hwnd))
    {
        MONITORINFO mi = {sizeof(mi)};
        RECT r;
        LONG style = GetWindowLongW(hwnd, GWL_STYLE);

        if (!(style & WS_CAPTION) && !(style & WS_MINIMIZE) && IsWindowVisible(hwnd) &&
            GetWindowRect(hwnd, &r) &&
            GetMonitorInfoW(MonitorFromWindow(hwnd, MONITOR_DEFAULTTOPRIMARY), &mi) &&
            !EqualRect(&r, &mi.rcMonitor))
        {
            SetWindowPos(hwnd, NULL, mi.rcMonitor.left, mi.rcMonitor.top,
                         mi.rcMonitor.right - mi.rcMonitor.left,
                         mi.rcMonitor.bottom - mi.rcMonitor.top,
                         SWP_NOZORDER | SWP_NOACTIVATE | SWP_NOOWNERZORDER);
        }
        Sleep(POLL_MS);
    }
    return 0;
}
