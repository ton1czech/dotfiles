:syntax on

:set noerrorbells

:set tabstop=4 softtabstop=4
:set smarttab
:set smartindent
:set autoindent

:set number relativenumber

:set nowrap
:set incsearch
:set clipboard=unnamedplus

:set smartcase

:set noswapfile
:set nobackup
:set undodir=~/.vim/undodir
:set undofile

call plug#begin('~/.vim/plugged')

Plug 'tpope/vim-fugitive'
Plug 'tpope/vim-surround'
Plug 'scrooloose/nerdtree'
Plug 'airblade/vim-gitgutter'
Plug 'valloric/youcompleteme'
Plug 'kien/ctrlp.vim'
Plug 'dracula/vim', { 'as': 'dracula' }

call plug#end()
":source%
":PlugInstall

if executable('rg')
    let g:rg_derive_root='true'
endif

let g:ctrpl_use_caching = 0
