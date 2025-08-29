from data import *

from time import sleep as slp

import pynput as pn  # Mouse control
from typing import Any, Union, cast, Hashable  # Type annotations
import numpy as np  # 3d color array
from PIL import ImageGrab  # Grabbing images


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
  if name == 'v':
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


def isfloat(s: str) -> bool:
  try:
    s = s.replace(',', '.')
    float(s)
    return (s.count('.') <= 1 and
            s.replace('.', '').isdigit() and
            len(s.replace('.', '')) > 0)
  except (ValueError, AttributeError):
    return False


class MouseLocation:
  current_setting = 'game_presets'
  current_setting_section = v['settings']['impostors']['cords']
  current_all_section = 'crewmate_roles'


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


mouse = pn.mouse.Controller()
qacm = QACManager()


def checkbox(cords: Cords) -> bool:
  x, y = cords
  screenshot = ImageGrab.grab(
      bbox=(x, y, x+CHECKBOX_SHAPE[0], y+CHECKBOX_SHAPE[1]))
  pixels = np.array(screenshot)
  lower = np.array([c - TOLERANCE for c in TEAL])
  upper = np.array([c + TOLERANCE for c in TEAL])
  mask = np.all((pixels >= lower) & (pixels <= upper), axis=-1)
  return np.any(mask).item()


def set_setting(name: str):
  """Sets new setting and changes global variable `current_setting`"""
  slp(0.05)
  match name:
    case 'settings':
      if MouseLocation.current_setting != 'settings':
        mouse.position = v['settings']['cords']
        mouse.click(pn.mouse.Button.left)
        MouseLocation.current_setting = 'settings'
    case 'roles_settings':
      if MouseLocation.current_setting != 'roles_settings':
        mouse.position = v['roles_settings']['cords']
        mouse.click(pn.mouse.Button.left)
        MouseLocation.current_setting = 'roles_settings'
    case _:
      print('Unknown setting')
  slp(0.05)


def scroll(was: Cords, will: Cords):
  """Scrolles slides from `settings` or `roles_settings.all`"""
  if was != will:
    mouse.position = was
    slp(0.15)
    mouse.press(pn.mouse.Button.left)
    slp(0.15)
    mouse.move(0, will[1] - was[1])
    slp(0.15)
    mouse.release(pn.mouse.Button.left)


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
  if section == 'settings':
    set_setting('settings')
    current_all_section = 'crewmate_roles'
  if section == 'roles_settings' or section == 'crewmate_roles' or section == 'all':
    set_setting('roles_settings')
    current_all_section = 'crewmate_roles'
  if section in SETTINGS_SECTIONS:
    set_setting('settings')
    cords = SETTINGS_SECTIONS[section]['cords']
    scroll(MouseLocation.current_setting_section, cords)
    MouseLocation.current_setting_section = cords
    MouseLocation.current_all_section = 'crewmate_roles'
  if section == 'impostor_roles':
    set_setting('roles_settings')
    if MouseLocation.current_all_section != 'impostor_roles':
      scroll(v['roles_settings']['all']['crewmate_roles']['cords'],
             v['roles_settings']['all']['impostor_roles']['cords'])
      MouseLocation.current_all_section = 'impostor_roles'
  if section in ROLES_SETTINGS_ROLES:
    set_setting('roles_settings')
    if MouseLocation.current_all_section != section:
      mouse.position = ROLES_SETTINGS_ROLES[section]['cords']
      mouse.click(pn.mouse.Button.left)
      MouseLocation.current_all_section = section
  slp(0.0555)


def calculate_clicks(info: FieldInfo | CheckboxInfo,
                     make: int | bool | float | str,
                     inner: bool | None = None,
                     qac: tuple[str, Literal['#', '%']] | None = None
                     ):

  if isinstance(inner, bool) and info[-1] == 'c':
    info = cast(CheckboxInfo, info)
    if isinstance(make, str):
      if make == 'true':
        new = True
      elif make == 'false':
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
        if qac and (prev_val := qacm.get(qac)) is not None:
          offset = int((new_val-prev_val)//info[-2]['step'])
          if offset > 0:
            mouse.position = info[-2]['plus']
            for _ in range(offset):
              mouse.click(pn.mouse.Button.left)
              slp(0.0355)
            qacm.set_val(qac, cast(int, new_val))
            return
          if offset < 0:
            mouse.position = info[-2]['minus']
            for _ in range(-offset):
              mouse.click(pn.mouse.Button.left)
              slp(0.0355)
            qacm.set_val(qac, cast(int, new_val))
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
            qacm.set_val(qac, 0)
          offset = int((new_val-prev_val)//info[-2]['step'])
          mouse.position = info[-2]['plus']
          for _ in range(offset):
            mouse.click(pn.mouse.Button.left)
            slp(0.0355)
          if qac:
            qacm.set_val(qac, cast(int, new_val))
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
