from typing import TypedDict, Literal, Any, cast, Callable, Hashable
import numpy as np
from screeninfo import get_monitors

ratio = get_monitors()[0].width / 1080/get_monitors()[0].height
width_d = 1920/get_monitors()[0].width
height_d = 1080/get_monitors()[0].height


def recount_pixels(x: int, y: int) -> tuple[int, int]:
  m = min(width_d, height_d)
  return (round(x/m), round(y/m))


def recursive_change(data: Any) -> Any:
  if isinstance(data, dict):
    data = cast(dict[Hashable, Any], data)
    return {k: recursive_change(v) for k, v in data.items()}
  elif isinstance(data, tuple):
    data = cast(tuple[Any, ...], data)
    if len(data) == 2 and isinstance(data[0], int) and isinstance(data[1], int):
      return recount_pixels(data[0], data[1])
  return data


class Handlers(TypedDict):
  args: dict[str | tuple[str, ...], Callable[[list[str]], None]]
  noargs: dict[str | tuple[str, ...], Callable[[], None]]


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


class DataDict(TypedDict):
  flag: bool
  lines: list[tuple[str, str]]


class ScriptDict(TypedDict):
  data: DataDict
  repr: list[str]


FieldInfo = tuple[str, str, FieldDict, Literal['f']]
CheckboxInfo = tuple[str, str, Cords, Literal['c']]

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
                '#common': {
                    'minus': (1291, 612),
                    'plus': (1551, 610),
                    'vars': (0, 1, 2),
                    'step': 1,
                },
                '#long': {
                    'minus': (1292, 694),
                    'plus': (1549, 689),
                    'vars': (0, 1, 2, 3),
                    'step': 1,
                },
                '#short': {
                    'minus': (1291, 774),
                    'plus': (1552, 772),
                    'vars': (0, 1, 2, 3, 4, 5),
                    'step': 1,
                },
            },
            'checkboxes': {
                'visual_tasks': (1275, 831),
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

v = recursive_change(v)

SETTINGS_SECTIONS = cast(dict[str, SectionDict], {
    k: val
    for k, val in v['settings'].items()
    if k != 'cords'
})
ROLES_SETTINGS_ROLES = cast(dict[str, SectionDict], {
    k: val
    for k, val in v['roles_settings'].items()
    if k != 'all' and k != 'cords'
})
ROLES_SETTINGS_ROLES_ALL = cast(dict[str, ScrollForAllDict | SectionDict], {
    k: val
    for k, val in v['roles_settings'].items()
    if k != 'cords'
})
ALL_TEAMS = cast(dict[str, CrewmateRolesDict | ImpostorRolesDict], {
    k: val
    for k, val in v['roles_settings']['all'].items()
    if k != 'cords'
})
TEAMS_CREWMATE_ROLES = cast(dict[str, QuantityAndChance], {
    k: val
    for k, val in v['roles_settings']['all']['crewmate_roles'].items()
    if k != 'cords'
})
TEAMS_IMPOSTOR_ROLES = cast(dict[str, QuantityAndChance], {
    k: val
    for k, val in v['roles_settings']['all']['impostor_roles'].items()
    if k != 'cords'
})

PARAMETERS_NAMES: list[str] = [
    '#impostors',
    'kill_cooldown',
    'kill_distance',
    'impostor_vision',
    'player_speed',
    'crewmate_vision',
    '#emergency_meetings',
    'emergency_cooldown',
    'discussion_time',
    'voting_time',
    'anonymous_votes',
    'confirm_ejects',
    '#common',
    '#long',
    '#short',
    'task_bar_updates',
    'visual_tasks',
    'engineer.#',
    'engineer.%',
    'guardian_angel.#',
    'guardian_angel.%',
    'scientist.#',
    'scientist.%',
    'tracker.#',
    'tracker.%',
    'noisemaker.#',
    'noisemaker.%',
    'shapeshifter.#',
    'shapeshifter.%',
    'phantom.#',
    'phantom.%',
    'vent_use_cooldown',
    'max_time_in_vents',
    'protect_cooldown',
    'protect_duration',
    'protect_visible_to_impostors',
    'vitals_display_cooldown',
    'battery_duration',
    'tracking_cooldown',
    'tracking_delay',
    'tracking_duration',
    'impostors_get_alert',
    'alert_duration',
    'leave_shapeshifting_evidence',
    'shapeshift_duration',
    'shapeshift_cooldown',
    'vanish_duration',
    'vanish_cooldown'
]
PARTS: list[str] = ['impostor_vision',
                    'emergency_cooldown',
                    'tasks',
                    'edit',
                    'tracking_delay',
                    'protect_visible_to_impostors',
                    'protect_duration',
                    'vitals_display_cooldown',
                    '#emergency_meetings',
                    'meetings',
                    '#common',
                    'engineer',
                    'discussion_time',
                    'guardian_angel',
                    'task_bar_updates',
                    'plus',
                    'visual_tasks',
                    'phantom',
                    'protect_cooldown',
                    '#impostors',
                    'checkboxes',
                    '#',
                    'kill_distance',
                    'shapeshifter',
                    'player_speed',
                    'battery_duration',
                    'shapeshift_cooldown',
                    'noisemaker',
                    'max_time_in_vents',
                    'kill_cooldown',
                    'confirm_ejects',
                    'anonymous_votes',
                    '#short',
                    'fields',
                    'cords',
                    'all',
                    'scientist',
                    'vent_use_cooldown',
                    'impostors',
                    'voting_time',
                    'leave_shapeshifting_evidence',
                    'shapeshift_duration',
                    'crewmates',
                    'tracker',
                    '%',
                    'crewmate_roles',
                    'roles_settings',
                    'impostor_roles',
                    'alert_duration',
                    'minus',
                    'vanish_cooldown',
                    'tracking_duration',
                    'impostors_get_alert',
                    'settings',
                    'step',
                    '#long',
                    'tracking_cooldown',
                    'crewmate_vision',
                    'vars',
                    'vanish_duration']

FINDABLE_NAMES: list[str] = [
    'settings',
    'impostors',
    '#impostors',
    'kill_cooldown',
    'impostor_vision',
    'kill_distance',
    'crewmates',
    'player_speed',
    'crewmate_vision',
    'meetings',
    '#emergency_meetings',
    'emergency_cooldown',
    'discussion_time',
    'voting_time',
    'tasks',
    'task_bar_updates',
    '#common',
    '#long',
    '#short',
    'roles_settings',
    'all',
    'crewmate_roles',
    'engineer',
    'guardian_angel',
    'scientist',
    'tracker',
    'noisemaker',
    'impostor_roles',
    'shapeshifter',
    'phantom',
    'engineer',
    'vent_use_cooldown',
    'max_time_in_vents',
    'guardian_angel',
    'protect_cooldown',
    'protect_duration',
    'scientist',
    'vitals_display_cooldown',
    'battery_duration',
    'tracker',
    'tracking_cooldown',
    'tracking_delay',
    'tracking_duration',
    'noisemaker',
    'alert_duration',
    'shapeshifter',
    'shapeshift_duration',
    'shapeshift_cooldown',
    'phantom',
    'vanish_duration',
    'vanish_cooldown'
]

command_info = '''Commands:
--------------------------------------------------------------------------------------------------------------------------------------------
- help                                   - Display information about shell commands.
- <parameter> <value>                    - Set parameter to value.
- remove/rm <index>                      - Remove line from script by index (index cannot be 0, -indexes supported).
- insert/ins <index> <parameter> <value> - Insert a parameter into the index value, moves the parameters after the index forward.
- replace/r <index> <parameter <value>   - Replace existing line with an.
- save/s                                 - Save script info a file (GUI).
- load/l                                 - Load script from a file (GUI).
- run <start_key> <stop_key>             - Program launch (Middle mouse button to start applying).
- stop                                   - Stop program execution.
- edit                                   - Toggle flag "First edit". If True first middle button pressing will enter Edit tab first in game.
- .                                      - View top level dict
- <Enter>                                - Display written script
- buttons                                - Display available mouse and keyboard buttons
- exit/e                                 - Leave program'''
iw4s = (
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
BUTTONS = ['alt', 'alt_gr', 'alt_l', 'alt_r', 'backspace', 'caps_lock', 'cmd', 'cmd_r', 'ctrl', 'ctrl_l', 'ctrl_r', 'delete', 'down', 'end', 'enter', 'esc', 'f1', 'f10',
           'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'home', 'insert',
           'left', 'media_next', 'media_play_pause', 'media_previous', 'media_stop', 'media_volume_down', 'media_volume_mute', 'media_volume_up', 'menu', 'num_lock', 'page_down',
           'page_up', 'pause', 'print_screen', 'right', 'scroll_lock', 'shift', 'shift_r', 'space', 'tab', 'up', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+',
           ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
           'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н',
           'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
           'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'Ё', 'ё']
TEAL = (44, 243, 198)  # Cyan checkbox color
TOLERANCE = 30  # Just in case
# Checkbox shape in pixels in 1080p
CHECKBOX_SHAPE = (round(60/width_d), round(60/height_d))
