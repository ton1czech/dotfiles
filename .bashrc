#############
# ~/.bashrc #
#############

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export HISTCONTROL=ignoreboth:erasedups
export TERM="xterm-256color"
export EDITOR="vim"

PS1='\[\e[0;2m\]\u\[\e[0m\]: \[\e[0;38;5;46m\]<\[\e[0;38;5;46m\]\w\[\e[0;38;5;46m\]> \[\e[0;91m\][\[\e[0;91m\]$(git branch 2>/dev/null | grep '"'"'^*'"'"' | colrm 1 2)\[\e[0;91m\]]\[\e[0;1m\]\$ \[\e[0m\]'

if [ -d "$HOME/.bin" ] ;
  then PATH="$HOME/.bin:$PATH"
fi

if [ -d "$HOME/.local/bin" ] ;
  then PATH="$HOME/.local/bin:$PATH"
fi

# Ignore upper and lowercase when TAB completion
bind "set completion-ignore-case on"

# Check the window size after each command and, if necessary,
# Update the values of LINES and COLUMNS.
shopt -s checkwinsize

#####                    ALIASES                   #####

# Colorize the grep command output for ease of use
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'

# Use all cores
alias uac="sh ~/.bin/main/000*"

# Continue download
alias wget="wget -c"

# ps
alias psa="ps auxf"
alias psgrep="ps aux | grep -v grep | grep -i -e VSZ -e"

# Get top process eating memory
alias psmem="ps auxf | sort -nr -k 4"
alias psmem10="ps auxf | sort -nr -k 4 | head -10"

# Get top process eating CPU
alias pscpu="ps auxf | sort -nr -k 3"
alias pscpu10="ps auxf | sort -nr -k 3 | head -10"

# Grub update
alias update-grub="sudo grub-mkconfig -o /boot/grub/grub.cfg"

# Add new fonts
alias update-fc='sudo fc-cache -fv'

# Switch between bash and zsh
alias tobash="sudo chsh $USER -s /bin/bash && echo 'Now log out.'"
alias tozsh="sudo chsh $USER -s /bin/zsh && echo 'Now log out.'"
alias tofish="sudo chsh $USER -s /bin/fish && echo 'Now log out.'"

# Switch between lightdm and sddm
alias tolightdm="sudo pacman -S lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings --noconfirm --needed ; sudo systemctl enable lightdm.service -f ; echo 'Lightm is active - reboot now'"
alias tosddm="sudo pacman -S sddm --noconfirm --needed ; sudo systemctl enable sddm.service -f ; echo 'Sddm is active - reboot now'"

# Confirm before overwriting something
alias cp="cp -i"
alias mv="mv -i"
alias rm="rm -i"

# Hardware info --short
alias hw="hwinfo --short"

# Get fastest mirrors in your neighborhood
alias mirror="sudo reflector -f 30 -l 30 --number 10 --verbose --save /etc/pacman.d/mirrorlist"
alias mirrord="sudo reflector --latest 30 --number 10 --sort delay --save /etc/pacman.d/mirrorlist"
alias mirrors="sudo reflector --latest 30 --number 10 --sort score --save /etc/pacman.d/mirrorlist"
alias mirrora="sudo reflector --latest 30 --number 10 --sort age --save /etc/pacman.d/mirrorlist"
# Our experimental - best option for the moment
alias mirrorx="sudo reflector --age 6 --latest 20  --fastest 20 --threads 5 --sort rate --protocol https --save /etc/pacman.d/mirrorlist"
alias mirrorxx="sudo reflector --age 6 --latest 20  --fastest 20 --threads 20 --sort rate --protocol https --save /etc/pacman.d/mirrorlist"

# Systeminfo
alias probe="sudo -E hw-probe -all -upload"

# Navigation
alias ..='cd ../'
alias ...='cd ../..'
alias .3='cd ../../..'
alias .4='cd ../../../..'
alias .5='cd ../../../../..'

alias tutdir="cd /home/ton1czech/CODING/Tutorials"
alias ptsdir="cd /home/ton1czech/CODING/Projects"
alias gngdir="cd /home/ton1czech/CODING/Projects/Python/Python3/gingy"
alias cvddir="cd /home/ton1czech/CODING/Projects/JavaScript/React/covid19"

# Super List dir command
alias ls="exa -lah --color=always --group-directories-first"
alias lt="exa -aT --color=always --group-directories-first"

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
