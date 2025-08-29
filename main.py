from data import *

import ctypes   # Windows scale disable, window control
from pynput import mouse

from io_tools import IOManager, check
from auto_click import qacm, goto, set_options

ctypes.windll.user32.SetProcessDPIAware()


def iw4_settings(x: int, y: int, button: mouse.Button, pressed: bool):
  global current_setting
  if button == mouse.Button.middle and pressed:
    goto('edit')
    current_setting = 'standart_settings'
    set_options(*iw4s)
    qacm.clear()


if __name__ == '__main__':
  choice = check("Iaw4tch's settings", "Enter shell")
  match choice:
    case 1:
      print('Press middle button to start applying settings')
      with mouse.Listener(on_click=iw4_settings) as listener:
        listener.join()
    case 2:
      iom = IOManager()
      print("Script is empty, fisrt edit enter -> False")
      print("Type 'help' if you use shell for the first time")
      while iom.can_repeat_commanding:
        inp = input(
            f'{len(iom.script['repr'])+1}: ').lower().strip()
        iom.commanding(inp)
    case _:
      pass
