import pynput as pn  # For mouse control
from time import sleep as slp  # For delay
from ctypes import windll  # For windows scale disable
import numpy as np  # For 3d color array
from PIL import ImageGrab
from typing import TypedDict, Literal, Any, Union, cast  # Type annotations

windll.user32.SetProcessDPIAware()

Cords = tuple[int, int]


class FieldInnerDict(TypedDict):
  cords: Cords
  vars: tuple[Any, ...]
  step: int | float | Literal['string', 'inf5']


class FieldDict(TypedDict):
  minus: Cords
  plus: Cords
  field: FieldInnerDict


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


class QuantityAndChance(TypedDict):
  quantity: FieldDict
  chance: FieldDict


class CrewmatesRolesDict(TypedDict):
  cords: Cords
  engineers: QuantityAndChance
  guardian_angels: QuantityAndChance
  scientists: QuantityAndChance
  trackers: QuantityAndChance
  noisemakers: QuantityAndChance


class ImpostorsRolesDict(TypedDict):
  cords: Cords
  shapeshifters: QuantityAndChance
  phantoms: QuantityAndChance


class ScrollForAllDict(TypedDict):
  cords: Cords
  crewmates_roles: CrewmatesRolesDict
  impostors_roles: ImpostorsRolesDict


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
                '#_impostors': {
                    'minus': (1288, 608),
                    'plus': (1559, 604),
                    'field': {
                        'cords': (1330, 583),
                        'vars': (1, 2, 3),
                        'step': 1,
                    },
                },
                'kill_cooldown': {
                    'minus': (1290, 689),
                    'plus': (1556, 691),
                    'field': {
                        'cords': (1330, 663),
                        'vars': tuple(map(float, np.arange(10, 61, 2.5))),
                        'step': 2.5,
                    },
                },
                'impostor_vision': {
                    'minus': (1293, 773),
                    'plus': (1552, 763),
                    'field': {
                        'cords': (1330, 745),
                        'vars': tuple(map(float, np.arange(0.25, 5.1, 0.25))),
                        'step': 0.25,
                    },
                },
                'kill_distance': {
                    'minus': (1294, 844),
                    'plus': (1554, 846),
                    'field': {
                        'cords': (1330, 826),
                        'vars': ('Короткая', 'Средняя', 'Большая'),
                        'step': 'string',
                    },
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
                    'field': {
                        'cords': (1329, 485),
                        'vars': tuple(map(float, np.arange(0.5, 3.1, 0.25))),
                        'step': 0.25,
                    },
                },
                'crewmate_vision': {
                    'minus': (1294, 597),
                    'plus': (1549, 596),
                    'field': {
                        'cords': (1329, 568),
                        'vars': tuple(map(float, np.arange(0.25, 5.1, 0.25))),
                        'step': 0.25,
                    },
                },
            },
            'checkboxes': None,
        },
        'meetings': {
            'cords': (1800, 766),
            'fields': {
                '#_emergency_meetings': {
                    'minus': (1294, 413),
                    'plus': (1553, 412),
                    'field': {
                        'cords': (1329, 401),
                        'vars': tuple(range(10)),
                        'step': 1,
                    },
                },
                'emergency_cooldown': {
                    'minus': (1290, 490),
                    'plus': (1556, 491),
                    'field': {
                        'cords': (1329, 483),
                        'vars': tuple(map(float, np.arange(0.25, 5.1, 0.25))),
                        'step': 0.25,
                    },
                },
                'discussion_time': {
                    'minus': (1293, 571),
                    'plus': (1551, 573),
                    'field': {
                        'cords': (1328, 558),
                        'vars': tuple(range(0, 121, 15)),
                        'step': 15,
                    },
                },
                'voting_time': {
                    'minus': (1291, 654),
                    'plus': (1550, 655),
                    'field': {
                        'cords': (1329, 640),
                        'vars': tuple(range(0, 301, 15)),
                        'step': 15,
                    },
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
                    'minus': (1292, 517),
                    'plus': (1550, 515),
                    'field': {
                        'cords': (1329, 489),
                        'vars': ('Постоянно', 'На собрании', 'Никогда'),
                        'step': 'string',
                    },
                },
                'common_tasks': {
                    'minus': (1289, 666),
                    'plus': (1551, 666),
                    'field': {
                        'cords': (1329, 614),
                        'vars': (0, 1, 2),
                        'step': 1,
                    },
                },
                'long_tasks': {
                    'minus': (1291, 721),
                    'plus': (1551, 721),
                    'field': {
                        'cords': (1331, 696),
                        'vars': (0, 1, 2, 3),
                        'step': 1,
                    },
                },
                'short_tasks': {
                    'minus': (1292, 804),
                    'plus': (1551, 803),
                    'field': {
                        'cords': (1330, 776),
                        'vars': tuple(range(0, 301, 15)),
                        'step': 15,
                    },
                },
            },
            'checkboxes': {
                'visual_tasks': (1273, 859),
            },
        },

    },

    'roles_settings': {
        'cords': (405, 894),
        'all': {
            'cords': (743, 286),
            'crewmates_roles': {
                'cords': (1804, 437),
                'engineers': {
                    'quantity':  {
                        'minus': (1135, 611),
                        'plus': (1327, 610),
                        'field': {
                            'cords': (1173, 581),
                            'vars': tuple(range(16)),
                            'step': 1,
                        },
                    },
                    'chance': {
                        'minus': (1490, 609),
                        'plus': (1681, 608),
                        'field': {
                            'cords': (1528, 579),
                            'vars': tuple(range(0, 101, 10)),
                            'step': 10,
                        },
                    },
                },
                'guardian_angels': {
                    'quantity':  {
                        'minus': (1139, 686),
                        'plus': (1329, 685),
                        'field': {
                            'cords': (1173, 657),
                            'vars': tuple(range(16)),
                            'step': 1,
                        },
                    },
                    'chance': {
                        'minus': (1489, 686),
                        'plus': (1682, 685),
                        'field': {
                            'cords': (1528, 656),
                            'vars': tuple(range(0, 101, 10)),
                            'step': 10,
                        },
                    },
                },
                'scientists': {
                    'quantity':  {
                        'minus': (1136, 765),
                        'plus': (1326, 764),
                        'field': {
                            'cords': (1171, 736),
                            'vars': tuple(range(16)),
                            'step': 1,
                        },
                    },
                    'chance': {
                        'minus': (1490, 764),
                        'plus': (1681, 763),
                        'field': {
                            'cords': (1528, 735),
                            'vars': tuple(range(0, 101, 10)),
                            'step': 10,
                        },
                    },
                },
                'trackers': {
                    'quantity':  {
                        'minus': (1136, 844),
                        'plus': (1327, 841),
                        'field': {
                            'cords': (1173, 815),
                            'vars': tuple(range(16)),
                            'step': 1,
                        },
                    },
                    'chance': {
                        'minus': (1488, 841),
                        'plus': (1682, 839),
                        'field': {
                            'cords': (1528, 812),
                            'vars': tuple(range(0, 101, 10)),
                            'step': 10,
                        },
                    },
                },
                'noisemakers': {
                    'quantity':  {
                        'minus': (1136, 918),
                        'plus': (1328, 919),
                        'field': {
                            'cords': (1173, 890),
                            'vars': tuple(range(16)),
                            'step': 1,
                        },
                    },
                    'chance': {
                        'minus': (1489, 918),
                        'plus': (1680, 917),
                        'field': {
                            'cords': (1528, 889),
                            'vars': tuple(range(0, 101, 10)),
                            'step': 10,
                        },
                    },
                },
            },
            'impostors_roles': {
                'cords': (1802, 951),
                'shapeshifters': {
                    'quantity':  {
                        'minus': (1134, 821),
                        'plus':  (1328, 820),
                        'field': {
                            'cords': (1172, 792),
                            'vars': tuple(range(16)),
                            'step': 1,
                        },
                    },
                    'chance': {
                        'minus': (1488, 820),
                        'plus': (1681, 819),
                        'field': {
                            'cords': (1528, 790),
                            'vars': tuple(range(0, 101, 10)),
                            'step': 10,
                        },
                    },
                },
                'phantoms': {
                    'quantity':  {
                        'minus': (1136, 899),
                        'plus':  (1327, 897),
                        'field': {
                            'cords': (1173, 869),
                            'vars': tuple(range(16)),
                            'step': 1,
                        },
                    },
                    'chance': {
                        'minus': (1490, 898),
                        'plus': (1682, 897),
                        'field': {
                            'cords': (1528, 868),
                            'vars': tuple(range(0, 101, 10)),
                            'step': 10,
                        },
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
                    'field': {
                        'cords': (1489, 713),
                        'vars': tuple(range(5, 61, 5)),
                        'step': 5,
                    },
                },
                'max_time_in_vent': {
                    'minus': (1452, 820),
                    'plus': (1711, 819),
                    'field': {
                        'cords': (1489, 795),
                        'vars': tuple('inf')+tuple(range(5, 61, 5)),
                        'step': 'inf5',
                    },
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
                    'field': {
                        'cords': (1489, 713),
                        'vars': tuple(range(35, 121, 15)),
                        'step': 15,
                    },
                },
                'protect_duration': {
                    'minus': (1452, 819),
                    'plus': (1711, 819),
                    'field': {
                        'cords': (1490, 794),
                        'vars': tuple(range(5, 31, 5)),
                        'step': 5,
                    },
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
                    'field': {
                        'cords': (1490, 713),
                        'vars': tuple(range(5, 61, 5)),
                        'step': 5,
                    },
                },
                'battery_duration': {
                    'minus': (1450, 819),
                    'plus': (1711, 818),
                    'field': {
                        'cords': (1490, 793),
                        'vars': tuple(range(5, 31, 5)),
                        'step': 5,
                    },
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
                    'field': {
                        'cords': (1489, 711),
                        'vars': tuple(range(10, 121, 5)),
                        'step': 5,
                    },
                },
                'tracking_delay': {
                    'minus': (1451, 819),
                    'plus': (1710, 817),
                    'field': {
                        'cords': (1489, 793),
                        'vars': tuple(range(5, 31, 5)),
                        'step': 5,
                    },
                },
                'tracking_duration': {
                    'minus': (1453, 900),
                    'plus': (1712, 899),
                    'field': {
                        'cords': (1490, 874),
                        'vars': tuple(range(10, 121, 5)),
                        'step': 5,
                    },
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
                    'field': {
                        'cords': (1490, 793),
                        'vars': tuple(range(1, 16)),
                        'step': 1,
                    },
                },
            },
        },
        'shapeshifter': {
            'cords': (1564, 286),
            'checkboxes': {
                'leave_shapeshifter_evidence': (1433, 712),
            },
            'fields': {
                'shapeshift_duration': {
                    'minus': (1452, 820),
                    'plus': (1711, 820),
                    'field': {
                        'cords': (1489, 793),
                        'vars': tuple('inf')+tuple(range(5, 31, 5)),
                        'step': 'inf5',
                    },
                },
                'shapeshift_cooldown': {
                    'minus': (1452, 903),
                    'plus': (1712, 901),
                    'field': {
                        'cords': (1488, 873),
                        'vars': tuple(range(5, 91, 5)),
                        'step': 'inf5',
                    },
                },
            },
        },
        'phantom': {
            'cords': (1701, 283),
            'fields': {
                'vanish_duration': {
                    'minus': (1453, 738),
                    'plus': (1711, 738),
                    'field': {
                        'cords': (1490, 713),
                        'vars': tuple(range(10, 91, 10)),
                        'step': 10,
                    },
                },
                'vanish_cooldown': {
                    'minus': (1450, 819),
                    'plus': (1711, 820),
                    'field': {
                        'cords': (1490, 794),
                        'vars': tuple(range(5, 61, 5)),
                        'step': 5,
                    },
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
role_no_all_cords = cast(dict[str, SectionDict], {
    k: val
    for k, val in v['roles_settings'].items()
    if k != 'all' and k != 'cords'
})
current_settings_section = v['settings']['impostors']['cords']
clicks: list[tuple[int, int]] = []
counter = 0
TEAL = (44, 243, 198)
TOLERANCE = 30
CHECKBOX_SHAPE = (60, 60)
current_setting = 'standart_settings'
Settings = Literal['settings', 'roles_settings']
FieldInfo = tuple[Settings, str, FieldDict, Literal['f', 'a']]
CheckboxInfo = tuple[Settings, str, Cords, Literal['c']]


def check(*check_to: str) -> str:
  """Universal dialog field.

    Args:
      check_to (list[tuple[str, str]]): List of options in format (display_text, value).

    Returns:
      str: Final (correct) entry of a user

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
  check_what = input('\n'.join(again)+'\n> ')
  while True:
    if check_what in map(str, range(1, len(check_to)+1)):
      break
    else:
      print('Invalid input')
      check_what = input('\n'.join(again)+'\n> ')
  return check_what


def find_info_by_name(name: str) -> Union[
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
        - Prefix with 'v.' or '.' (automatically stripped)

    Returns:
      out         
      One of many possible return types depending on what's found:
      - Cords (tuple[int, int]): When coordinates are found
      - int/float/str: When a step value found
      - list[str]: When returning available keys for a dictionary level
      - None: When the path doesn't resolve to anything or no checkboxes in section
      - Special tuples for structured settings (see below)


      Structured return tuples:
      - (setting, section_name, field_data, 'f'|'a'): For fields
      - (setting, section_name, cords_data, 'c'): For checkboxes

    Examples:
        >>> # Get coordinates directly
        >>> find_info_by_name('edit')
        (1584, 751)

        >>> # Get field information
        >>> find_info_by_name('settings.impostors.fields.kill_cooldown')
        ('setting', 'impostors', {...}, 'f')

        >>> # Recursive search by field name
        >>> find_info_by_name('kill_cooldown')
        ('setting', 'impostors', {...}, 'f')

        >>> # Get available settings sections
        >>> find_info_by_name('settings')
        ['impostors', 'crewmates', 'meetings', 'tasks']
    """
  if name.startswith('v.'):
    name = name[2:]
  elif name.startswith('.'):
    name = name[1:]
  if name == '' or name == 'v':
    return list(cast(list[str], v.keys()))
  current: Any = v
  parts = name.split('.')
  all_no_cords = cast(dict[str, CrewmatesRolesDict | ImpostorsRolesDict], {
      k: val
      for k, val in v['roles_settings']['all'].items()
      if k != 'cords'
  })
  try:
    if len(parts) == 4 and parts[0] == 'settings' and parts[1] in settings_sections and parts[2] == 'fields' and parts[3] in settings_sections[parts[1]]['fields']:
      section = parts[1]
      field = settings_sections[section]['fields'][parts[3]]
      return 'setting', section, field, 'f'
  except:
    pass
  try:
    if len(parts) == 4 and parts[0] == 'settings' and parts[1] in settings_sections and parts[2] == 'checkboxes' and parts[3] in cast(dict[str, Cords], settings_sections[parts[1]]['checkboxes']):
      section = parts[1]
      checkbox = cast(dict[str, Cords], settings_sections[section]['checkboxes'])[
          parts[3]]
      return 'setting', section, checkbox, 'c'
  except:
    pass
  try:
    if len(parts) == 5 and parts[0] == 'roles_settings' and parts[1] == 'all' and parts[2] in all_no_cords and parts[3] in {
        k: val
        for k, val in all_no_cords[parts[2]].items()
        if k != 'cords'
    } and parts[4] in ('quantity', 'chance'):
      team = parts[2]
      role = parts[3]
      cont = parts[4]
      field = cast(FieldDict, all_no_cords[team][role][cont])
      return 'roles_settings', team, field, 'a'
  except:
    pass
  try:
    if len(parts) == 4 and parts[0] == 'roles_settings' and parts[1] in role_no_all_cords and parts[2] in 'fields' and parts[3] in role_no_all_cords[parts[1]]['fields']:
      role = parts[1]
      return 'roles_settings', role, role_no_all_cords[role]['fields'][parts[3]], 'f'
  except:
    pass
  try:
    if len(parts) == 4 and parts[0] == 'roles_settings' and parts[1] in role_no_all_cords and parts[2] in 'checkboxes' and parts[3] in cast(dict[str, Cords], role_no_all_cords[parts[1]]['checkboxes']):
      role = parts[1]
      return 'roles_settings', role,  cast(dict[str, Cords], role_no_all_cords[parts[1]]['checkboxes'])[parts[3]], 'c'
  except:
    pass

  for part in parts:
    if isinstance(current, dict) and part in current:
      current = cast(Any, current[part])
    else:
      if current is v:
        if part in settings_sections:
          return find_info_by_name(f'settings.{name}')

        for section in settings_sections:
          if part in v['settings'][section]['fields']:
            return find_info_by_name(f'settings.{section}.fields.{name}')
          if v['settings'][section]['checkboxes'] is not None and part in v['settings'][section]['checkboxes']:
            return find_info_by_name(f'settings.{section}.checkboxes.{name}')

        if part in v['roles_settings']:
          return find_info_by_name(f'roles_settings.{name}')

        if part in all_no_cords:
          return find_info_by_name(f'roles_settings.all.{name}')

        crew_roles_no_cords = cast(dict[str, QuantityAndChance], {
            k: val
            for k, val in v['roles_settings']['all']['crewmates_roles'].items()
            if k != 'cords'
        })
        if part in crew_roles_no_cords:
          return find_info_by_name(f'roles_settings.all.crewmates_roles.{name}')

        imp_roles_no_cords = cast(dict[str, QuantityAndChance], {
            k: val
            for k, val in v['roles_settings']['all']['impostors_roles'].items()
            if k != 'cords'
        })
        if part in imp_roles_no_cords:
          return find_info_by_name(f'roles_settings.all.impostors_roles.{name}')

        for section in role_no_all_cords:
          if part in v['roles_settings'][section]['fields']:
            return find_info_by_name(f'roles_settings.{section}.fields.{name}')
          if v['roles_settings'][section]['checkboxes'] is not None and part in v['roles_settings'][section]['checkboxes']:
            return find_info_by_name(f'roles_settings.{section}.checkboxes.{name}')

      return None
  if isinstance(current, dict):
    return list(cast(dict[str, Any], current.keys()))
  return current


def goto(section: str):
  """Universal function for travelling through sections

  Args:
    section (str): Can be name of a setting, section from `settings`, section from `roles_settings`, team from `roles_settings.all`
  """
  global current_settings_section
  if section == 'edit':
    mouse.position = v['edit']
    mouse.click(pn.mouse.Button.left)
    print('Went to edit')
  if section == 'settings':
    set_setting('settings')
  if section == 'roles_settings':
    set_setting('roles_settings')
  if section in settings_sections:
    set_setting('settings')
    cords = settings_sections[section]['cords']
    if scroll(current_settings_section, cords):
      current_settings_section = cords
  if section == 'crewmates_roles' or section == 'all':
    set_setting('roles_settings')
  if section == 'impostors_roles':
    set_setting('roles_settings')
    scroll(v['roles_settings']['all']['crewmates_roles']['cords'],
           v['roles_settings']['all']['impostors_roles']['cords'])
  if section in role_no_all_cords:
    set_setting('roles_settings')
    mouse.position = role_no_all_cords[section]['cords']
    mouse.click(pn.mouse.Button.left)
    print('Section:', section)
  slp(0.3)


def set_setting(name: str):
  """Sets new setting and changes global variable `current_setting`"""
  global current_setting
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
  slp(0.3)


def calculate_clicks(info: FieldInfo | CheckboxInfo,
                     make: Any,
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
    else:
      new = make
    if new != inner:
      mouse.position = info[-2]
      mouse.click(pn.mouse.Button.left)
      print(f'Checkbox: was: {inner}, became: {make}')
  elif inner is None and info[-1] in ('f', 'a') and not isinstance(make, bool):
    info = cast(FieldInfo, info)
    if isinstance(info[-2]['field']['step'], (int, float)):
      make = make.replace(',', '.')
      if make.isdigit():
        new_val = int(make)
      else:
        print(f'Making value {make} is NaN')
        return
      mid = info[-2]['field']['vars'][len(info[-2]['field']['vars'])//2]
      if new_val < mid:
        mouse.position = info[-2]['minus']
        prev_val = info[-2]['field']['vars'][0]
        for _ in range(len(info[-2]['field']['vars'])-1):
          mouse.click(pn.mouse.Button.left)
          slp(0.035)
        offset = (new_val-prev_val)//info[-2]['field']['step']
        mouse.position = info[-2]['plus']
        for _ in range(offset):
          mouse.click(pn.mouse.Button.left)
          slp(0.035)
      else:
        mouse.position = info[-2]['plus']
        prev_val = info[-2]['field']['vars'][-1]
        for _ in range(len(info[-2]['field']['vars'])-1):
          mouse.click(pn.mouse.Button.left)
          slp(0.035)
        offset = (prev_val-new_val)//info[-2]['field']['step']
        mouse.position = info[-2]['minus']
        for _ in range(offset):
          mouse.click(pn.mouse.Button.left)
          slp(0.035)


def set_options(*options: tuple[Any, ...]):
  """Universal function for setting needed values to options

  Args:
    mode (Literal['ocr','bordering']): option setting mode
    options (tuple[tuple[str,str], ...]): In each inner tuple 1st value describes option e.g.->kill_distance, 2nd describes value that must be set
  """
  for option in options:
    info = find_info_by_name(option[0])
    if info is not None and isinstance(info, tuple):
      if info[-1] == 'c':
        info = cast(CheckboxInfo, info)
        goto(info[1])
        calculate_clicks(info, option[1], checkbox(info[-2]))
      elif info[-1] in ('f', 'a'):
        info = cast(FieldInfo, info)
        goto(info[1])
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
    for team in ('crewmates_roles', 'impostors_roles'):
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
      return True
    elif not was_name or not will_name:
      print(f'Section cannot be found')
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


def iw4_actions(x: int, y: int, button: pn.mouse.Button, pressed: bool):
  if button == pn.mouse.Button.middle and pressed:
    goto('edit')
    set_options(
        ('settings.impostors.fields.#_impostors', 3),
        ('settings.impostors.fields.kill_cooldown', 25),
        ('settings.impostors.fields.impostor_vision', 1.75),
        ('settings.impostors.fields.kill_distance', 'Medium'),
        ('settings.crewmates.fields.player_speed', 1.5),
        ('settings.crewmates.fields.crewmate_vision', 1),
        ('settings.meetings.fields.#_emergency_meetings', 1),
        ('settings.meetings.fields.emergency_cooldown', 20),
        ('settings.meetings.fields.disscusion_time', 30),
        ('settings.meetings.fields.voting_time', 30),
        ('settings.meetings.checkboxes.anonymous_votes', True),
        ('settings.meetings.checkboxes.confirm_ejects', True),
        ('settings.tasks.fields.#_task_bar_updates', 'Always'),
        
        ('settings.tasks.checkboxes.visual_tasks', True),
    )


def iw4_settings():
  with pn.mouse.Listener(on_click=iw4_actions) as listener:
    listener.join()


mouse = pn.mouse.Controller()
choice = check("Iaw4tch's settings", 'Load from file', 'Create new')
match choice:
  case '1':
    print('Press middle button to start applying settings')
    iw4_settings()  # type: ignore
  case '2':
    ...
  case '3':
    ...
  case _:
    pass
