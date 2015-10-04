
import time
import win32con
import win32api
import win32gui
import win32process

laMeilleureListe ={}

monApplication = "C:\\Users\\User\\Documents\\actiview\\Actiview705-Laptop.exe"
notepad = "C:\\Windows\\System32\\notepad.exe"


_, _, pid, tid = win32process.CreateProcess(
    None,    # name
    notepad,     # command line
    None,    # process attributes
    None,    # thread attributes
    0,       # inheritance flag
    0,       # creation flag
    None,    # new environment
    None,    # current directory
    win32process.STARTUPINFO ())



def putSubList(hwnd, laMeilleureListe):
    laMeilleureListe[win32gui.GetClassName(hwnd)] = hwnd

def putInList(hwnd, laMeilleureListe):
    maSousListe = {}
    
    if win32gui.GetClassName(hwnd) in ('IME', 'MSCTFIME UI'):
        return True
    else:
        win32gui.EnumChildWindows(hwnd, putSubList, laMeilleureListe)
    
    
time.sleep(2)
win32gui.EnumThreadWindows(tid, putInList, laMeilleureListe)

win32api.PostMessage(laMeilleureListe['Edit'], win32con.WM_CHAR, ord('b'), 0)

print laMeilleureListe