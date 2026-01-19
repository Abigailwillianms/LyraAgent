import win32gui

def get_window_titles():
    def enum_windows(hwnd, titles):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                titles.append((hwnd, title))
    titles = []
    win32gui.EnumWindows(enum_windows, titles)
    for hwnd, title in titles:
        print(f"HWND: {hwnd}, Title: {title}")
    return titles


