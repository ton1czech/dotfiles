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
from libqtile import qtile
from libqtile.config import Drag, Key, Screen, Group, Drag, Click, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.widget import Spacer

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

# Most of our keybindings are in sxhkd file - except these

# SUPER + FUNCTION KEYS
    Key([mod], "F1", lazy.spawn("firefox")),
    Key([mod], "F2", lazy.spawn("qutebrowser")),
    Key([mod], "F3", lazy.spawn("qutebrowser")),
    Key([mod], "F4", lazy.spawn("spotify")),
    Key([mod], "F5", lazy.spawn("code")),
    Key([mod], "F6", lazy.spawn("discord")),

# SUPER + ... KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "BackSpace", lazy.spawn(term+" -e fish")),
    Key([mod], "Return", lazy.spawn(term)),

# SUPER + SHIFT KEYS

    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
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
    Key([mod, "control"], "h",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "l",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),

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


# FOR QWERTY KEYBOARDS
group_names = [("1", {'layout': 'monadtall'}),
           ("2", {'layout': 'monadtall'}),
           ("3", {'layout': 'monadtall'}),
           ("4", {'layout': 'monadtall'}),
           ("5", {'layout': 'monadtall'}),
           ("6", {'layout': 'monadtall'}),
           ("7", {'layout': 'monadtall'}),
           ("8", {'layout': 'monadtall'}),
           ("9", {'layout': 'monadtall'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

def init_layout_theme():
    return {"margin":8,
            "border_width":2,
            "border_focus": "#1cefff",
            "border_normal": "#c0c0aa"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Max(**layout_theme)
]

# COLORS FOR THE BAR

def init_colors():
    return [["#ff00cc", "#333399"], # color 0   # Cosmic Fusion
            ["#100c08", "#100c08"], # color 1   # Smoky Black
            ["#fceabb", "#f8b500"], # color 2   # Sun on the Horizon
            ["#41295a", "#2f0743"], # color 3   # 80s Purple
            ["#1e3c72", "#2a5298"], # color 4   # Joomla
            ["#c0c0aa", "#c0c0aa"], # color 5   # Cocoa
            ["#e1e7e4", "#e1e7e4"], # color 6   # Ice White
            ["#a1ffce", "#faffd1"], # color 7   # Limeade
            ["#141e30", "#243b55"], # color 8   # Royal
            ["#1cefff", "#1cefff"], # color 9   # Ice
            ["#000428", "#004e92"], # color 10  # Frost
            ["#e90079", "#be0062"], # color 11  # Flickr
            ["#8e2de2", "#4a00e0"], # color 12  # Amin
            ["#56ccf2", "#2f80ed"]]  # color 13  # Blue Skies


colors = init_colors()


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize = 12,
                padding = 2,
                background=colors[1])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
               widget.GroupBox(font="Ubuntu Bold",
                        fontsize = 18,
                        margin_y = 2.5,
                        margin_x = 0,
                        padding_y = 6,
                        padding_x = 5,
                        borderwidth = 0,
                        disable_drag = True,
                        active = colors[5],
                        inactive = colors[5],
                        rounded = False,
                        highlight_method = "text",
                        this_current_screen_border = colors[9],
                        foreground = colors[9],
                        background = colors[1]
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[5],
                        background = colors[1]
                        ),
               widget.CurrentLayout(
                        font = "Ubuntu Bold",
                        fontsize = 15,
                        foreground = colors[11],
                        background = colors[1]
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[5],
                        background = colors[1]
                        ),
               widget.WindowName(
                        font="Ubuntu",
                        fontsize = 12,
                        foreground = colors[5],
                        background = colors[1],
                        ),
               widget.TextBox(
                       font="Ubuntu Bold",
                       text = " ₿",
                       padding = 0,
                       foreground = colors[1],
                       background = colors[2],
                       fontsize = 16
                       ),
               widget.BitcoinTicker(
                       font="Ubuntu",
                       foreground = colors[1],
                       background = colors[2],
                       padding = 7
                       ),
               widget.TextBox(
                       font="Ubuntu Bold",
                       text = "☂",
                       padding = 3,
                       foreground = colors[1],
                       background = colors[13],
                       fontsize = 16
                       ),
               widget.OpenWeather(
                       app_key = '95903b10ac9f405b5b7aa02feb8717e5',
                       cityid = 3062351,
                       foreground = colors[1],
                       background = colors[13],
                       format = "{location_city}: {main_temp}°{units_temperature}  {weather_details}"
                       ),
               widget.TextBox(
                       font="Ubuntu Bold",
                       text = "↑",
                       foreground = colors[6],
                       background = colors[8],
                       padding = 0,
                       fontsize = 16
                       ),
               widget.CPU(
                       font="Ubuntu",
                       foreground = colors[6],
                       background = colors[8],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       format="{freq_current}GHz | {load_percent}%"
                       ),
               widget.TextBox(
                       font="Ubuntu Bold",
                       text = " 🖬",
                       foreground = colors[6],
                       background = colors[10],
                       padding = 0,
                       fontsize = 16
                       ),
              widget.Memory(
                       font="Ubuntu",
                       foreground = colors[6],
                       background = colors[10],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       padding = 5
                       ),
               widget.TextBox(
                       font="Ubuntu Bold",
                       text = "🌡",
                       padding = 2,
                       foreground = colors[6],
                       background = colors[4],
                       fontsize = 12
                       ),
               widget.ThermalSensor(
                       font="Ubuntu",
                       foreground = colors[6],
                       background = colors[4],
                       threshold = 90,
                       padding = 5,
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       ),
               widget.TextBox(
                       font="Ubuntu Bold",
                       text = "♻",
                       padding = 2,
                       foreground = colors[6],
                       background = colors[3],
                       fontsize = 16
                       ),
               widget.CheckUpdates(
                       font="Ubuntu",
                       update_interval = 1800,
                       distro = "Arch_checkupdates",
                       display_format = "{updates} Updates",
                       foreground = colors[6],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syyu')},
                       background = colors[3]
                       ),
               widget.TextBox(
                        font="Ubuntu Bold",
                        text="🔊",
                        foreground=colors[6],
                        background=colors[12],
                        padding = 4,
                        fontsize=16
                        ),
               widget.Volume(
                        foreground = colors[6],
                        background = colors[12],
                        ),
               widget.TextBox(
                        font="Ubuntu Bold",
                        text="",
                        foreground=colors[1],
                        background=colors[7],
                        padding = 5,
                        fontsize=16
                        ),
               widget.Clock(
                       font="Ubuntu",
                        foreground = colors[1],
                        background = colors[7],
                        fontsize = 12,
                        format="%Y-%m-%d %H:%M:%S"
                        ),
               #widget.Systray(
               #         background=colors[1],
               #         icon_size=20,
               #         padding = 4
               #         ),
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
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=0.8)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, opacity=0.8))]
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
