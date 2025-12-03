# Among Us Lobby Settings Setter (OUT OF DATE)

Lobby settings setter for game Among Us.
Allows you to quickly set needed lobby options via console or UI interface.

## Features
- Settings setting through console or UI.
- Saving and Loading settings script into `.json`.
- Automatic application of settings in the game.
- All settings supported.

## Installation
Download and run `.exe` file from [*Releases*](https://github.com/Iaw4tch/among-us-settings-setter/releases) tab.

## Usage
### Commands:
- `help` - Display information about shell commands.
- `<parameter>` `<value>` - Set parameter to value.
- `remove`/`rm` `<index>` - Remove line from script by index $( index \in \mathbb{Z}, \quad index \neq 0 )$.
- `insert`/`ins` `<index>` `<parameter>` `<value>` - Insert a parameter into the index value, moves the parameters after the index forward.
- `replace`/`r` `<index>` `<parameter>` `<value>` - Replace existing line with another.
- `save`/`s`  - Save script info a file (GUI).
- `load`/`l`  - Load script from a file (GUI).
- `run` `<start_key>` `<stop_key>`   - Program launch (Middle mouse button to start applying).
- `stop`  - Stop program execution.
- `edit`    - Toggle flag "*First edit*". If True middle button pressing will enter *Edit* tab first in game.
- `.`  - View top level dict
- `<Enter>` - Display written script
- `buttons` - Display available mouse and keyboard buttons
- `exit`/`e`     - Leave program


### Dictionary info:
Program works with massive dictionary called *v*, you can see it's keys typing "**.**" in the shell.

```
{edit,
settings,
roles_settings}
```

With "**.**" separator you can delve into *v* dictionary.\
For instance:
```
.edit -> (1584, 751)
settings -> {cords: (425, 776),
impostors,
crewmates,
meetings,
tasks}

roles_settings -> {cords: (405, 894),
all,
engineer,
guardian_angel,
scientist,
tracker,
noisemaker,
shapeshifter,
phantom}

engineer -> {cords: (884, 286),
fields,
checkboxes: None}

engineer.#.vars -> (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)

engineer.fields -> {vent_use_cooldown,
max_time_in_vents}
```

Repeating names like `vars`, `fields`, `step`, etc. wont be found.

### Usage examples
#### Entering shell:
```
1 -> Iaw4tch's settings
2 -> Enter shell
> 2
Script is empty, fisrt edit enter -> False
Type 'help' if you use shell for the first time
1:
```


#### Adding options setting:
```set kill_cooldown 25
1: player_speed 1.5
2: anonymous_votes true
3:
```

#### Viewing and editing the script:
```
<Enter>
First edit enter -> False
1: kill_cooldown > 25
2: player_speed > 1.5
3: anonymous_votes > true
4: rm 2
```
```
First edit enter -> False
1: kill_cooldown > 25
2: anonymous_votes > true
3:
```
---
```
<Enter>
First edit enter -> False
1: kill_cooldown > 25
2: anonymous_votes > true
3: r -1 anonymous_votes false
```
```
First edit enter -> False
1: kill_cooldown > 25
2: anonymous_votes > false
3:
```
