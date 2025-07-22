# Among Us Lobby Settings Setter

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
### Basic commands:
- `help` - Display information about console commands.
- `view`/`v` - Toggle viewing mode.
- `set` `<parameter>` `<value>` - Set value to option.
- `remove`/`rm` `<index>` - Remove line from script by index (-Indexes supported).
- `insert`/`ins` `<index>` `<parameter>` `<value>` - Inserts a parameter into the index value and moves the parameters after the index forward.
- `save`/`s`  - Save script info a file.
- `load`/`l`  - Load script from a file.
- `run`/`r`   - Program launch (Middle mouse button to start applying).
- `stop`/`st`  - Stop program execution.
- `edit`    - Toggle flag "*First edit*". If True first middle button pressing will enter *Edit* tab first in game.
- `exit`/`e`     - Leave program

### Dictionary info:
Program works with massive dictionary called *v*, you can see it's keys typing "**.**" in the shell.

> ['edit', 'settings', 'roles_settings']

With "**.**" separator you can delve into *v* dictionary.\
For instance:
```
.edit -> (1584, 751)
settings -> ['cords', 'impostors', 'crewmates', 'meetings', 'tasks']
roles_settings -> ['cords', 'all', 'engineer', 'guardian_angel', 'scientist', 'tracker', 'noisemaker', 'shapeshifter', 'phantom']
engineer -> ['cords', 'fields', 'checkboxes']
engineer.#.vars -> (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
engineer.fields -> ['vent_use_cooldown', 'max_time_in_vents']
```

Repeating names like `vars`, `fields`, `step`, etc. will be signed as Unknown commands.

### Usage examples
#### Entering shell:
```1 -> Iaw4tch's settings
2 -> Enter shell
> 2
Type 'help' for help

```


#### Adding options setting:
```set kill_cooldown 25
set player_speed 1.5
set anonymous_votes true
```

#### Viewing and editing the script:
```view
First edit enter -> False
1: set kill_cooldown 25
2: set player_speed 1.5
3: set anonymous_votes true
4: rm 2
```
```
First edit enter -> False
1: set kill_cooldown 25
2: set anonymous_votes true
3: 
```
