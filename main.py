import pynput as pn  # For mouse control
from time import sleep as slp  # For delay
from ctypes import windll  # For windows scale disable
import numpy as np  # For 3d color array
from PIL import ImageGrab  # For grabbing images
from typing import Any, Union, cast  # Type annotations
from os import system, name
from data import *
import tkinter as tk
from tkinter import filedialog
import json
import ctypes
from threading import Thread


class ConsoleManager:
  can_run = True

  def __init__(self):
    self.viewing = False
    self.script: ScriptDict = {
        'data': {'flag': False, 'lines': []}, 'repr': []}
    self.written: list[str] = []
    self.handlers: Handlers = {
        'args': {
            'set': self.handle_set,
            ('remove', 'rm'): self.handle_remove,
            ('insert', 'ins'): self.handle_insert,
        },
        'noargs': {
            'help': lambda: printq(command_info),
            ('view', 'v'): self.handle_v,
            ('save', 's'): self.handle_save,
            ('load', 'l'): self.handle_load,
            ('run', 'r'): lambda: Thread(target=self.handle_run).start(),
            ('stop', 'st'): self.handle_stop,
            ('edit'): self.handle_edit,
        }
    }
    self.running = False

  def commanding(self, inp: str):
    parts = inp.split()
    if len(parts) > 0:
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
        self.handle_info_lookup(inp)
    else:
      clear_console()
      if manager.viewing:
        script_view()
      else:
        manager.written.pop()
        normal_view()

  def handle_set(self, args: list[str]):
    if len(args) != 2:
      printq('Set command takes two arguments')
      return
    if set_check(args[0], args[1]):
      self.script['data']['lines'].append(
          (cast(CheckboxInfo | FieldInfo, find_info_by_name(args[0]))[0], args[1]))
      self.script['repr'].append(f'set {args[0]} {args[1]}')
      if self.viewing:
        script_view()

  def handle_remove(self, args: list[str]):
    if len(args) != 1:
      printq('Remove command takes one index argument')
      return
    if not (args[0].isdigit() or (args[0].startswith('-') and args[0][1:].isdigit())):
      printq('Index must be an integer')
      return
    index = int(args[0])
    if index == 0:
      printq('Unsupported index 0')
      return
    if abs(index) > len(self.script['repr']):
      printq('Index out of script range')
      return
    idx = index - 1 if index > 0 else index
    self.script['data']['lines'].pop(idx)
    self.script['repr'].pop(idx)
    if self.viewing:
      script_view()

  def handle_insert(self, args: list[str]):
    if len(args) != 3:
      printq('Insert command takes three arguments')
      return
    if not (args[0].isdigit() or (args[0].startswith('-') and args[0][1:].isdigit())):
      printq('Index must be an integer')
      return
    if not set_check(args[1], args[2]):
      return
    index = int(args[0])
    if index == 0:
      printq('Unsupported index 0')
      return
    if abs(index) > len(self.script['repr']):
      printq('Index out of script range')
      return
    idx = index - 1 if index > 0 else index
    self.script['data']['lines'].insert(idx,
                                        (cast(CheckboxInfo | FieldInfo, find_info_by_name(args[1]))[0], args[2]))
    self.script['repr'].insert(idx, f'set {args[1]} {args[2]}')
    if self.viewing:
      script_view()

  def handle_v(self):
    if self.viewing:
      normal_view()
      self.viewing = False
    else:
      script_view()
      self.viewing = True

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
          self.script['repr'] = [
              f'set {name} {make}' for name, make in self.script['data']['lines']]
        except:
          printq('Damaged or unknown structure of the loading file')
    root.destroy()
    ctypes.windll.user32.SetForegroundWindow(
        ctypes.windll.kernel32.GetConsoleWindow()
    )

  def handle_info_lookup(self, inp: str):
    if (info := find_info_by_name(inp, commanding=True)) is not None:
      printq(info)
    else:
      printq('Unknown command')

  def handle_run(self):
    global current_setting
    if self.script['data']:
      current_setting = 'standart_settings'
      self.running = True
      printq('Press middle button to start applying settings')
      with pn.mouse.Listener(on_click=self.script_run):
        while self.running:
          slp(0.1)
    else:
      printq('Empty script, cannot run')

  def script_run(self, x: int, y: int, button: pn.mouse.Button, pressed: bool):
    if button == pn.mouse.Button.middle and pressed:
      printq('Script started')
      if self.script['data']['flag']:
        goto('edit')
      set_options(*self.script['data']['lines'])
      qacmanager.clear()

  def handle_stop(self):
    if self.running:
      printq('Script finished')
      self.running = False
    else:
      printq('You cannot stop a script that is not running')

  def handle_edit(self):
    if self.script['data']['flag']:
      self.script['data']['flag'] = False
    else:
      self.script['data']['flag'] = True
    if self.viewing:
      script_view()


class QACManager:
  def __init__(self):
    self.qac: dict[str, dict[str, int | None]] = {
        'engineer': {'#': None, '%': None},
        'guardian_angel': {'#': None, '%': None},
        'scientist': {'#': None, '%': None},
        'tracker': {'#': None, '%': None},
        'noisemaker': {'#': None, '%': None},
        'shapeshifter': {'#': None, '%': None},
        'phantom': {'#': None, '%': None},
    }

  def set_val(self, qac: tuple[str, Literal['#', '%']], val: int):
    role, t = qac
    if role in self.qac:
      if val == 0:
        self.qac[role]['%'] = 0
        self.qac[role]['#'] = 0
      else:
        self.qac[role][t] = val
        self.update()
    else:
      printq(f'Role {role} is not in a role')

  def update(self):
    for role in self.qac:
      if self.qac[role]['#'] is not None and self.qac[role]['#'] != 0 and self.qac[role]['%'] == 0:
        self.qac[role]['%'] = 50
      elif self.qac[role]['%'] is not None and self.qac[role]['%'] != 0 and self.qac[role]['#'] == 0:
        self.qac[role]['#'] = 1

  def clear(self):
    for role in self.qac:
      self.qac[role]['#'] = None
      self.qac[role]['%'] = None

  def get(self, qac: tuple[str, Literal['#', '%']]) -> int | None:
    name, t = qac
    if name in self.qac:
      return self.qac[name][t]


windll.user32.SetProcessDPIAware()
mouse = pn.mouse.Controller()
manager = ConsoleManager()
qacmanager = QACManager()
current_settings_section = v['settings']['impostors']['cords']
TEAL = (44, 243, 198)
TOLERANCE = 30
CHECKBOX_SHAPE = (60, 60)
current_setting = 'standart_settings'
current_all_section = 'crewmate_roles'


def check(*check_to: str) -> str:
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
      function returns '2'
      >>> # With invalid input
      >>> check('Yes','No')
      1 -> Yes
      2 -> No
      > m  # invalid input, asks again
      ...
      > 1  # valid
      Returns '1'
    """
  again: list[str] = []
  for i, string in enumerate(check_to):
    again.append(f'{i+1} -> {string}')
  check_what = inputq('\n'.join(again)+'\n> ').strip()
  while True:
    if check_what in map(str, range(1, len(check_to)+1)):
      break
    else:
      printq('Invalid input')
      check_what = inputq('\n'.join(again)+'\n> ').strip()
  return check_what


def clear_console():
  """Clears text from the console"""
  system('cls' if name == 'nt' else 'clear')


def find_info_by_name(name: str, commanding: bool = False) -> Union[
    Cords,
    int,
    float,
    str,
    tuple[Any, ...],
    list[str],
    FieldInfo,
    CheckboxInfo,
    None
]:
  """Finds and returns information from the settings hierarchy by name/path.

    Searches through the nested settings structure (defined in global 'v' dictionary)
    using dot notation paths. Supports both direct access and recursive searching.

    Args:
      name (str): The dot-separated path to the setting. Can be:
        - Direct path (e.g., 'settings.impostors.fields.kill_cooldown')
        - Shortcut (e.g., 'kill_cooldown' for recursive search)
        - Prefix with 'v.' (automatically stripped)
      commanding (bool): If True, returns only keys/views instead of full info for other functions.

    Returns:
      out:
      One of many possible return types depending on what's found:
        - tuple[int, int]: When coordinates are found (x, y)
        - int | float | str: When a step value found
        - list[str]: When returning available keys for a dictionary level
        - None: When path doesn't resolve or no checkboxes in section
        - tuple[str, dict, Literal['f', 'c']]: Structured return:
          * (vpath, section_name, field_data, 'f') for fields
          * (vpath, section_name, cords, 'c') for checkboxes

    Examples:
      Get coordinates directly:
      >>> find_info_by_name('edit')
      (1584, 751)
      Get field information:
      >>> find_info_by_name('settings.impostors.fields.kill_cooldown')
      ('impostors', {...}, 'f')
      Get field view (commanding mode):
      >>> find_info_by_name('settings.impostors.fields.kill_cooldown', commanding=True)
      ['minus', 'plus', 'field']
      Recursive search by field name:
      >>> find_info_by_name('kill_cooldown')
      ('settings.impostors.fields.kill_cooldown', 'impostors', {...}, 'f')
      >>> find_info_by_name('noisemaker.#')
      ('roles_settings.all.crewmate_roles.noisemaker.#', 'crewmate_roles', {...}, 'f')
    """
  if name.startswith('v.'):
    name = name[2:]
  if name == 'v' or name == '.':
    return list(cast(list[str], v.keys()))
  if name.startswith('.'):
    name = name[1:]
  current: Any = v
  parts = name.split('.')
  if not commanding:
    try:
      if len(parts) == 4 and parts[0] == 'settings' and parts[1] in settings_sections and parts[2] == 'fields' and parts[3] in settings_sections[parts[1]]['fields']:
        section = parts[1]
        field = settings_sections[section]['fields'][parts[3]]
        return name, section, field, 'f'
    except:
      pass
    try:
      if len(parts) == 4 and parts[0] == 'settings' and parts[1] in settings_sections and parts[2] == 'checkboxes' and parts[3] in cast(dict[str, Cords], settings_sections[parts[1]]['checkboxes']):
        section = parts[1]
        checkbox = cast(dict[str, Cords], settings_sections[section]['checkboxes'])[
            parts[3]]
        return name, section, checkbox, 'c'
    except:
      pass
    try:
      if len(parts) == 5 and parts[0] == 'roles_settings' and parts[1] == 'all' and parts[2] in all_teams and parts[3] in {
          k: val
          for k, val in all_teams[parts[2]].items()
          if k != 'cords'
      } and parts[4] in ('#', '%'):
        team = parts[2]
        role = parts[3]
        cont = parts[4]
        field = cast(FieldDict, all_teams[team][role][cont])
        return name, team, field, 'f'
    except:
      pass
    try:
      if len(parts) == 4 and parts[0] == 'roles_settings' and parts[1] in roles_settings_roles and parts[2] in 'fields' and parts[3] in roles_settings_roles[parts[1]]['fields']:
        role = parts[1]
        return name, role, roles_settings_roles[role]['fields'][parts[3]], 'f'
    except:
      pass
    try:
      if len(parts) == 4 and parts[0] == 'roles_settings' and parts[1] in roles_settings_roles and parts[2] in 'checkboxes' and parts[3] in cast(dict[str, Cords], roles_settings_roles[parts[1]]['checkboxes']):
        role = parts[1]
        return name, role,  cast(dict[str, Cords], roles_settings_roles[parts[1]]['checkboxes'])[parts[3]], 'c'
    except:
      pass

  for part in parts:
    if isinstance(current, dict) and part in current:
      current = cast(Any, current[part])
    else:
      if current is v:
        if part in settings_sections:
          return find_info_by_name(f'settings.{name}', commanding=commanding)

        for section in settings_sections:
          if part in v['settings'][section]['fields']:
            return find_info_by_name(f'settings.{section}.fields.{name}', commanding=commanding)

          if v['settings'][section]['checkboxes'] is not None and part in v['settings'][section]['checkboxes']:
            return find_info_by_name(f'settings.{section}.checkboxes.{name}', commanding=commanding)

        if part in all_teams:
          return find_info_by_name(f'roles_settings.all.{name}')

        if len(parts) >= 2 and '#' in parts or '%' in parts:
          for i in range(len(parts)):
            if parts[i] in ('#', '%'):
              if parts[i-1] in teams_crewmate_roles:
                return find_info_by_name(f'roles_settings.all.crewmate_roles.{name}', commanding=commanding)
              if parts[i-1] in teams_impostor_roles:
                return find_info_by_name(f'roles_settings.all.impostor_roles.{name}', commanding=commanding)
              break

        if part in roles_settings_roles_all:
          return find_info_by_name(f'roles_settings.{name}', commanding=commanding)

        for section in roles_settings_roles:
          if part in v['roles_settings'][section]['fields']:
            return find_info_by_name(f'roles_settings.{section}.fields.{name}', commanding=commanding)

          if v['roles_settings'][section]['checkboxes'] is not None and part in v['roles_settings'][section]['checkboxes']:
            return find_info_by_name(f'roles_settings.{section}.checkboxes.{name}', commanding=commanding)

      return None
  if isinstance(current, dict):
    return list(cast(dict[str, Any], current.keys()))
  return current


def goto(section: str):
  """Universal function for travelling through sections

  Args:
    section (str): Can be name of a setting, section from `settings`, section from `roles_settings`, team from `roles_settings.all`
  """
  global current_settings_section, current_all_section
  slp(0.05)
  if section == 'edit':
    mouse.position = v['edit']
    mouse.click(pn.mouse.Button.left)
    printq('Went to edit')
  if section == 'settings':
    set_setting('settings')
    current_all_section = 'crewmate_roles'
  if section == 'roles_settings' or section == 'crewmate_roles' or section == 'all':
    set_setting('roles_settings')
    current_all_section = 'crewmate_roles'
  if section in settings_sections:
    set_setting('settings')
    cords = settings_sections[section]['cords']
    if scroll(current_settings_section, cords):
      current_settings_section = cords
    current_all_section = 'crewmate_roles'
  if section == 'impostor_roles':
    set_setting('roles_settings')
    if current_all_section != 'impostor_roles':
      scroll(v['roles_settings']['all']['crewmate_roles']['cords'],
             v['roles_settings']['all']['impostor_roles']['cords'])
    current_all_section = 'impostor_roles'
  if section in roles_settings_roles:
    set_setting('roles_settings')
    if current_all_section != section:
      mouse.position = roles_settings_roles[section]['cords']
      mouse.click(pn.mouse.Button.left)
      printq('Section:', section)
      current_all_section = section
  slp(0.0555)


def set_setting(name: str):
  """Sets new setting and changes global variable `current_setting`"""
  global current_setting
  slp(0.05)
  match name:
    case 'settings':
      if current_setting != 'settings':
        mouse.position = v['settings']['cords']
        mouse.click(pn.mouse.Button.left)
        printq(f'Setting: was: {current_setting}, became: {name}')
        current_setting = 'settings'
    case 'roles_settings':
      if current_setting != 'roles_settings':
        mouse.position = v['roles_settings']['cords']
        mouse.click(pn.mouse.Button.left)
        printq(f'Setting: was: {current_setting}, became: {name}')
        current_setting = 'roles_settings'
    case _:
      print('Unknown setting')
  slp(0.05)


def calculate_clicks(info: FieldInfo | CheckboxInfo,
                     make: int | bool | float | str,
                     inner: bool | None = None,
                     qac: tuple[str, Literal['#', '%']] | None = None
                     ):
  if isinstance(inner, bool) and info[-1] == 'c':
    info = cast(CheckboxInfo, info)
    if isinstance(make, str):
      if make.lower() == 'true':
        new = True
      elif make.lower() == 'false':
        new = False
      else:
        print(f'Checkbox cannot be set to {make}')
        return
    elif isinstance(make, bool):
      new = make
    else:
      print(f'Checkbox cannot be set to {make}')
      return
    if new != inner:
      mouse.position = info[-2]
      mouse.click(pn.mouse.Button.left)
      print(f'Checkbox: was: {inner}, became: {make}')
  elif inner is None and info[-1] == 'f' and not isinstance(make, bool):
    info = cast(FieldInfo, info)
    if isinstance(info[-2]['step'], (int, float)):
      if isinstance(make, str):
        make = make.replace(',', '.')
        if make.isdigit():
          if isinstance(info[-2]['step'], int):
            new_val = int(make)
          else:
            new_val = float(make)
        elif isfloat(make):
          new_val = float(make)
        else:
          print(f'Making value {make} is NaN')
          return
      else:
        new_val = make
      if new_val in info[-2]['vars']:
        if qac and (prev_val := qacmanager.get(qac)) is not None:
          offset = int((new_val-prev_val)//info[-2]['step'])
          if offset > 0:
            mouse.position = info[-2]['plus']
            for _ in range(offset):
              mouse.click(pn.mouse.Button.left)
              slp(0.0355)
            qacmanager.set_val(qac, cast(int, new_val))
            return
          if offset < 0:
            mouse.position = info[-2]['minus']
            for _ in range(-offset):
              mouse.click(pn.mouse.Button.left)
              slp(0.0355)
            qacmanager.set_val(qac, cast(int, new_val))
            return
        mid = info[-2]['vars'][len(info[-2]['vars'])//2]
        if new_val < mid:
          mouse.position = info[-2]['minus']
          prev_val = info[-2]['vars'][0]
          for _ in range(len(info[-2]['vars'])-1):
            mouse.click(pn.mouse.Button.left)
            slp(0.0355)
          if qac:
            qacmanager.set_val(qac, 0)
          offset = int((new_val-prev_val)//info[-2]['step'])
          mouse.position = info[-2]['plus']
          for _ in range(offset):
            mouse.click(pn.mouse.Button.left)
            slp(0.0355)
          if qac:
            qacmanager.set_val(qac, cast(int, new_val))
        else:
          mouse.position = info[-2]['plus']
          prev_val = info[-2]['vars'][-1]
          for _ in range(len(info[-2]['vars'])-1):
            mouse.click(pn.mouse.Button.left)
            slp(0.0355)
          offset = int((prev_val-new_val)//info[-2]['step'])
          mouse.position = info[-2]['minus']
          for _ in range(offset):
            mouse.click(pn.mouse.Button.left)
            slp(0.0355)
      else:
        print(
            f'Making value {make} must be compatible {info[-2]["vars"]}')
    if info[-2]['step'] == 'string' and isinstance(make, str):
      if make.lower() in info[-2]['vars']:
        make = make.lower()
        index = info[-2]['vars'].index(make)
        mid = len(info[-2]['vars'])//2
        if index < mid:
          mouse.position = info[-2]['minus']
          prev_val = 0
          for _ in range(len(info[-2]['vars'])-1):
            mouse.click(pn.mouse.Button.left)
            slp(0.035)
          offset = index-prev_val
          mouse.position = info[-2]['plus']
          for _ in range(offset):
              mouse.click(pn.mouse.Button.left)
              slp(0.0355)
        else:
          mouse.position = info[-2]['plus']
          prev_val = 2
          for _ in range(len(info[-2]['vars'])-1):
            mouse.click(pn.mouse.Button.left)
            slp(0.035)
          offset = prev_val-index
          mouse.position = info[-2]['minus']
          for _ in range(offset):
              mouse.click(pn.mouse.Button.left)
              slp(0.0355)
        

      else:
        print(
            f'Making value {make} must be compatible {info[-2]["vars"]}')
        return
    if info[-2]['step'] == 'inf5':
      if isinstance(make, str) and make.lower().replace(',', '.') in info[-2]['vars'] or make in info[-2]['vars']:
        if isinstance(make, str) and (make.lower() == 'infinity' or make.lower() == 'inf'):
          index = 0
        elif isinstance(make, str) and make.replace(',', '.').isdigit():
          make = int(make.replace(',', '.'))
          index = info[-2]['vars'].index(make)
        else:
          index = info[-2]['vars'].index(make)
        mid = len(info[-2]['vars'])//2
        if index < mid:
          mouse.position = info[-2]['minus']
          for _ in range(len(info[-2]['vars'])-1):
            mouse.click(pn.mouse.Button.left)
            slp(0.035)
          mouse.position = info[-2]['plus']
          for _ in range(index):
            mouse.click(pn.mouse.Button.left)
            slp(0.0355)
        elif index > mid:
          mouse.position = info[-2]['plus']
          for _ in range(len(info[-2]['vars'])-1):
            mouse.click(pn.mouse.Button.left)
            slp(0.035)
          offset = len(info[-2]['vars'])-1-index
          mouse.position = info[-2]['minus']
          for _ in range(offset):
            mouse.click(pn.mouse.Button.left)
            slp(0.0355)
      else:
        print(
            f'Making value {make} must be compatible {info[-2]["vars"]}')


def set_options(*options: tuple[str, Any]):
  """Universal function for setting needed values to options

  Args:
    options (tuple[tuple[str,str], ...]): In each inner tuple 1st value describes option e.g.->kill_distance, 2nd describes value that must be set
  """
  for option in options:
    info = find_info_by_name(option[0])
    if info is not None and isinstance(info, tuple):
      if info[-1] == 'c':
        info = cast(CheckboxInfo, info)
        goto(info[1])
        calculate_clicks(info, option[1], checkbox(info[-2]))
        slp(0.1)
      elif info[-1] == 'f':
        info = cast(FieldInfo, info)
        goto(info[1])
        if info[0].split('.')[-2] in teams_crewmate_roles | teams_impostor_roles and info[0].split('.')[-1] in ('#', '%'):
          calculate_clicks(info, option[1], qac=(
              info[0].split('.')[-2], cast(Literal['#', '%'], info[0].split('.')[-1])))
        else:
          calculate_clicks(info, option[1])

    else:
      print(f'Wrong name: {option[0]}')


def scroll(was: Cords, will: Cords) -> bool:
  """Scrolles slides from `settings` or `roles_settings.all`, """
  if was != will:
    was_name, will_name = None, None
    for section in settings_sections:
      if settings_sections[section]['cords'] == was:
        was_name = section
      if settings_sections[section]['cords'] == will:
        will_name = section
    for team in ('crewmate_roles', 'impostor_roles'):
      if v['roles_settings']['all'][team]['cords'] == was:
        was_name = team
      if v['roles_settings']['all'][team]['cords'] == will:
        will_name = team
    if was_name and will_name:
      mouse.position = was
      slp(0.15)
      mouse.press(pn.mouse.Button.left)
      slp(0.15)
      mouse.move(0, will[1] - was[1])
      slp(0.15)
      mouse.release(pn.mouse.Button.left)
      printq(f'Scroll: was: {was_name}, became: {will_name}')
    elif not was_name or not will_name:
      print(f'Section cannot be found')
      return False
    else:
      print(f'Sections cannot be found')
      return False
  return True


def checkbox(cords: Cords) -> bool:
  x, y = cords
  screenshot = ImageGrab.grab(
      bbox=(x, y, x+CHECKBOX_SHAPE[0], y+CHECKBOX_SHAPE[1]))
  pixels = np.array(screenshot)
  lower = np.array([c - TOLERANCE for c in TEAL])
  upper = np.array([c + TOLERANCE for c in TEAL])
  mask = np.all((pixels >= lower) & (pixels <= upper), axis=-1)
  return np.any(mask).item()


def iw4_settings(x: int, y: int, button: pn.mouse.Button, pressed: bool):
  global current_setting
  if button == pn.mouse.Button.middle and pressed:
    current_setting = 'standart_settings'
    goto('edit')
    set_options(
        ('settings.impostors.fields.#impostors', 3),
        ('settings.impostors.fields.kill_cooldown', 25),
        ('settings.impostors.fields.impostor_vision', 1.75),
        ('settings.impostors.fields.kill_distance', 'medium'),
        ('settings.crewmates.fields.player_speed', 1.5),
        ('settings.crewmates.fields.crewmate_vision', 1),
        ('settings.meetings.fields.#emergency_meetings', 1),
        ('settings.meetings.fields.emergency_cooldown', 15),
        ('settings.meetings.fields.discussion_time', 30),
        ('settings.meetings.fields.voting_time', 30),
        ('settings.meetings.checkboxes.anonymous_votes', True),
        ('settings.meetings.checkboxes.confirm_ejects', True),
        ('settings.tasks.fields.task_bar_updates', 'meetings'),
        ('settings.tasks.fields.#common', 1),
        ('settings.tasks.fields.#long', 1),
        ('settings.tasks.fields.#short', 2),
        ('settings.tasks.checkboxes.visual_tasks', False),

        ('roles_settings.all.crewmate_roles.engineer.#', 1),
        ('roles_settings.all.crewmate_roles.engineer.%', 100),
        ('roles_settings.all.crewmate_roles.guardian_angel.#', 5),
        ('roles_settings.all.crewmate_roles.guardian_angel.%', 100),
        ('roles_settings.all.crewmate_roles.scientist.#', 3),
        ('roles_settings.all.crewmate_roles.scientist.%', 100),
        ('roles_settings.all.crewmate_roles.tracker.#', 1),
        ('roles_settings.all.crewmate_roles.tracker.%', 100),
        ('roles_settings.all.crewmate_roles.noisemaker.#', 3),
        ('roles_settings.all.crewmate_roles.noisemaker.%', 100),
        ('roles_settings.all.impostor_roles.shapeshifter.#', 1),
        ('roles_settings.all.impostor_roles.shapeshifter.%', 100),
        ('roles_settings.all.impostor_roles.phantom.#', 2),
        ('roles_settings.all.impostor_roles.phantom.%', 100),

        ('roles_settings.engineer.fields.vent_use_cooldown', 10),
        ('roles_settings.engineer.fields.max_time_in_vents', 30),
        ('roles_settings.guardian_angel.fields.protect_cooldown', 40),
        ('roles_settings.guardian_angel.fields.protect_duration', 20),
        ('roles_settings.guardian_angel.checkboxes.protect_visible_to_impostors', False),
        ('roles_settings.scientist.fields.vitals_display_cooldown', 10),
        ('roles_settings.scientist.fields.battery_duration', 30),
        ('roles_settings.tracker.fields.tracking_cooldown', 15),
        ('roles_settings.tracker.fields.tracking_delay', 0),
        ('roles_settings.tracker.fields.tracking_duration', 30),
        ('roles_settings.noisemaker.checkboxes.impostors_get_alert', True),
        ('roles_settings.noisemaker.fields.alert_duration', 1),
        ('roles_settings.shapeshifter.checkboxes.leave_shapeshifting_evidence', True),
        ('roles_settings.shapeshifter.fields.shapeshift_duration', 30),
        ('roles_settings.shapeshifter.fields.shapeshift_cooldown', 10),
        ('roles_settings.phantom.fields.vanish_duration', 40),
        ('roles_settings.phantom.fields.vanish_cooldown', 15),
    )
    qacmanager.clear()


def normal_view():
  clear_console()
  print('\n'.join(manager.written))


def script_view():
  clear_console()
  print(f'First edit enter -> {manager.script['data']['flag']}')
  if manager.script['repr']:
    print('\n'.join(f'{i+1}:{line}' for i,
          line in enumerate(manager.script['repr'])))
  else:
    print('Empty script...')


def printq(*args: Any, **kwargs: Any):
  if not manager.viewing:
    if kwargs.get('sep') is not None:
      manager.written.append(kwargs['sep'].join([str(arg) for arg in args]))
    else:
      manager.written.append(' '.join([str(arg) for arg in args]))
  print(*args, **kwargs)


def inputq(string: str = '') -> str:
  if manager.viewing and not manager.running:
    nline()
  inp = input(string)
  if not manager.viewing:
    if inp.lower().strip() not in ('view', 'v'):
      manager.written.append(string+inp)
  return inp


def isfloat(s: str) -> bool:
  try:
    s = s.replace(',', '.')
    float(s)
    return (s.count('.') <= 1 and
            s.replace('.', '').isdigit() and
            len(s.replace('.', '')) > 0)
  except (ValueError, AttributeError):
    return False


def set_check(name: str, make: str) -> bool:
  info = find_info_by_name(name)
  if isinstance(info, tuple) and len(info) == 4:
    if info[-1] == 'f':
      info = cast(FieldInfo, info)
      if isinstance(info[-2]['step'], int):
        if make.isdigit() and int(make) in info[-2]['vars']:
          return True
        else:
          printq(
              f'Making value {make} must be compatible {info[-2]["vars"]}')
          return False
      if isinstance(info[-2]['step'], float):
        make = make.replace(',', '.')
        if isfloat(make) and float(make) in info[-2]['vars']:
          return True
        else:
          printq(
              f'Making value {make} must be compatible {info[-2]["vars"]}')
          return False
      if info[-2]['step'] == 'string':
        if make in info[-2]['vars']:
          return True
        else:
          printq(
              f'Making value {make} must be compatible {info[-2]["vars"]}')
          return False
      if info[-2]['step'] == 'inf5':
        if make == 'infinite' or make in info[-2]['vars'] or make.isdigit() and int(make) in info[-2]['vars']:
          return True
        else:
          printq(
              f'Making value {make} must be compatible {info[-2]["vars"]}')
          return False
    if info[-1] == 'c':
      if make in ('true', 'false'):
        return True
      else:
        printq(
            f'Making value {make} must be compatible {('true', 'false')}')
        return False
  printq(f'Incorrect name {name}')
  return False


def nline():
  print(f'{len(manager.script['repr'])+1}:', end='')


if __name__ == '__main__':
  choice = check("Iaw4tch's settings", "Enter shell")
  match choice:
    case '1':
      print('Press middle button to start applying settings')
      with pn.mouse.Listener(on_click=iw4_settings) as listener:
        listener.join()
    case '2':
      printq("Type 'help' for help")
      while (inp := inputq().lower().strip()) not in ('e', 'exit'):
        manager.commanding(inp)
    case _:
      pass
