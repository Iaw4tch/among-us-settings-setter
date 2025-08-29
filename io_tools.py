from data import *

import tkinter as tk  # GUI
from tkinter import filedialog  # File saving/opening
import json  # Saving script
from difflib import get_close_matches  # Command prompter
import ctypes
from typing import Any, cast  # Type annotations
from os import system, name  # Console clear
import pynput as pn
from time import sleep as slp

from auto_click import MouseLocation, isfloat, find_info_by_name, goto, set_options, qacm


def clear_console():
  """Clears text from the console"""
  system('cls' if name == 'nt' else 'clear')


def check(*check_to: str) -> int:
  """Universal dialog field.

    Args:
      check_to (list[tuple[str, str]]): List of options in format (display_text, value).

    Returns:
      str: Final (correct) entry of a user.

    Examples:
      >>> # Valid input
      >>> check('First','Second')
      1 -> First
      2 -> Second
      > 2  # user input
      function returns 2
      >>> # With invalid input
      >>> check('Yes','No')
      1 -> Yes
      2 -> No
      > m  # invalid input, asks again
      ...
      > 1  # valid
      Returns 1
    """
  again: list[str] = []
  for i, string in enumerate(check_to):
    again.append(f'{i+1} -> {string}')
  check_what = input('\n'.join(again)+'\n> ').strip()
  while True:
    if check_what in map(str, range(1, len(check_to)+1)):
      break
    else:
      print('Invalid input')
      check_what = input('\n'.join(again)+'\n> ').strip()
  return int(check_what)


def valid_index(index: int, script: list[Any]) -> bool:
  if index == 0:
    print('Unsupported index 0')
    return False
  if abs(index)-1 > len(script):
    print('Index out of script range')
    return False
  return True


def set_check(name: str, make: str) -> bool:
  info = find_info_by_name(name)
  if isinstance(info, tuple) and len(info) == 4:
    if info[-1] == 'f':
      info = cast(FieldInfo, info)
      if isinstance(info[-2]['step'], int):
        if make.isdigit() and int(make) in info[-2]['vars']:
          return True
        else:
          print(f"Making value '{make}' must be compatible {info[-2]['vars']}")
          return False
      if isinstance(info[-2]['step'], float):
        make = make.replace(',', '.')
        if isfloat(make) and float(make) in info[-2]['vars']:
          return True
        else:
          print(f"Making value '{make}' must be compatible {info[-2]['vars']}")
          return False
      if info[-2]['step'] == 'string':
        if make in info[-2]['vars']:
          return True
        else:
          print(f"Making value '{make}' must be compatible {info[-2]['vars']}")
          return False
      if info[-2]['step'] == 'inf5':
        if make == 'infinite' or make in info[-2]['vars'] or make.isdigit() and int(make) in info[-2]['vars']:
          return True
        else:
          print(f"Making value '{make}' must be compatible {info[-2]['vars']}")
          return False
    if info[-1] == 'c':
      if make in ('true', 'false'):
        return True
      else:
        print(f"Making value '{make}' must be compatible ('true', 'false')")
        return False
  matches = get_close_matches(name, PARAMETERS_NAMES, n=1)
  if matches:
    print(f"Incorrect name, did you mean '{matches[0]}'?")
  else:
    print(f'Incorrect name {name}')
  return False


class IOManager:
  def __init__(self):
    self.script: ScriptDict = {
        'data': {'flag': False, 'lines': []}, 'repr': []}
    self.handlers: Handlers = {
        'args': {
            'run': self.handle_run,
            ('remove', 'rm'): self.handle_remove,
            ('insert', 'ins'): self.handle_insert,
            ('replace', 'r'): self.handle_replace,
        },
        'noargs': {
            '.': lambda: print('{'+',\n'.join(v.keys())+'}'),
            'help': lambda: print(command_info),
            'edit': self.handle_edit,
            'buttons': lambda: print(BUTTONS),
            ('save', 's'): self.handle_save,
            ('load', 'l'): self.handle_load,
            ('exit', 'e'): lambda: setattr(self, 'can_repeat_commanding', False),
        }
    }
    self.running = False
    self.can_repeat_commanding = True
    self.commands: list[str] = []
    for c in self.handlers['args'] | self.handlers['noargs']:
      if isinstance(c, str):
        self.commands.append(c)
      else:
        self.commands.append(c[0])

  def commanding(self, inp: str):
    inp = inp.replace('>', '')
    parts = inp.split()
    if len(parts) > 0:
      parameter = True
      for command in self.handlers['noargs'] | self.handlers['args']:
        if parts[0] in command:
          parameter = False
          break
      if parameter and len(parts) == 2:
        self.handle_set(parts[0], parts[1])
      else:
        cmd = parts[0]
        args = parts[1:]
        cmd_found = False
        for command in self.handlers['noargs']:
          if isinstance(command, str):
            if cmd == command:
              self.handlers['noargs'][command]()
              cmd_found = True
              break
          else:
            if cmd in command:
              self.handlers['noargs'][command]()
              cmd_found = True
              break
        if not cmd_found:
          for command in self.handlers['args']:
            if isinstance(command, str):
              if cmd == command:
                self.handlers['args'][command](args)
                cmd_found = True
                break
            else:
              if cmd in command:
                self.handlers['args'][command](args)
                cmd_found = True
                break
        if not cmd_found:
          self.find_probable_compilance(cmd)
    else:
      self.review()

  def find_probable_compilance(self, cmd: str):
    if self.found_close_commands(cmd):
      return
    if (info := find_info_by_name(cmd, commanding=True)) is not None:
      print(info)
    else:
      probable: list[str] = []
      parts = cmd.split('.')
      no_real_info = True
      for part in parts:
        if part in PARTS:
          probable.append(part)
        else:
          if p := self.get_close_part(part):
            probable.append(f'<{p}>')
            no_real_info = False
          else:
            probable.append('<???>')
      if not no_real_info:
        print(f'Unknown object, did you mean {'.'.join(probable)}?')
      else:
        if not self.found_close_names(cmd):
          print('Unknown command')

  def found_close_commands(self, cmd: str) -> bool:
    command_match = get_close_matches(cmd, self.commands)
    if '.' not in cmd:
      if len(command_match) == 1:
        print(f"Unknown command, did you mean <{command_match[0]}>?")
        return True
      elif len(command_match) > 1:
        print(
            f"Unknown command, did you mean {('?'+'\n'+' '*30).join(map(lambda x: f"<{x}>", command_match))}?")
        return True
      else:
        return False
    return False

  def found_close_names(self, name: str) -> bool:
    name_match = get_close_matches(name, list(
        set(FINDABLE_NAMES) | set(PARAMETERS_NAMES)))
    if len(name_match) == 1:
      print(f"Unknown name, did you mean '{name_match[0]}'?")
      return True
    elif len(name_match) > 1:
      print(
          f"Unknown name, did you mean {('?'+'\n'+' '*27).join(map(lambda x: f"<{x}>", name_match))}?")
      return True
    return False

  def get_close_part(self, part: str) -> str:
    part_match = get_close_matches(part, PARTS, n=1)
    if part_match:
      return part_match[0]
    return ''

  def handle_set(self, parameter: str, value: str):
    if set_check(parameter, value):
      self.script['data']['lines'].append(
          (cast(CheckboxInfo | FieldInfo, find_info_by_name(parameter))[0], value))
      self.script['repr'].append(f'{parameter} > {value}')
      self.review()

  def handle_remove(self, args: list[str]):
    if len(args) != 1:
      print('Remove command takes one index argument')
      return
    if not (args[0].isdigit() or (args[0].startswith('-') and args[0][1:].isdigit())):
      print('Index must be an integer')
      return
    index = int(args[0])
    if not valid_index(index, self.script['repr']):
      return
    idx = index - 1 if index > 0 else index
    self.script['data']['lines'].pop(idx)
    self.script['repr'].pop(idx)
    self.review()

  def handle_insert(self, args: list[str]):
    if len(args) != 3:
      print('Insert command takes three arguments')
      return
    if not (args[0].isdigit() or (args[0].startswith('-') and args[0][1:].isdigit())):
      print('Index must be an integer')
      return
    index = int(args[0])
    if not valid_index(index, self.script['repr']):
      return
    if not set_check(args[1], args[2]):
      return
    idx = index - 1 if index > 0 else index
    self.script['data']['lines'].insert(idx,
                                        (cast(CheckboxInfo | FieldInfo, find_info_by_name(args[1]))[0], args[2]))
    self.script['repr'].insert(idx, f'{args[1]} > {args[2]}')
    self.review()

  def handle_save(self):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # type: ignore
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Script files", "*.json")],
        title='Script file')
    if file_path:
      with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(self.script['data'], f, indent=2, ensure_ascii=True)
        print('Successfuly saved')
    root.destroy()
    ctypes.windll.user32.SetForegroundWindow(
        ctypes.windll.kernel32.GetConsoleWindow()
    )

  def handle_load(self):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # type: ignore
    file_path = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("Script files", "*.json")],
        title="Script file")
    if file_path:
      with open(file_path, 'r', encoding='utf-8') as f:
        try:
          load = json.load(f)
          self.script['data'] = load
          self.script['repr'].clear()
          for name, make in self.script['data']['lines']:
            splitted = name.split('.')
            if splitted in ('#', '%'):
              name = splitted[-2]+'.'+splitted[-1]
            else:
              name = splitted[-1]
            self.script['repr'].append(f'{name} > {make}')
        except:
          print('Damaged or unknown structure of the loading file')
    root.destroy()
    ctypes.windll.user32.SetForegroundWindow(
        ctypes.windll.kernel32.GetConsoleWindow()
    )
    self.review()

  def handle_run(self, args: list[str]):
    if len(args) != 2:
      print('Run command takes two arguments')
      return
    if self.script['data']:
      if self.script['data']['flag']:
        MouseLocation.current_setting = 'game_presets'
      self.running = True
      print('Press middle button to start applying settings')
      with pn.mouse.Listener(on_click=self.script_run):
        while self.running:
          slp(0.1)
    else:
      print('Empty script, cannot run')

  def script_run(self, x: int, y: int, button: pn.mouse.Button, pressed: bool):
    if button == pn.mouse.Button.middle and pressed:
      print('Script started')
      if self.script['data']['flag']:
        goto('edit')
      set_options(*self.script['data']['lines'])
      qacm.clear()

  def handle_stop(self):
    if self.running:
      print('Script finished')
      self.running = False
    else:
      print('You cannot stop a script that is not running')

  def handle_edit(self):
    if self.script['data']['flag']:
      self.script['data']['flag'] = False
    else:
      self.script['data']['flag'] = True
    self.review()

  def handle_replace(self, args: list[str]):
    if len(args) != 3:
      print('Replace command takes three arguments')
      return
    if not (args[0].isdigit() or (args[0].startswith('-') and args[0][1:].isdigit())):
      print('Index must be an integer')
      return
    index = int(args[0])
    if not valid_index(index, self.script['repr']):
      return
    if not set_check(args[1], args[2]):
      return
    idx = index - 1 if index > 0 else index
    self.script['data']['lines'][idx] = cast(
        CheckboxInfo | FieldInfo, find_info_by_name(args[1]))[0], args[2]
    self.script['repr'][idx] = f'{args[1]} > {args[2]}'
    self.review()

  def review(self):
    clear_console()
    print(f'First edit enter -> {self.script['data']['flag']}')
    if self.script['repr']:
      print('\n'.join(f'{i+1}: {line}' for i,
            line in enumerate(self.script['repr'])))
    else:
      print('Empty script...')
