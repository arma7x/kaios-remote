import os
import threading
import time
import kaiscr
import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk

takescreenshot = kaiscr.TakeScreenshot()
screenshot = takescreenshot.screenshot
bye = takescreenshot.close
img = None
stop = False


def quit(*args):
    global stop
    stop = True
    bye()
    Gtk.main_quit()


def send_event(dev, key):
    cmd = f'adb shell sendevent {dev} 1 {key} 1 ; adb shell sendevent {dev} 0 0 0 ;adb shell sendevent {dev} 1 {key} 0 ;adb shell sendevent {dev} 0 0 0'
    # print(cmd)
    os.system(cmd)

def on_keypress(widget, event):
    print(event.hardware_keycode)
    if event.keyval == 113: # q key
        quit()
    elif event.hardware_keycode == 22: # BackSpace
        send_event("dev/input/event4", 116)
    elif event.hardware_keycode == 36: # Enter
        send_event("dev/input/event0", 352)
    elif event.hardware_keycode == 111: # Up => Up
        send_event("dev/input/event4", 103)
    elif event.hardware_keycode == 116: # Down => Down
        send_event("dev/input/event3", 108)
    elif event.hardware_keycode == 114: # Right => Right
        send_event("dev/input/event0", 106)
    elif event.hardware_keycode == 113: # Left => Left
        send_event("dev/input/event0", 105)

def update_pic():
    global img
    global takescreenshot
    try:
        while not stop:
            loader = GdkPixbuf.PixbufLoader()
            png = screenshot()
            loader.write(png)
            pb = loader.get_pixbuf()
            if not img:
                img = Gtk.Image.new_from_pixbuf(pb)
            else:
                img.set_from_pixbuf(pb)
            loader.close()
    except Exception as e:
        print(e)


threading.Thread(target=update_pic).start()
window = Gtk.Window()
window.connect("destroy", quit)
window.connect("key-press-event", on_keypress)
window.set_type_hint(Gdk.WindowTypeHint.UTILITY)
while not img:
    time.sleep(0.1)
window.add(img)
window.show_all()
Gtk.main()
