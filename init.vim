set autoindent
set ruler
set showcmd
syntax on
filetype plugin indent on

call plug#begin('~/.vim/plugged')
" Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'scrooloose/nerdtree'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'gkapfham/vim-vitamin-onec'
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'
call plug#end()

let g:python3_host_prog = 'C:\\Users\\JB\\AppData\\Local\\Programs\\Python\\Python37-32\\python.exe'

" deoplete
" let g:deoplete#enable_at_startup = 1  " start autocomplete 

" ultisnips 
let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<tab>"
let g:UltiSnipsJumpBackwardTrigger="<s-tab>"
let g:UltiSnipsSnippetsDir="D:\\Programs\\Neovim\\share\\nvim\\UltiSnips"
let g:UltiSnipsSnippetDirectories=["D:\\Programs\\Neovim\\share\\nvim\\UltiSnips"]

" colorscheme
colorscheme vitaminonec 

" tab = 4 spaces
set tabstop=4
set shiftwidth=4
set expandtab

" Resize split easily 
:map <C-w><C-Left> <C-w><lt>
:map <C-w><C-Right> <C-w>>
:map <C-w><C-Up> <C-w>-
:map <C-w><C-Down> <C-w>+

:imap <C-BS> <Esc>dbxi
