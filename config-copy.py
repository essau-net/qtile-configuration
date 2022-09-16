import os
import subprocess
from libqtile import hook

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger

mod = "mod4"
terminal = guess_terminal()
current_keyboard:str = 'us'

background_color = "#1B1E32"
foreground_color = "#f8f8f2"
size_bar = 30
font_default = "Sauce Code Nerd Font"
font_size = 14
icon_size = 27
active_color = "#68aff2"
inactive_color = "#224D73"
border_var = 1
background_icons = "#101329"
background_separator = "#07091A"
marginx = 0
marginy = 5
color_temperature = "#ff7f00"
color_memory = ""

def separator():
    return widget.Sep(
        linewidth=0,
        padding=16,
        background=background_separator,
    )

def rectangle_side(color, side):
    if side == 'left':
        icon = "" # nf-ple-left_half_circle_thick
    else:
        icon = "" #nf-ple-right_half_circle_thick
    return widget.TextBox(
        text=icon,
        fontsize=size_bar+2,
        foreground=color,
        background=background_color,
        padding = 0,
    )

def rectangle_icon(color_group, icon):
    return widget.TextBox(
        text=icon,
        fontsize=icon_size,
        foreground=foreground_color,
        background=color_group,
    )

@lazy.function
def change_keyboard(qtile):
    global current_keyboard
    logger.info("Si corre la funcion")
    if (current_keyboard == 'us'):
        current_keyboard = 'latam'
    elif (current_keyboard == 'latam'):
        current_keyboard = 'us'
    subprocess.run(["setxkbmap", current_keyboard])

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    #Key([mod]
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    # keys to run rofi menu
    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="Open menu"),
    # keys to change keyboard
    Key([mod, "control"], "space", change_keyboard, desc="Change keyboard layout"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

#List nerd fonts icons
# 1- nf-linux-archlinux
# 2- nf-mdi-firefox
# 3- nf-dev-visualstudio
# 4- nf-custom-folder_open
# 5- nf-mdi-spotify
# 6- nf-mdi-message_settings

groups = [Group(i) for i in [
    "  ",
    "  ",
    "  ",
    "  ",
    " 阮 ",
    " ﯮ "
]]


for i, group in enumerate(groups):
    current_desktop = str(i+1)
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                current_desktop,
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                current_desktop,
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font=font_default,
    fontsize=font_size,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active=active_color,
                    inactive=inactive_color,
                    border_width=border_var,
                    fontsize=icon_size,
                    highlight_method='line',
                    foreground = '#5B3B88',
                    background = background_icons,
                    margin_x=marginx,
                    margin_y=marginy,
                ),
                separator(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Systray(
                    icon_size=icon_size,
                    background=background_color
                ),
                separator(),
                rectangle_side(color_temperature, "left"),
                rectangle_icon(color_temperature, "  "),
                widget.ThermalSensor(
                    foreground=foreground_color,
                    background=color_temperature,
                    treshold=70,
                    tag_sensor="Core 0",
                    fmt = "C0: {}"
                ),
                widget.ThermalSensor(
                    foreground=foreground_color,
                    background=color_temperature,
                    treshold=70,
                    tag_sensor="Core 1",
                    fmt = "C1: {}"
                ),
                rectangle_side(color_temperature, "right"),
                rectangle_side(color_temperature, "left"),
                rectangle_icon(color_temperature, ""),
                widget.Memory(
                    foreground=foreground_color,
                    background=color_temperature,
                ),
                rectangle_side(color_temperature, "right"),
                widget.Clock(format="%Y-%m-%d %a %H:%M %S"),
            ],
            size_bar,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background=background_color
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
        home = os.path.expanduser('~')
        subprocess.Popen([home + '/.config/qtile/autostart.sh'])
