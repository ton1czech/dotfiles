:syntax on

:set noerrorbells				" no annoying sounds

:set tabstop=4 softtabstop=4	" tab 4 spaces
:set smarttab					" auto tabs
:set smartindent				" auto indentation
:set autoindent					" auto indentation

:set number relativenumber		" show numbers

:set nowrap						" no text wraping, use always one line
:set incsearch					" incremental search
:set clipboard=unnamedplus		" copy/pase between vim and other apps

:set smartcase					" better searching

:set noswapfile					" no swap
:set nobackup					" no auto backups
:set undodir=~/.vim/undodir		" set undo directory
:set undofile					" set undo file

call plug#begin('~/.vim/plugged')

Plug 'morhetz/gruvbox'
Plug 'tpope/vim-fugitive'
Plug 'tpope/vim-surround'
Plug 'scrooloose/nerdtree'
Plug 'airblade/vim-gitgutter'
Plug 'valloric/youcompleteme'
Plug 'kien/ctrlp.vim'

call plug#end()
":source%
":PlugInstall

colorscheme gruvbox

set background=dark

if executable('rg')
    let g:rg_derive_root='true'
endif

let g:ctrpl_use_caching = 0
