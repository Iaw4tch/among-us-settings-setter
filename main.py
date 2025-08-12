import pynput as pn  # Mouse control
from time import sleep as slp  # Delay
import ctypes   # Windows scale disable, window control
import numpy as np  # 3d color array
from PIL import ImageGrab  # Grabbing images
from typing import Any, Union, cast, Hashable  # Type annotations
from os import system, name  # Console clear
from data import *  # Info messages and type annotations
import tkinter as tk  # GUI
from tkinter import filedialog  # Warning
import json  # Saving script
from threading import Thread  # Opportunity to stop launched script
from difflib import get_close_matches  # Command prompter


class ConsoleManager:
  def __init__(self):
    self.viewing = False
    self.script: ScriptDict = {
        'data': {'flag': False, 'lines': []}, 'repr': []}
    self.handlers: Handlers = {
        'args': {
            ('remove', 'rm'): self.handle_remove,
            ('insert', 'ins'): self.handle_insert,
            ('replace', 'r'): self.handle_replace,
        },
        'noargs': {
            'help': lambda: print(command_info),
            'edit': self.handle_edit,
            'run': lambda: Thread(target=self.handle_run).start(),
            'stop': self.handle_stop,
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
      review()

  def get_close_command(self, cmd: str) -> bool:
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

  def get_close_name(self, name: str) -> bool:
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

  def find_probable_compilance(self, cmd: str):
    if not self.get_close_command(cmd):
      if (info := find_info_by_name(inp, commanding=True)) is not None:
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
              probable.append('<Unable to find>')
        if not no_real_info:
          print(f'Unknown object, did you mean {'.'.join(probable)}?')
        else:
          if not self.get_close_name(cmd):
            print('Cannot find information about this')

  def handle_set(self, parameter: str, value: str):
    if set_check(parameter, value):
      self.script['data']['lines'].append(
          (cast(CheckboxInfo | FieldInfo, find_info_by_name(parameter))[0], value))
      self.script['repr'].append(f'{parameter} > {value}')
      review()

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
    review()

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
    review()

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
    review()

  def handle_run(self):
    global current_setting
    if self.script['data']:
      current_setting = 'standart_settings'
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
      qacmanager.clear()

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
    review()

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
    review()


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
      print(f'Role {role} is not in a role')

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


ctypes.windll.user32.SetProcessDPIAware()
mouse = pn.mouse.Controller()
qacmanager = QACManager()
current_settings_section = v['settings']['impostors']['cords']
current_setting = 'standart_settings'
current_all_section = 'crewmate_roles'


def valid_index(index: int, script: list[Any]) -> bool:
  if index == 0:
    print('Unsupported index 0')
    return False
  if abs(index)-1 > len(script):
    print('Index out of script range')
    return False
  return True


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
  check_what = input('\n'.join(again)+'\n> ').strip()
  while True:
    if check_what in map(str, range(1, len(check_to)+1)):
      break
    else:
      print('Invalid input')
      check_what = input('\n'.join(again)+'\n> ').strip()
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
    return '{'+',\n'.join(v.keys())+'}'
  if name.startswith('.'):
    name = name[1:]
  current: Any = v
  parts = name.split('.')
  if not commanding:
    if len(parts) == 4:
      if parts[0] == 'settings':
        if parts[1] in SETTINGS_SECTIONS and parts[2] == 'fields' and parts[3] in SETTINGS_SECTIONS[parts[1]]['fields']:
          section = parts[1]
          field = SETTINGS_SECTIONS[section]['fields'][parts[3]]
          return name, section, field, 'f'

        if parts[1] in SETTINGS_SECTIONS and parts[2] == 'checkboxes' and parts[3] in cast(dict[str, Cords], SETTINGS_SECTIONS[parts[1]]['checkboxes']):
          section = parts[1]
          checkbox = cast(dict[str, Cords], SETTINGS_SECTIONS[section]['checkboxes'])[
              parts[3]]
          return name, section, checkbox, 'c'

      if parts[0] == 'roles_settings':
        if parts[1] in ROLES_SETTINGS_ROLES and parts[2] in 'fields' and parts[3] in ROLES_SETTINGS_ROLES[parts[1]]['fields']:
          role = parts[1]
          return name, role, ROLES_SETTINGS_ROLES[role]['fields'][parts[3]], 'f'

        if parts[1] in ROLES_SETTINGS_ROLES and parts[2] in 'checkboxes' and parts[3] in cast(dict[str, Cords], ROLES_SETTINGS_ROLES[parts[1]]['checkboxes']):
          role = parts[1]
          return name, role,  cast(dict[str, Cords], ROLES_SETTINGS_ROLES[parts[1]]['checkboxes'])[parts[3]], 'c'

    if len(parts) == 5 and parts[0] == 'roles_settings' and parts[1] == 'all' and parts[2] in ALL_TEAMS and parts[3] in {
        k: val
        for k, val in ALL_TEAMS[parts[2]].items()
        if k != 'cords'
    } and parts[4] in ('#', '%'):
      team = parts[2]
      role = parts[3]
      cont = parts[4]
      field = cast(FieldDict, ALL_TEAMS[team][role][cont])
      return name, team, field, 'f'

  for part in parts:
    if isinstance(current, dict) and part in current:
      current = cast(Any, current[part])
    else:
      if current is v:
        if part in SETTINGS_SECTIONS:
          return find_info_by_name(f'settings.{name}', commanding=commanding)

        for section in SETTINGS_SECTIONS:
          if part in v['settings'][section]['fields']:
            return find_info_by_name(f'settings.{section}.fields.{name}', commanding=commanding)

          if v['settings'][section]['checkboxes'] is not None and part in v['settings'][section]['checkboxes']:
            return find_info_by_name(f'settings.{section}.checkboxes.{name}', commanding=commanding)

        if part in ALL_TEAMS:
          return find_info_by_name(f'roles_settings.all.{name}')

        if len(parts) >= 2 and '#' in parts or '%' in parts:
          for i in range(len(parts)):
            if parts[i] in ('#', '%'):
              if parts[i-1] in TEAMS_CREWMATE_ROLES:
                return find_info_by_name(f'roles_settings.all.crewmate_roles.{name}', commanding=commanding)
              if parts[i-1] in TEAMS_IMPOSTOR_ROLES:
                return find_info_by_name(f'roles_settings.all.impostor_roles.{name}', commanding=commanding)
              break

        if part in ROLES_SETTINGS_ROLES_ALL:
          return find_info_by_name(f'roles_settings.{name}', commanding=commanding)

        for section in ROLES_SETTINGS_ROLES:
          if part in v['roles_settings'][section]['fields']:
            return find_info_by_name(f'roles_settings.{section}.fields.{name}', commanding=commanding)

          if v['roles_settings'][section]['checkboxes'] is not None and part in v['roles_settings'][section]['checkboxes']:
            return find_info_by_name(f'roles_settings.{section}.checkboxes.{name}', commanding=commanding)

      return None
  if isinstance(current, dict):
    current = cast(dict[Hashable, Any], current)
    to_return: list[str] = []
    for key, value in current.items():
      if isinstance(value, dict):
        to_return.append(key)
      else:
        to_return.append(f'{key}: {value}')
    return '{'+',\n'.join(to_return)+'}'
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
    print('Went to edit')
  if section == 'settings':
    set_setting('settings')
    current_all_section = 'crewmate_roles'
  if section == 'roles_settings' or section == 'crewmate_roles' or section == 'all':
    set_setting('roles_settings')
    current_all_section = 'crewmate_roles'
  if section in SETTINGS_SECTIONS:
    set_setting('settings')
    cords = SETTINGS_SECTIONS[section]['cords']
    if scroll(current_settings_section, cords):
      current_settings_section = cords
    current_all_section = 'crewmate_roles'
  if section == 'impostor_roles':
    set_setting('roles_settings')
    if current_all_section != 'impostor_roles':
      scroll(v['roles_settings']['all']['crewmate_roles']['cords'],
             v['roles_settings']['all']['impostor_roles']['cords'])
    current_all_section = 'impostor_roles'
  if section in ROLES_SETTINGS_ROLES:
    set_setting('roles_settings')
    if current_all_section != section:
      mouse.position = ROLES_SETTINGS_ROLES[section]['cords']
      mouse.click(pn.mouse.Button.left)
      print('Section:', section)
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
        print(f'Setting: was: {current_setting}, became: {name}')
        current_setting = 'settings'
    case 'roles_settings':
      if current_setting != 'roles_settings':
        mouse.position = v['roles_settings']['cords']
        mouse.click(pn.mouse.Button.left)
        print(f'Setting: was: {current_setting}, became: {name}')
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
          else:
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
            f'Making value {make} must be compatible {info[-2]['vars']}')

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
            f'Making value {make} must be compatible {info[-2]['vars']}')
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
            f'Making value {make} must be compatible {info[-2]['vars']}')


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
        if info[0].split('.')[-2] in TEAMS_CREWMATE_ROLES | TEAMS_IMPOSTOR_ROLES and info[0].split('.')[-1] in ('#', '%'):
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
    for section in SETTINGS_SECTIONS:
      if SETTINGS_SECTIONS[section]['cords'] == was:
        was_name = section
      if SETTINGS_SECTIONS[section]['cords'] == will:
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
      print(f'Scroll: was: {was_name}, became: {will_name}')
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
    goto('edit')
    current_setting = 'standart_settings'
    set_options(
        ('settings.impostors.fields.#impostors', 3),
        ('settings.impostors.fields.kill_cooldown', 22.5),
        ('settings.impostors.fields.impostor_vision', 1.75),
        ('settings.impostors.fields.kill_distance', 'medium'),
        ('settings.crewmates.fields.player_speed', 1.25),
        ('settings.crewmates.fields.crewmate_vision', 1),
        ('settings.meetings.fields.#emergency_meetings', 1),
        ('settings.meetings.fields.emergency_cooldown', 10),
        ('settings.meetings.fields.discussion_time', 15),
        ('settings.meetings.fields.voting_time', 60),
        ('settings.meetings.checkboxes.anonymous_votes', True),
        ('settings.meetings.checkboxes.confirm_ejects', True),
        ('settings.tasks.fields.task_bar_updates', 'meetings'),
        ('settings.tasks.fields.#common', 1),
        ('settings.tasks.fields.#long', 1),
        ('settings.tasks.fields.#short', 3),
        ('settings.tasks.checkboxes.visual_tasks', False),

        ('roles_settings.all.crewmate_roles.engineer.#', 1),
        ('roles_settings.all.crewmate_roles.engineer.%', 100),
        ('roles_settings.all.crewmate_roles.guardian_angel.#', 5),
        ('roles_settings.all.crewmate_roles.guardian_angel.%', 100),
        ('roles_settings.all.crewmate_roles.scientist.#', 0),
        ('roles_settings.all.crewmate_roles.scientist.%', 0),
        ('roles_settings.all.crewmate_roles.tracker.#', 1),
        ('roles_settings.all.crewmate_roles.tracker.%', 100),
        ('roles_settings.all.crewmate_roles.noisemaker.#', 2),
        ('roles_settings.all.crewmate_roles.noisemaker.%', 100),
        ('roles_settings.all.impostor_roles.shapeshifter.#', 1),
        ('roles_settings.all.impostor_roles.shapeshifter.%', 100),
        ('roles_settings.all.impostor_roles.phantom.#', 2),
        ('roles_settings.all.impostor_roles.phantom.%', 100),

        ('roles_settings.engineer.fields.vent_use_cooldown', 5),
        ('roles_settings.engineer.fields.max_time_in_vents', 50),
        ('roles_settings.guardian_angel.fields.protect_cooldown', 35),
        ('roles_settings.guardian_angel.fields.protect_duration', 15),
        ('roles_settings.guardian_angel.checkboxes.protect_visible_to_impostors', False),
        ('roles_settings.tracker.fields.tracking_cooldown', 25),
        ('roles_settings.tracker.fields.tracking_delay', 0),
        ('roles_settings.tracker.fields.tracking_duration', 60),
        ('roles_settings.noisemaker.checkboxes.impostors_get_alert', True),
        ('roles_settings.noisemaker.fields.alert_duration', 15),
        ('roles_settings.shapeshifter.checkboxes.leave_shapeshifting_evidence', True),
        ('roles_settings.shapeshifter.fields.shapeshift_duration', 30),
        ('roles_settings.shapeshifter.fields.shapeshift_cooldown', 10),
        ('roles_settings.phantom.fields.vanish_duration', 40),
        ('roles_settings.phantom.fields.vanish_cooldown', 15),
    )
    qacmanager.clear()


def review():
  clear_console()
  print(f'First edit enter -> {manager.script['data']['flag']}')
  if manager.script['repr']:
    print('\n'.join(f'{i+1}: {line}' for i,
          line in enumerate(manager.script['repr'])))
  else:
    print('Empty script...')


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
          print(
              f'Making value {make} must be compatible {info[-2]["vars"]}')
          return False
      if isinstance(info[-2]['step'], float):
        make = make.replace(',', '.')
        if isfloat(make) and float(make) in info[-2]['vars']:
          return True
        else:
          print(
              f'Making value {make} must be compatible {info[-2]["vars"]}')
          return False
      if info[-2]['step'] == 'string':
        if make in info[-2]['vars']:
          return True
        else:
          print(
              f'Making value {make} must be compatible {info[-2]["vars"]}')
          return False
      if info[-2]['step'] == 'inf5':
        if make == 'infinite' or make in info[-2]['vars'] or make.isdigit() and int(make) in info[-2]['vars']:
          return True
        else:
          print(
              f'Making value {make} must be compatible {info[-2]["vars"]}')
          return False
    if info[-1] == 'c':
      if make in ('true', 'false'):
        return True
      else:
        print(
            f'Making value {make} must be compatible {('true', 'false')}')
        return False
  matches = get_close_matches(name, PARAMETERS_NAMES, n=1)
  if matches:
    print(f"Incorrect name, did you mean '{matches[0]}'?")
  else:
    print(f'Incorrect name {name}')
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
      manager = ConsoleManager()
      print("Script is empty, fisrt edit enter -> False")
      print("Type 'help' if you use shell for the first time")
      while manager.can_repeat_commanding:
        inp = input(
            f'{len(manager.script['repr'])+1}: ').lower().strip()
        manager.commanding(inp)
    case _:
      pass
