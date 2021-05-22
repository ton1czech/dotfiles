# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from os import environ
from dotenv import load_dotenv
from libqtile import qtile
from libqtile.config import Drag, Key, Screen, Group, Drag, Click, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.widget import Spacer

load_dotenv()

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')
term = "alacritty"


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [
# SUPER + FUNCTION KEYS
    Key([mod], "F1", lazy.spawn("firefox")),
    Key([mod], "F2", lazy.spawn("qutebrowser")),
    Key([mod], "F3", lazy.spawn("google-chrome-stable")),
    Key([mod], "F4", lazy.spawn("spotify")),
    Key([mod], "F5", lazy.spawn("code")),
    Key([mod], "F6", lazy.spawn("discord")),

# SUPER + ... KEYS
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "x", lazy.spawn("arcolinux-logout")),
    Key([mod], "BackSpace", lazy.spawn(term+" -e fish")),
    Key([mod], "Return", lazy.spawn(term)),

# SUPER + SHIFT KEYS
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "w", lazy.spawn('nitrogen')),
    Key([mod, "shift"], "Return", lazy.spawn("dmenu_run -p 'Run: '")),

# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, mod2], "h", lazy.layout.shrink(), lazy.layout.decrease_nmaster()),
    Key([mod, mod2], "l", lazy.layout.grow(), lazy.layout.increase_nmaster()),

# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod], "c", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    ]

# GROUPS
group_names = [("", {'layout': 'monadtall'}),
                ("{ }", {'layout': 'monadtall'}),
                ("", {'layout': 'monadtall'}),
                ("🎶", {'layout': 'monadtall'}),
                ("✈", {'layout': 'monadtall'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

def init_layout_theme():
    return {"margin":8,
            "border_width":2,
            "border_focus": "#FF79C6",
            "border_normal": "#6272A4"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Max(**layout_theme),
]



# COLORS FOR THE BAR
def init_colors():
    return [["#282A36", "#282A36"], # 0   # BACKGROUND
            ["#FF79C6", "#FF79C6"], # 1   # PINK
            ["#BD93F9", "#BD93F9"], # 2   # PURPLE
            ["#6272A4", "#6272A4"], # 3   # COMMENT
            ["#FFB86C", "#FFB86C"], # 4   # ORANGE
            ["#50FA7B", "#50FA7B"]] # 5   # GREEN 

colors = init_colors()



# WIDGETS FOR THE BAR
def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize = 12,
                padding = 2,
                background=colors[0])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
                widget.CurrentLayoutIcon(
                        custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                        scale = 0.65,
                        ),
                widget.Sep(
                        linewidth = 2,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.GroupBox(
                        font="FontAwesome",
                        fontsize = 16,
                        margin_y = 2.5,
                        margin_x = 0,
                        padding_y = 6,
                        padding_x = 5,
                        borderwidth = 0,
                        active = colors[3],
                        inactive = colors[3],
                        rounded = False,
                        highlight_method = "text",
                        this_current_screen_border = colors[1],
                        foreground = colors[1],
                        background = colors[0]
                        ),
                widget.Spacer(),
                widget.Clock(
                        font="Ubuntu Bold",
                        foreground=colors[5],
                        background=colors[0],
                        fontsize=14,
                        format='%H:%M:%S'
                        ),
                widget.Spacer(),
                widget.Sep(
                        linewidth = 2,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.TextBox(
                        font="FontAwesome",
                        text = "☂",
                        padding = 3,
                        foreground = colors[1],
                        background = colors[0],
                        fontsize = 16
                        ),
                widget.OpenWeather(
                        app_key = environ['APP_KEY'],
                        cityid = environ['CITY_ID'],
                        foreground = colors[1],
                        background = colors[0],
                        format = "{main_temp}°{units_temperature}"
                        ),
                widget.Sep(
                        linewidth = 2,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.TextBox(
                        font="Ubuntu Bold",
                        text = "↑",
                        foreground = colors[1],
                        background = colors[0],
                        padding = 0,
                        fontsize = 16
                        ),
                widget.CPU(
                        font="Ubuntu",
                        foreground = colors[1],
                        background = colors[0],
                        format="{freq_current}GHz | {load_percent}%"
                        ),
                widget.Sep(
                        linewidth = 2,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.TextBox(
                        font="Ubuntu Bold",
                        text = " 🖬",
                        foreground = colors[1],
                        background = colors[0],
                        padding = 0,
                        fontsize = 16
                        ),
                widget.Memory(
                        font="Ubuntu",
                        foreground = colors[1],
                        background = colors[0],
                        padding = 5
                        ),
                widget.Sep(
                        linewidth = 2,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.TextBox(
                        font="Ubuntu Bold",
                        text = "🌡",
                        padding = 2,
                        foreground = colors[1],
                        background = colors[0],
                        fontsize = 12
                        ),
                widget.ThermalSensor(
                        font="Ubuntu",
                        foreground = colors[1],
                        background = colors[0],
                        threshold = 90,
                        padding = 5,
                        ),
                widget.Sep(
                        linewidth = 2,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.TextBox(
                        font="Ubuntu Bold",
                        text="🔊",
                        foreground = colors[1],
                        background = colors[0],
                        padding = 4,
                        fontsize=16
                        ),
                widget.Volume(
                        foreground = colors[1],
                        background = colors[0],
                        ),
                widget.Sep(
                        linewidth = 2,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.TextBox(
                        font="Ubuntu Bold",
                        text="",
                        foreground=colors[1],
                        background=colors[0],
                        padding = 5,
                        fontsize=16
                        ),
                widget.Clock(
                        font="Ubuntu",
                        foreground = colors[1],
                        background = colors[0],
                        fontsize = 12,
                        format="%d-%m"
                        ),
                ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, border_radius=40, opacity=0.95, margin=[4,8,0,8])),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, border_radius=40, opacity=0.95, margin=[4,8,0,8]))]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'Arcolinux-welcome-app.py'},
    {'wmclass': 'Arcolinux-tweak-tool.py'},
    {'wmclass': 'Arcolinux-calamares-tool.py'},
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},
    {'wmclass': 'makebranch'},
    {'wmclass': 'maketag'},
    {'wmclass': 'Arandr'},
    {'wmclass': 'feh'},
    {'wmclass': 'Galculator'},
    {'wmclass': 'arcolinux-logout'},
    {'wmclass': 'xfce4-terminal'},
    {'wname': 'branchdialog'},
    {'wname': 'Open File'},
    {'wname': 'pinentry'},
    {'wmclass': 'ssh-askpass'},
],  

fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"
