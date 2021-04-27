#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export HISTCONTROL=ignoreboth:erasedups

export PS1='\[\e[0;2m\]\u\[\e[0;2m\]@\[\e[0;2m\]\h\[\e[0m\]: \[\e[0;38;5;46m\]<\[\e[0;38;5;46m\]\w\[\e[0;38;5;46m\]> \[\e[0;91m\][\[\e[0;91m\]$(git branch 2>/dev/null | grep '"'"'^*'"'"' | colrm 1 2)\[\e[0;91m\]]\[\e[0;1m\]\$ \[\e[0m\]' 

if [ -d "$HOME/.bin" ] ;
  then PATH="$HOME/.bin:$PATH"
fi

if [ -d "$HOME/.local/bin" ] ;
  then PATH="$HOME/.local/bin:$PATH"
fi

#ignore upper and lowercase when TAB completion
bind "set completion-ignore-case on"

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

#####                    ALIASES                   #####

# Colorize the grep command output for ease of use (good for log files)##
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'

# Use all cores
alias uac="sh ~/.bin/main/000*"

# Continue download
alias wget="wget -c"

#ps
alias psa="ps auxf"
alias psgrep="ps aux | grep -v grep | grep -i -e VSZ -e"

#grub update
alias update-grub="sudo grub-mkconfig -o /boot/grub/grub.cfg"

#add new fonts
alias update-fc='sudo fc-cache -fv'

#switch between bash and zsh
alias tobash="sudo chsh $USER -s /bin/bash && echo 'Now log out.'"
alias tozsh="sudo chsh $USER -s /bin/zsh && echo 'Now log out.'"

#switch between lightdm and sddm
alias tolightdm="sudo pacman -S lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings --noconfirm --needed ; sudo systemctl enable lightdm.service -f ; echo 'Lightm is active - reboot now'"
alias tosddm="sudo pacman -S sddm --noconfirm --needed ; sudo systemctl enable sddm.service -f ; echo 'Sddm is active - reboot now'"

# confirm before overwriting something
alias cp="cp -i"
alias mv="mv -i"
alias rm="rm -i"

#hardware info --short
alias hw="hwinfo --short"

#get fastest mirrors in your neighborhood
alias mirror="sudo reflector -f 30 -l 30 --number 10 --verbose --save /etc/pacman.d/mirrorlist"
alias mirrord="sudo reflector --latest 30 --number 10 --sort delay --save /etc/pacman.d/mirrorlist"
alias mirrors="sudo reflector --latest 30 --number 10 --sort score --save /etc/pacman.d/mirrorlist"
alias mirrora="sudo reflector --latest 30 --number 10 --sort age --save /etc/pacman.d/mirrorlist"
#our experimental - best option for the moment
alias mirrorx="sudo reflector --age 6 --latest 20  --fastest 20 --threads 5 --sort rate --protocol https --save /etc/pacman.d/mirrorlist"
alias mirrorxx="sudo reflector --age 6 --latest 20  --fastest 20 --threads 20 --sort rate --protocol https --save /etc/pacman.d/mirrorlist"

#systeminfo
alias probe="sudo -E hw-probe -all -upload"

# Laptop change brightness
alias bs01="xrandr --output eDP-1 --brightness 0.1"
alias bs02="xrandr --output eDP-1 --brightness 0.2"
alias bs03="xrandr --output eDP-1 --brightness 0.3"
alias bs04="xrandr --output eDP-1 --brightness 0.4"
alias bs05="xrandr --output eDP-1 --brightness 0.5"
alias bs06="xrandr --output eDP-1 --brightness 0.6"
alias bs07="xrandr --output eDP-1 --brightness 0.7"
alias bs08="xrandr --output eDP-1 --brightness 0.8"
alias bs09="xrandr --output eDP-1 --brightness 0.9"
alias bs1="xrandr --output eDP-1 --brightness 1"

# Navigation
alias ..='cd ../'
alias ...='cd ../..'
alias .3='cd ../../..'
alias .4='cd ../../../..'
alias .5='cd ../../../../..'

alias tutdir="cd /home/ton1czech/CODING/Tutorials"
alias ptsdir="cd /home/ton1czech/CODING/Projects"
alias gngdir="cd /home/ton1czech/CODING/Projects/Python/Python3/gingy"
alias dlsdir="cd /mnt/c/Users/ton1czech/Downloads"
alias cvddir="cd /home/ton1czech/CODING/Projects/JavaScript/React/covid19"

# Super List dir command
alias ll="ls -lah --color"

# Custom git commands
alias gS="git pull"
alias gA="git add ."
alias gC="git commit -m '"
alias gP="git push -u origin master"

# sync .files inside git repository Dotfiles
alias config="/usr/bin/git --git-dir=$HOME/Dotfiles --work-tree=$HOME"

# # ex = EXtractor for all kinds of archives
# # usage: ex <file>
ex ()
{
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1   ;;
      *.tar.gz)    tar xzf $1   ;;
      *.bz2)       bunzip2 $1   ;;
      *.rar)       unrar x $1   ;;
      *.gz)        gunzip $1    ;;
      *.tar)       tar xf $1    ;;
      *.tbz2)      tar xjf $1   ;;
      *.tgz)       tar xzf $1   ;;
      *.zip)       unzip $1     ;;
      *.Z)         uncompress $1;;
      *.7z)        7z x $1      ;;
      *.deb)       ar x $1      ;;
      *.tar.xz)    tar xf $1    ;;
      *.tar.zst)   unzstd $1    ;;
      *)           echo "'$1' cannot be extracted via ex()" ;;
    esac
  else
    echo "'$1' is not a valid file"
  fi
}

neofetch
