from typing import TypedDict, Literal, Any, cast, Callable
import numpy as np

class Handlers(TypedDict):
  args: dict[str|tuple[str, ...], Callable[[list[str]], None]]
  noargs: dict[str|tuple[str, ...], Callable[[],None]]
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

FieldInfo = tuple[str, str, FieldDict, Literal['f']]
CheckboxInfo = tuple[str, str, Cords, Literal['c']]

command_info = '''Commands:
-------------------------------------------------------------------
set {option name} {option value}
view -> toggle code view (v)
remove {index} -> removes entered lines by index (-indexes supported) (rm)
. -> top level dict
save -> saves script (.json) (s)
load -> loads script from file (.json) (l)
run -> middle button to start setting (r)
stop -> stops script running (st)
exit -> leaves the program (e)'''
