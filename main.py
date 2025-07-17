import pynput as pn  # For mouse control
from time import sleep as slp  # For delay
from ctypes import windll  # For windows scale disable
import numpy as np  # For 3d color array
from PIL import ImageGrab  # For grabbing images
from typing import TypedDict, Literal, Any, Union, cast  # Type annotations
from os import system, name

windll.user32.SetProcessDPIAware()

Cords = tuple[int, int]


class FieldDict(TypedDict):
  minus: Cords
  plus: Cords
  vars: tuple[Any, ...]
  step: int | float | Literal['string', 'inf5']


class CrewmatesDict(TypedDict):
  cords: Cords
  fields: dict[str, FieldDict]
  checkboxes: None


class SectionDict(TypedDict):
  cords: Cords
  fields: dict[str, FieldDict]
  checkboxes: dict[str, tuple[int, int]] | None


class SectionsDict(TypedDict):
  cords: Cords
  impostors: SectionDict
  crewmates: SectionDict
  meetings: SectionDict
  tasks: SectionDict


QuantityAndChance = TypedDict('QuantityAndChance', {
    '#': FieldDict,
    '%': FieldDict
})


class CrewmateRolesDict(TypedDict):
  cords: Cords
  engineer: QuantityAndChance
  guardian_angel: QuantityAndChance
  scientist: QuantityAndChance
  tracker: QuantityAndChance
  noisemaker: QuantityAndChance


class ImpostorRolesDict(TypedDict):
  cords: Cords
  shapeshifter: QuantityAndChance
  phantom: QuantityAndChance


class ScrollForAllDict(TypedDict):
  cords: Cords
  crewmate_roles: CrewmateRolesDict
  impostor_roles: ImpostorRolesDict


class RoleDict(TypedDict):
  cords: Cords
  all: ScrollForAllDict
  engineer: SectionDict
  guardian_angel: SectionDict
  scientist: SectionDict
  tracker: SectionDict
  noisemaker: SectionDict
  shapeshifter: SectionDict
  phantom: SectionDict


class SettingsDict(TypedDict):
  edit: Cords
  settings: SectionsDict
  roles_settings: RoleDict


v: SettingsDict = {
    'edit': (1584, 751),
    'settings': {
        'cords': (425, 776),
        'impostors': {
            'cords': (1803, 440),
            'fields': {
                '#impostors': {
                    'minus': (1288, 608),
                    'plus': (1559, 604),
                    'vars': (1, 2, 3),
                    'step': 1,
                },
                'kill_cooldown': {
                    'minus': (1290, 689),
                    'plus': (1556, 691),
                    'vars': tuple(map(float, np.arange(10, 61, 2.5))),
                    'step': 2.5,
                },
                'impostor_vision': {
                    'minus': (1293, 773),
                    'plus': (1552, 763),
                    'vars': tuple(map(float, np.arange(0.25, 5.1, 0.25))),
                    'step': 0.25,
                },
                'kill_distance': {
                    'minus': (1294, 844),
                    'plus': (1554, 846),
                    'vars': ('short', 'medium', 'long'),
                    'step': 'string',
                },
            },

            'checkboxes': None,
        },
        'crewmates': {
            'cords': (1803, 632),
            'fields': {
                'player_speed': {
                    'minus': (1293, 516),
                    'plus': (1551, 514),
                    'vars': tuple(map(float, np.arange(0.5, 3.1, 0.25))),
                    'step': 0.25,
                },
                'crewmate_vision': {
                    'minus': (1294, 597),
                    'plus': (1549, 596),
                    'vars': tuple(map(float, np.arange(0.25, 5.1, 0.25))),
                    'step': 0.25,
                },
            },
            'checkboxes': None,
        },
        'meetings': {
            'cords': (1800, 766),
            'fields': {
                '#emergency_meetings': {
                    'minus': (1294, 413),
                    'plus': (1553, 412),
                    'vars': tuple(range(10)),
                    'step': 1,
                },
                'emergency_cooldown': {
                    'minus': (1290, 490),
                    'plus': (1556, 491),
                    'vars': tuple(range(0, 61, 5)),
                    'step': 5,
                },
                'discussion_time': {
                    'minus': (1293, 571),
                    'plus': (1551, 573),
                    'vars': tuple(range(0, 121, 15)),
                    'step': 15,
                },
                'voting_time': {
                    'minus': (1291, 654),
                    'plus': (1550, 655),
                    'vars': tuple(range(0, 301, 15)),
                    'step': 15,
                },
            },
            'checkboxes': {
                'anonymous_votes': (1272, 721),
                'confirm_ejects': (1273, 804),
            },
        },
        'tasks': {
            'cords': (1803, 941),
            'fields': {
                'task_bar_updates': {
                    'minus': (1290, 533),
                    'plus': (1550, 530),
                    'vars': ('always', 'meetings', 'never'),
                    'step': 'string',
                },
                '#common_tasks': {
                    'minus': (1291, 612),
                    'plus': (1551, 610),
                    'vars': (0, 1, 2),
                    'step': 1,
                },
                '#long_tasks': {
                    'minus': (1292, 694),
                    'plus': (1549, 689),
                    'vars': (0, 1, 2, 3),
                    'step': 1,
                },
                '#short_tasks': {
                    'minus': (1291, 774),
                    'plus': (1552, 772),
                    'vars': (0, 1, 2, 3, 4, 5),
                    'step': 1,
                },
            },
            'checkboxes': {
                'visual_tasks': (1275, 829),
            },
        },

    },

    'roles_settings': {
        'cords': (405, 894),
        'all': {
            'cords': (743, 286),
            'crewmate_roles': {
                'cords': (1804, 437),
                'engineer': {
                    '#':  {
                        'minus': (1135, 611),
                        'plus': (1327, 610),
                        'vars': tuple(range(16)),
                        'step': 1,
                    },
                    '%': {
                        'minus': (1490, 609),
                        'plus': (1681, 608),
                        'vars': tuple(range(0, 101, 10)),
                        'step': 10,
                    },
                },
                'guardian_angel': {
                    '#':  {
                        'minus': (1139, 686),
                        'plus': (1329, 685),
                        'vars': tuple(range(16)),
                        'step': 1,
                    },
                    '%': {
                        'minus': (1489, 686),
                        'plus': (1682, 685),
                        'vars': tuple(range(0, 101, 10)),
                        'step': 10,
                    },
                },
                'scientist': {
                    '#':  {
                        'minus': (1136, 765),
                        'plus': (1326, 764),
                        'vars': tuple(range(16)),
                        'step': 1,
                    },
                    '%': {
                        'minus': (1490, 764),
                        'plus': (1681, 763),
                        'vars': tuple(range(0, 101, 10)),
                        'step': 10,
                    },
                },
                'tracker': {
                    '#':  {
                        'minus': (1136, 844),
                        'plus': (1327, 841),
                        'vars': tuple(range(16)),
                        'step': 1,
                    },
                    '%': {
                        'minus': (1488, 841),
                        'plus': (1682, 839),
                        'vars': tuple(range(0, 101, 10)),
                        'step': 10,
                    },
                },
                'noisemaker': {
                    '#':  {
                        'minus': (1136, 918),
                        'plus': (1328, 919),
                        'vars': tuple(range(16)),
                        'step': 1,
                    },
                    '%': {
                        'minus': (1489, 918),
                        'plus': (1680, 917),
                        'vars': tuple(range(0, 101, 10)),
                        'step': 10,
                    },
                },
            },
            'impostor_roles': {
                'cords': (1802, 951),
                'shapeshifter': {
                    '#':  {
                        'minus': (1134, 821),
                        'plus':  (1328, 820),
                        'vars': tuple(range(16)),
                        'step': 1,
                    },
                    '%': {
                        'minus': (1488, 820),
                        'plus': (1681, 819),
                        'vars': tuple(range(0, 101, 10)),
                        'step': 10,
                    },
                },
                'phantom': {
                    '#':  {
                        'minus': (1136, 899),
                        'plus':  (1327, 897),
                        'vars': tuple(range(16)),
                        'step': 1,
                    },
                    '%': {
                        'minus': (1490, 898),
                        'plus': (1682, 897),
                        'vars': tuple(range(0, 101, 10)),
                        'step': 10,
                    },
                },
            },
        },
        'engineer': {
            'cords': (884, 286),
            'fields': {
                'vent_use_cooldown': {
                    'minus': (1452, 739),
                    'plus': (1711, 737),
                    'vars': tuple(range(5, 61, 5)),
                    'step': 5,
                },
                'max_time_in_vents': {
                    'minus': (1452, 820),
                    'plus': (1711, 819),
                    'vars': ('inf', *range(5, 61, 5)),
                    'step': 'inf5',
                },
            },
            'checkboxes': None,
        },
        'guardian_angel': {
            'cords': (1020, 286),
            'fields': {
                'protect_cooldown': {
                    'minus': (1451, 738),
                    'plus': (1710, 735),
                    'vars': tuple(range(35, 121, 5)),
                    'step': 5,
                },
                'protect_duration': {
                    'minus': (1452, 819),
                    'plus': (1711, 819),
                    'vars': tuple(range(5, 31, 5)),
                    'step': 5,
                },
            },
            'checkboxes': {
                'protect_visible_to_impostors': (1433, 875),
            },
        },
        'scientist': {
            'cords': (1157, 285),
            'fields': {
                'vitals_display_cooldown': {
                    'minus': (1452, 737),
                    'plus': (1711, 736),
                    'vars': tuple(range(5, 61, 5)),
                    'step': 5,
                },
                'battery_duration': {
                    'minus': (1450, 819),
                    'plus': (1711, 818),
                    'vars': tuple(range(5, 31, 5)),
                    'step': 5,
                },
            },
            'checkboxes': None,
        },
        'tracker': {
            'cords': (1290, 286),
            'fields': {
                'tracking_cooldown': {
                    'minus': (1451, 737),
                    'plus': (1711, 737),
                    'vars': tuple(range(10, 121, 5)),
                    'step': 5,
                },
                'tracking_delay': {
                    'minus': (1451, 819),
                    'plus': (1710, 817),
                    'vars': tuple(range(4)),
                    'step': 1,
                },
                'tracking_duration': {
                    'minus': (1453, 900),
                    'plus': (1712, 899),
                    'vars': tuple(range(10, 121, 5)),
                    'step': 5,
                },
            },
            'checkboxes': None,
        },
        'noisemaker': {
            'cords': (1429, 283),
            'checkboxes': {
                'impostors_get_alert': (1433, 713),
            },
            'fields': {
                'alert_duration': {
                    'minus': (1451, 818),
                    'plus': (1711, 818),
                    'vars': tuple(range(1, 16)),
                    'step': 1,
                },
            },
        },
        'shapeshifter': {
            'cords': (1564, 286),
            'checkboxes': {
                'leave_shapeshifting_evidence': (1433, 712),
            },
            'fields': {
                'shapeshift_duration': {
                    'minus': (1452, 820),
                    'plus': (1711, 820),
                    'vars': ('inf', *range(5, 31, 5)),
                    'step': 'inf5',
                },
                'shapeshift_cooldown': {
                    'minus': (1452, 903),
                    'plus': (1712, 901),
                    'vars': tuple(range(5, 91, 5)),
                    'step': 5,
                },
            },
        },
        'phantom': {
            'cords': (1701, 283),
            'fields': {
                'vanish_duration': {
                    'minus': (1453, 738),
                    'plus': (1711, 738),
                    'vars': tuple(range(10, 91, 10)),
                    'step': 10,
                },
                'vanish_cooldown': {
                    'minus': (1450, 819),
                    'plus': (1711, 820),
                    'vars': tuple(range(5, 61, 5)),
                    'step': 5,
                },
            },
            'checkboxes': None,
        },
    },

}

settings_sections = cast(dict[str, SectionDict], {
    k: val
    for k, val in v['settings'].items()
    if k != 'cords'
})
roles_settings_roles = cast(dict[str, SectionDict], {
    k: val
    for k, val in v['roles_settings'].items()
    if k != 'all' and k != 'cords'
})
roles_settings_roles_all = cast(dict[str, ScrollForAllDict | SectionDict], {
    k: val
    for k, val in v['roles_settings'].items()
    if k != 'cords'
})
all_teams = cast(dict[str, CrewmateRolesDict | ImpostorRolesDict], {
    k: val
    for k, val in v['roles_settings']['all'].items()
    if k != 'cords'
})
teams_crewmate_roles = cast(dict[str, QuantityAndChance], {
    k: val
    for k, val in v['roles_settings']['all']['crewmate_roles'].items()
    if k != 'cords'
})
teams_impostor_roles = cast(dict[str, QuantityAndChance], {
    k: val
    for k, val in v['roles_settings']['all']['impostor_roles'].items()
    if k != 'cords'
})
current_settings_section = v['settings']['impostors']['cords']
clicks: list[tuple[int, int]] = []
counter = 0
TEAL = (44, 243, 198)
TOLERANCE = 30
CHECKBOX_SHAPE = (60, 60)
current_setting = 'standart_settings'
current_all_section = 'crewmate_roles'
FieldInfo = tuple[str, FieldDict, Literal['f']]
CheckboxInfo = tuple[str, Cords, Literal['c']]
goedit = True
script: dict[str, list[str]]= {'exec':[], 'repr':[]}
written: list[str] = []
viewing: bool = False


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
  check_what = inputq('\n'.join(again)+'\n> ')
  while True:
    if check_what in map(str, range(1, len(check_to)+1)):
      break
    else:
      printq('Invalid input')
      check_what = inputq('\n'.join(again)+'\n> ')
  return check_what


def clear_console():
  """Clears text from the console"""
  system('cls' if name == 'nt' else 'clear')


def find_info_by_name(name: str, commanding: bool = False, get_path: bool = False) -> Union[
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
      get_path (bool): Gives recursively searched path for a name

    Returns:
      out                    
      One of many possible return types depending on what's found:
      - tuple[int, int]: When coordinates are found (x, y)
      - int | float | str: When a step value found
      - list[str]: When returning available keys for a dictionary level
      - None: When path doesn't resolve or no checkboxes in section
      - tuple[str, dict, Literal['f', 'c']]: Structured return:
        * (section_name, field_data, 'f') for fields
        * (section_name, cords_data, 'c') for checkboxes

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
      ('impostors', {...}, 'f')
      >>> find_info_by_name('noisemaker.#')
      ('crewmate_roles', {...}, 'f')
      Get full path:
      >>> find_info_by_name('protect_visible_to_impostors', get_path=True)
      'roles_settings.guardian_angel.checkboxes.protect_visible_to_impostors'
    """
  if name.startswith('v.'):
    name = name[2:]
  if name == 'v' or name == '.':
    return list(cast(list[str], v.keys()))
  if name.startswith('.'):
    name = name[1:]
  if name == '':
    return "Try type 'help'"
  current: Any = v
  parts = name.split('.')
  if not commanding:
    try:
      if len(parts) == 4 and parts[0] == 'settings' and parts[1] in settings_sections and parts[2] == 'fields' and parts[3] in settings_sections[parts[1]]['fields']:
        section = parts[1]
        field = settings_sections[section]['fields'][parts[3]]
        return section, field, 'f'
    except:
      pass
    try:
      if len(parts) == 4 and parts[0] == 'settings' and parts[1] in settings_sections and parts[2] == 'checkboxes' and parts[3] in cast(dict[str, Cords], settings_sections[parts[1]]['checkboxes']):
        section = parts[1]
        checkbox = cast(dict[str, Cords], settings_sections[section]['checkboxes'])[
            parts[3]]
        return section, checkbox, 'c'
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
        return team, field, 'f'
    except:
      pass
    try:
      if len(parts) == 4 and parts[0] == 'roles_settings' and parts[1] in roles_settings_roles and parts[2] in 'fields' and parts[3] in roles_settings_roles[parts[1]]['fields']:
        role = parts[1]
        return role, roles_settings_roles[role]['fields'][parts[3]], 'f'
    except:
      pass
    try:
      if len(parts) == 4 and parts[0] == 'roles_settings' and parts[1] in roles_settings_roles and parts[2] in 'checkboxes' and parts[3] in cast(dict[str, Cords], roles_settings_roles[parts[1]]['checkboxes']):
        role = parts[1]
        return role,  cast(dict[str, Cords], roles_settings_roles[parts[1]]['checkboxes'])[parts[3]], 'c'
    except:
      pass

  for part in parts:
    if isinstance(current, dict) and part in current:
      current = cast(Any, current[part])
    else:
      if current is v:
        if part in settings_sections:
          if not get_path:
            return find_info_by_name(f'settings.{name}', commanding=commanding)
          else:
            return f'settings.{name}'

        for section in settings_sections:
          if part in v['settings'][section]['fields']:
            if not get_path:
              return find_info_by_name(f'settings.{section}.fields.{name}', commanding=commanding)
            else:
              return f'settings.{section}.fields.{name}'
          if v['settings'][section]['checkboxes'] is not None and part in v['settings'][section]['checkboxes']:
            if not get_path:
              return find_info_by_name(f'settings.{section}.checkboxes.{name}', commanding=commanding)
            else:
              return f'settings.{section}.checkboxes.{name}'

        if part in all_teams:
          if not get_path:
            return find_info_by_name(f'roles_settings.all.{name}')
          else:
            return f'roles_settings.all.{name}'

        if len(parts) >= 2 and '#' in parts or '%' in parts:
          for i in range(len(parts)):
            if parts[i] in ('#', '%'):
              if parts[i-1] in teams_crewmate_roles:
                if not get_path:
                  return find_info_by_name(f'roles_settings.all.crewmate_roles.{name}', commanding=commanding)
                else:
                  return f'roles_settings.all.crewmate_roles.{name}'
              if parts[i-1] in teams_impostor_roles:
                if not get_path:
                  return find_info_by_name(f'roles_settings.all.impostor_roles.{name}', commanding=commanding)
                else:
                  return f'roles_settings.all.impostor_roles.{name}'
              break

        if part in roles_settings_roles_all:
          if not get_path:
            return find_info_by_name(f'roles_settings.{name}', commanding=commanding)
          else:
            return f'roles_settings.{name}'

        for section in roles_settings_roles:
          if part in v['roles_settings'][section]['fields']:
            if not get_path:
              return find_info_by_name(f'roles_settings.{section}.fields.{name}', commanding=commanding)
            else:
              return f'roles_settings.{section}.fields.{name}'
          if v['roles_settings'][section]['checkboxes'] is not None and part in v['roles_settings'][section]['checkboxes']:
            if not get_path:
              return find_info_by_name(f'roles_settings.{section}.checkboxes.{name}', commanding=commanding)
            else:
              return f'roles_settings.{section}.checkboxes.{name}'

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
    print('Went to edit')
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
      print('Section:', section)
      current_all_section = section
  slp(0.05)


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
          new_val = int(make)
        else:
          print(f'Making value {make} is NaN')
          return
      else:
        new_val = make
      if make in info[-2]['vars']:
        mid = info[-2]['vars'][len(info[-2]['vars'])//2]
        if new_val < mid:
          mouse.position = info[-2]['minus']
          prev_val = info[-2]['vars'][0]
          for _ in range(len(info[-2]['vars'])-1):
            mouse.click(pn.mouse.Button.left)
            slp(0.0355)
          offset = int((new_val-prev_val)//info[-2]['step'])
          mouse.position = info[-2]['plus']
          for _ in range(offset):
            mouse.click(pn.mouse.Button.left)
            slp(0.0355)
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
          for _ in range(len(info[-2]['vars'])-1):
            mouse.click(pn.mouse.Button.left)
            slp(0.035)
        elif index > mid:
          mouse.position = info[-2]['plus']
          for _ in range(len(info[-2]['vars'])-1):
            mouse.click(pn.mouse.Button.left)
            slp(0.035)
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


def set_options(*options: tuple[Any, ...]):
  """Universal function for setting needed values to options

  Args:
    options (tuple[tuple[str,str], ...]): In each inner tuple 1st value describes option e.g.->kill_distance, 2nd describes value that must be set
  """
  for option in options:
    info = find_info_by_name(option[0])
    if info is not None and isinstance(info, tuple):
      if info[-1] == 'c':
        info = cast(CheckboxInfo, info)
        goto(info[0])
        calculate_clicks(info, option[1], checkbox(info[-2]))
        slp(0.1)
      elif info[-1] == 'f':
        info = cast(FieldInfo, info)
        goto(info[0])
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
  global goedit
  if button == pn.mouse.Button.middle and pressed:
    if goedit:
      goto('edit')
      goedit = False
    set_options(
        ('settings.impostors.fields.#impostors', 3),
        ('settings.impostors.fields.kill_cooldown', 25),
        ('settings.impostors.fields.impostor_vision', 1.75),
        ('settings.impostors.fields.kill_distance', 'short'),
        ('settings.crewmates.fields.player_speed', 1.5),
        ('settings.crewmates.fields.crewmate_vision', 1),
        ('settings.meetings.fields.#emergency_meetings', 1),
        ('settings.meetings.fields.emergency_cooldown', 20),
        ('settings.meetings.fields.discussion_time', 30),
        ('settings.meetings.fields.voting_time', 30),
        ('settings.meetings.checkboxes.anonymous_votes', True),
        ('settings.meetings.checkboxes.confirm_ejects', True),
        ('settings.tasks.fields.task_bar_updates', 'Always'),
        ('settings.tasks.fields.#common_tasks', 1),
        ('settings.tasks.fields.#long_tasks', 1),
        ('settings.tasks.fields.#short_tasks', 2),
        ('settings.tasks.checkboxes.visual_tasks', True),

        ('roles_settings.all.crewmate_roles.engineer.#', 2),
        ('roles_settings.all.crewmate_roles.engineer.%', 100),
        ('roles_settings.all.crewmate_roles.guardian_angel.#', 5),
        ('roles_settings.all.crewmate_roles.guardian_angel.%', 100),
        ('roles_settings.all.crewmate_roles.scientist.#', 3),
        ('roles_settings.all.crewmate_roles.scientist.%', 100),
        ('roles_settings.all.crewmate_roles.tracker.#', 2),
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


def view(script: list[str]) -> str:
  if script:
    for i in range(len(script)):
      script[i] = script[i].replace(
          '_options((', ' ').replace(',', '').replace('))', '')
    return '\n'.join([f'{i+1}:{line}' for i, line in enumerate(script)])
  else:
    return 'Empty'


def printq(*args: Any, **kwargs: Any):
  global written
  if kwargs.get('sep') is not None:
    written.append(kwargs['sep'].join([str(arg) for arg in args]))
  else:
    written.append(' '.join([str(arg) for arg in args]))
  print(*args, **kwargs)


def inputq(string: str = '') -> Any:
  global written
  inp = input(string)
  written.append(string+inp)
  return inp


def commanding(inp: str):
  global written, viewing
  if not viewing:
    if inp.lower() == 'v':
      clear_console()
      print(view(script))
      viewing = True
      return
    else:
      written.append(inp)
      inp = inp.lower()
      if inp == 'help':
        printq(
            '''Commands:
-------------------------------------------------------------------
set {option name} {option value}
v -> toggle code view
rm {index} -> removes entered lines by index (-indexes supported)
. -> top level dict
save -> .json
run -> middle button to start setting''')
        return
      parts = inp.split()
      if len(parts) > 0 and parts[0] == 'set':
        if len(parts) == 3:
          full_name = find_info_by_name(parts[1], get_path=True)
          if full_name is not None:
            if isinstance((info := find_info_by_name(parts[1])), tuple) and info[-1] == 'f':
              info = cast(FieldInfo, info)
              if isinstance(info[-2]['step'], int) and int(parts[2]) in info[-2]['vars'] or isinstance(info[-2]['step'], float) and parts[2] in info[-2]['vars']:
                script['exec'].append(
                    f'set_options(({full_name}, {parts[2]}))')
                script['repr'].append(f'set {parts[1]} {parts[2]}')
                return
              else:
                printq('Setting value must be able to be set in the game')
                return
            if isinstance((info := find_info_by_name(parts[1])), tuple) and info[-1] == 'c':
              if parts[2] in ('true','false'):
                script['exec'].append(
                    f'set_options(({full_name}, {parts[2]}))')
                script['repr'].append(f'set {parts[1]} {parts[2]}')
                return
              else:
                printq('Setting value must be able to be set in the game')
                return
          else:
            printq(f'Name {parts[1]} does not exist')
            return
        else:
          printq('Set command takes two arguments')
          return

      if (info := find_info_by_name(inp, commanding=True)) is not None:
        printq(info)
      else:
        printq('Unknown command')
  else:
    if inp == 'v':
      clear_console()
      print('\n'.join(written))
      viewing = False
      return
    else:
      print("Type 'v' to exit viewing mode")


if __name__ == '__main__':
  mouse = pn.mouse.Controller()
  choice = check("Iaw4tch's settings", 'Load from file', 'Create new')
  match choice:
    case '1':
      print('Press middle button to start applying settings')
      with pn.mouse.Listener(on_click=iw4_settings) as listener:
        listener.join()
    case '2':
      ...
    case '3':
      printq("Entering command shell. Try type 'help' for help")
      while (inp:=input()).lower() not in ('e', 'exit'):
        commanding(inp)
    case _:
      pass
