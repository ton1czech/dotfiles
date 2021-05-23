#############
# ~/.bashrc #
#############

### ADDING TO THE PATH ###
if [ -d "$HOME/.bin" ] ;
  then PATH="$HOME/.bin:$PATH"
fi

if [ -d "$HOME/.local/bin" ] ;
  then PATH="$HOME/.local/bin:$PATH"
fi


### BASICS ###
# if not running interactively, don't do anything
[[ $- != *i* ]] && return

# ignore upper and lowercase when TAB completion
bind "set completion-ignore-case on"

# Check the window size after each command and, if necessary,
# Update the values of LINES and COLUMNS.
shopt -s checkwinsize


### EXPORT ###
export HISTCONTROL=ignoreboth:erasedups
export TERM="xterm-256color"
export EDITOR="vim"


### PS ###
PS1='\[\e[0;2m\]\u\[\e[0m\]: \[\e[0;38;5;46m\]<\[\e[0;38;5;46m\]\w\[\e[0;38;5;46m\]> \[\e[0;91m\][\[\e[0;91m\]$(git branch 2>/dev/null | grep '"'"'^*'"'"' | colrm 1 2)\[\e[0;91m\]]\[\e[0;1m\]\$ \[\e[0m\]'


### ALIASES ###
# colorize the grep command output for ease of use
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'

# continue download
alias wget="wget -c"

# top process eating memory
alias psmem="ps auxf | sort -nr -k 4"
alias psmem10="ps auxf | sort -nr -k 4 | head -10"

# top process eating CPU
alias pscpu="ps auxf | sort -nr -k 3"
alias pscpu10="ps auxf | sort -nr -k 3 | head -10"

# confirm before overwriting something
alias cp="cp -i"
alias mv="mv -i"
alias rm="rm -i"

# hardware info
alias hw="hwinfo --short"

# systeminfo
alias probe="sudo -E hw-probe -all -upload"

# navigation
alias ..='cd ../'
alias ...='cd ../..'
alias .3='cd ../../..'
alias .4='cd ../../../..'
alias .5='cd ../../../../..'

alias tutdir="cd /home/ton1czech/CODING/Tutorials"
alias ptsdir="cd /home/ton1czech/CODING/Projects"
alias gngdir="cd /home/ton1czech/CODING/Projects/Python/Python3/gingy"
alias cvddir="cd /home/ton1czech/CODING/Projects/JavaScript/React/covid19"

# super List dir command
alias ls="exa -lah --color=always --group-directories-first"
alias lt="exa -aT --color=always --group-directories-first"

# custom git commands
alias gS="git pull"
alias gA="git add ."
alias gC="git commit -m '"
alias gP="git push -u origin master"

# sync .files inside git repository Dotfiles
alias config="/usr/bin/git --git-dir=$HOME/Dotfiles --work-tree=$HOME"

# EXtractor for all kinds of archives
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

archey