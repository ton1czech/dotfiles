# Path to Oh My Fish install.
set -q XDG_DATA_HOME
  and set -gx OMF_PATH "$XDG_DATA_HOME/omf"
  or set -gx OMF_PATH "$HOME/.local/share/omf"

# Load Oh My Fish configuration.
source $OMF_PATH/init.fish

#####                   ALIASES                    #####

# Colorize the grep command output for ease of use
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'

# Use all cores
alias uac="sh ~/.bin/main/000*"

# Continue download
alias wget="wget -c"

# PS
alias psa="ps auxf"
alias psgrep="ps aux | grep -v grep | grep -i -e VSZ -e"

# Grub update
alias update-grub="sudo grub-mkconfig -o /boot/grub/grub.cfg"

# Add new fonts
alias update-fc="sudo fc-cache -fv"

# Confirm before overwriting something
alias cp="cp -i"
alias mv="mv -i"
alias rm="rm -i"

# Hardware info --short
alias hw="hwinfo --short"

# Systeminfo
alias probe="sudo -E hw-probe -all -upload"

# Navigation
alias ..="cd ../"
alias ...="cd ../.."
alias .3="cd ../../.."
alias .4="cd ../../../.."
alias .5="cd ../../../../.."

alias tutdir="cd /home/ton1czech/CODING/Tutorials"
alias ptsdir="cd /home/ton1czech/CODING/Projects"
alias gngdir="cd /home/ton1czech/CODING/Projects/Python/Python3/gingy"
alias cvddir="cd /home/ton1czech/CODING/Projects/JavaScript/React/covid19"

# Super List dir command
alias ll="ls -lah --color"

# Custom git commands
alias gS="git pull"
alias gA="git add ."
alias gC="git commit -m '"
alias gP="git push -u origin master"
