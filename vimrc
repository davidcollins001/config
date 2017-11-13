" sets format options in INSERT mode
"  c - Automatically wrap comments.  Insert the comment leader automatically.
"  r - Insert comment leader in a comment when a new line is inserted.
"  t - Automatically wrap text when the textwidth value is reached.  If
"      textwidth is not defined, text will not be wrapped.
set formatoptions=crt

"" because I'm running vim from my home directory
"chdir H:\

"""""
""""" BASIC OPTION SETTINGS
"""""

set textwidth=80
set number              " makes Vim show you line numbers on the left
set nocompatible        " Be incompatible with vi, please
"set backspace=2         " Backspace all the way to wherever it takes
set bioskey             " Use PC BIOS to read keyboard, for better ^C detection
"set cpoptions=cFs$      " Vi compatibility options
set helpheight=15	" 15 lines of help is enough, thank you
"set infercase           " Infer case for ignorecase keyword completion
"set keywordprg=man\ -a  " Display all man entries for `K' lookup
set statusline=%<%F%h%m%r%=\[%B\]\ %l,%c%V\ %P
set laststatus=2        " Always show a status line
"set notextmode          " Don't append bloody carriage returns
set ruler               " Enable ruler on status line
set autoindent          " copies indent from the previous line to new line
set shiftwidth=4        " Indent by four columns at a time
set tabstop=4           " determines how many spaces tabs shift text
set expandtab           " insert spaces in tabs
"set tabpagemax=100      " allow up to 100 tabs
"set shortmess=ao        " Shorter status messages
set showmatch           " Show matching delimiters
set showmode            " Show current input mode in status line
set sidescroll=8        " Horizontal scrolling 8 columns at a time
set ignorecase
set smartcase           " Ignore ignorecase for uppercase letters in patterns
set splitbelow          " Split windows below current window
set nostartofline       " Do not home cursor to beginning of line
set ttyscroll=5         " Scroll at most 5 lines at a time
set whichwrap=<,>,[,]   " Left/right arrow keys wrap
set nowrap
set winheight=4         " At least 4 lines for current window
set cinoptions=:0,p0,t0,(1s           " C language indent options
"set tags=.git/tags; "./tags,.git/tags,tags,../tags " Tags file search path
set tags=.git/tags;     " Tags file search path
set dictionary=/usr/dict/words        " Dictionary file path
set path=.,include,../include,../../include,/usr/local/include/g++,/usr/local/lib/g++-include,/usr/include,, " Include file path
set wildmode=longest,list	" Command line completion matches longest common
set backup
set showcmd
set gcr=a:blinkon0
set errorbells
set visualbell
set nowarn
set hidden              " Allow edited files to be hidden
set hlsearch
set mouse=a             " Enable mouse to place cursor

"highlight! Cursor gui=NONE guifg=black guibg=cyan
"highlight! VisualCursor gui=NONE guifg=darkblue guibg=black

" highlight Cursor gui=NONE guifg=white guibg=black
" highlight iCursor gui=NONE guifg=white guibg=red
" highlight Cursor ctermfg=white ctermbg=black
" highlight iCursor ctermfg=white ctermbg=red
"set guicursor+=n-v-c:Cursor
"set guicursor+=i:iCursor
"set cursorline

" tell vim where to find tag file
" set tags=./.git/tags;,.git/tags;
map <leader>t :tn<cr>
map <leader>st :stn<cr>
" ctags optimization
set autochdir

"""""
""""" EDITING MODES
"""""

"" Clear all existing autocommands (in case this is sourced again)
"autocmd!

" enable automatic mode switching.
" see :help filetype for more details.
syntax on
":help :syn-sync
"syntax sync fromstart   "syntax is synced from first fold
"syn-sync-first
filetype plugin indent on


"""
""""" MACRO DEFINITIONS
"""""

" Set text reformatting width (right margin)
nmap _2 :set textwidth=72<CR>
nmap _7 :set textwidth=70<CR>
nmap _8 :set textwidth=80<CR>
nmap _0 :set textwidth=0<CR>
" /ef to split and scroll lock windows
nmap <silent> <Leader>ef :vsplit<bar>wincmd l<bar>exe "norm!  Ljz<c-v><cr>"<cr>:set scb<cr>:wincmd h<cr>:set scb<cr>

" Move around in quickfix mode
map ( :cp<CR>0
map ) :cn<CR>0

nmap _D md:r !date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S'<CR>`d
if version >= 500
  nmap _D mdo<C-R>=strftime("%Y-%m-%d %H:%M:%S")<CR><Esc>`d
endif


"""""
""""" FUNCTION KEYS
"""""

"   F1: Help  F5: Center line  F9: Reformat paragraph
"   F2: Save  F6: Next window  F10: Zoom window
"   F3: Edit  F7: Prev buffer  F11/S-F3: Split window
"   F4: Quit  F8: Next buffer  F12/S-F4: Save & quit all

nmap <F1> :ls<CR>:b<Space>
imap <F1> <C-O>:ls<CR>:b<Space>
cmap <F1> <C-U>:ls<CR>:b<Space>
nmap <F2> :w<CR>
imap <F2> <C-O>:w<CR>
cmap <F2> <C-U>w<Space>
nmap <F3> :e<Space>
imap <F3> <C-O>:e<Space>
cmap <F3> <C-U>e<Space>
nmap <F4> :bwipeout<CR>
imap <F4> <C-O>:bwipeout<CR>
cmap <F4> <C-U>bwipeout<CR>
" nmap <F4> :call CloseOrQuit()<CR>
" imap <F4> <C-O>:call CloseOrQuit()<CR>
" cmap <F4> <C-U>call CloseOrQuit()<CR>
nmap <F5> zz
vmap <F5> zz
imap <F5> <C-O>zz
nmap <F6> <C-W><C-W>
imap <F6> <C-O><C-W><C-W>
nmap <S-F6> <C-W>W
imap <S-F6> <C-O><C-W>W
nmap <F7> :bprevious<CR>
imap <F7> <C-O>:bprevious<CR>
nmap <F8> :bnext<CR>
imap <F8> <C-O>:bnext<CR>
nmap < :bprevious<CR>
nmap > :bnext<CR>
nmap <S-F10> <C-W>_
imap <S-F10> <C-O><C-W>_
nmap <F11> :new<Space>
imap <F11> <C-O>:new<Space>
cmap <F11> <C-U>new<Space>
nmap <F12> :xa<CR>
imap <F12> <C-O>:xa<CR>
cmap <F12> <C-U>xa

nmap <C-X> :w<CR>

map  <S-F3> <F11>
map! <S-F3> <F11>
map  <S-F4> <F12>
map! <S-F4> <F12>

map  <Esc>OT <F5>
map! <Esc>OT <F5>
map  <Esc>OU <F6>
map! <Esc>OU <F6>
map  <Esc>OV <F7>
map! <Esc>OV <F7>
map  <Esc>OW <F8>
map! <Esc>OW <F8>
map  <Esc>OX <F9>
map! <Esc>OX <F9>
map  <Esc>OY <F10>
map! <Esc>OY <F10>
map  <Esc>OZ <F11>
map! <Esc>OZ <F11>
map  <Esc>O[ <F12>
map! <Esc>O[ <F12>
map  <Esc>[5~ <PageUp>
map! <Esc>[5~ <PageUp>
map  <Esc>[6~ <PageDown>
map! <Esc>[6~ <PageDown>
map  <Esc>[1~ <Home>
map! <Esc>[1~ <Home>
map  <Esc>[4~ <End>
map! <Esc>[4~ <End>
map  <Esc>[2~ <Insert>
map! <Esc>[2~ <Insert>

map [t :tlast<cr>
map ]t :tnext<cr>
map =t :tselect<cr>

" -/+ scroll like ^e/^y
map - 
map + 
map  zz
map dl 0D
map <C-x><C-s> <Esc>:w<CR>

" buffer mappings
map :bd<CR> :b#<CR>:bd#<CR>

" folding
set foldmethod=indent   " fold based on syntax
set foldminlines=0      " fold a single line
"set foldlevelstart=1    " start with all folds closed

" python specific
autocmd FileType python setlocal foldmethod=indent
autocmd FileType python setlocal foldignore=
"autocmd FileType python setlocal nosmartindent autoindent
"autocmd FileType python setlocal nosmartindent
" add breakpoint using \(b|B)
autocmd FileType python noremap <silent> <leader>b oimport pdb; pdb.set_trace()<esc>
autocmd FileType python noremap <silent> <leader>B Oimport pdb; pdb.set_trace()<esc>
let g:flake8_show_in_gutter=1
autocmd BufWritePost *.py call Flake8()
autocmd BufWritePost *.pxy call Flake8()

" set cython filetypes as python
autocmd BufNewFile,BufRead *.pyx  setlocal filetype=python
autocmd BufNewFile,BufRead *.pxd setlocal filetype=python

" xml specific
"au FileType xml exe ":silent 1,$!xmllint --format --recover - 2>/dev/null"
autocmd FileType xml setlocal foldmethod=indent
autocmd FileType xml setlocal shiftwidth=2

" slang specific
autocmd BufRead,BufNewFile *.s setlocal filetype=slang
autocmd FileType slang setlocal syntax=CPP
autocmd FileType slang setlocal foldmethod=indent

" java specific
autocmd FileType java setlocal foldmethod=indent
autocmd FileType java setlocal noexpandtab
autocmd FileType vim setlocal foldmethod=indent

augroup vimrcEx
  au!
    " When editing a file, always jump to the last known cursor position.
    " Don't do it when the position is invalid or when inside an event handler
    " (happens when dropping a file on gvim).
    autocmd BufReadPost *
        \ if line("'\"") > 0 && line("'\"") <= line("$") |
        \   exe "normal g`\"" |
        \ endif
augroup END

" Run gvim maximized
if has("gui_running")
    au GUIEnter * simalt ~x

    set guioptions=ac
    set guioptions-=mrlb
    set guifont=Consolas:h11
endif

"" macros - http://byron.theclarkfamily.name/blog/archive/2007/03/1/
"" insert function boiler plate
let @f='0y$O/64a*o**  Routine: po**** Summary:64i*A/ja = Func()Returns( ){};k'
let @s='0i"A",'

"" make paragraph jump skip folds and not whitespace lines
let g:ip_skipfold=1
let g:ip_boundary='"\?\s*$'

let $TMP="C:\\tmp"

function MyDiff()
   let opt = '-a --binary '
   if &diffopt =~ 'icase' | let opt = opt . '-i ' | endif
   if &diffopt =~ 'iwhite' | let opt = opt . '-b ' | endif
   let arg1 = v:fname_in
   if arg1 =~ ' ' | let arg1 = '"' . arg1 . '"' | endif
   let arg2 = v:fname_new
   if arg2 =~ ' ' | let arg2 = '"' . arg2 . '"' | endif
   let arg3 = v:fname_out
   if arg3 =~ ' ' | let arg3 = '"' . arg3 . '"' | endif
   if $VIMRUNTIME =~ ' '
     if &sh =~ '\<cmd'
       if empty(&shellxquote)
         let l:shxq_sav = ''
         set shellxquote&
       endif
       let cmd = '"' . $VIMRUNTIME . '\diff"'
     else
       let cmd = substitute($VIMRUNTIME, ' ', '" ', '') . '\diff"'
     endif
   else
     let cmd = $VIMRUNTIME . '\diff'
   endif
   silent execute '!' . cmd . ' ' . opt . arg1 . ' ' . arg2 . ' > ' . arg3
   if exists('l:shxq_sav')
     let &shellxquote=l:shxq_sav
   endif
 endfunction

set diffexpr=MyDiff()

"" pymode settings
let g:pymode_rope = 0
let g:pymode_lint_checkers = []


"Change read/only files to read/write when they are edited
au FileChangedRO * !start attrib -r %
au FileChangedRO * :let s:changedRO = 1
au FileChangedRO * :set noro

"Don't ask about the modified read-only file
au FileChangedShell * call s:HandleChangedROFile()

function s:HandleChangedROFile()
   if exists('s:changedRO') && s:changedRO == 1
      let s:changedRO = 0
      let v:fcs_choice='reload'
   else
      v:fcs_choice='ask'
   endif
endfunction

let g:scratch_height = 1.0


" Commenting blocks of code.
autocmd FileType c,cpp,java,scala let b:comment_leader = '// '
autocmd FileType sh,ruby,python   let b:comment_leader = '# '
autocmd FileType conf,fstab       let b:comment_leader = '# '
autocmd FileType tex              let b:comment_leader = '% '
autocmd FileType mail             let b:comment_leader = '> '
autocmd FileType vim              let b:comment_leader = '" '

noremap <silent> ,cc :<C-B>silent <C-E>s/\(\S\)/<C-R>=escape(b:comment_leader,'\/')<CR>\1/<CR> :nohlsearch<CR> :call histdel("search", -1)<CR>
noremap <silent> ,cu :<C-B>silent <C-E>s/\V<C-R>=escape(b:comment_leader,'\/')<CR>//e<CR> :nohlsearch<CR> :call histdel("search", -1)<CR>

" " for command mode
" nnoremap <S-Tab> <<
" " for insert mode
" inoremap <S-Tab> <C-d>

func! DeleteTrailingWS()
  exe "normal mz"
  %s/\s\+$//ge
  exe "normal `z"
endfunc

autocmd BufWrite * :call DeleteTrailingWS()

" Format xml
func! FormatXML()
    setlocal ft=xml
    let save_pos = getpos(".")
    %s/\\\n//ge
    %s/></>\r</ge
    %s/> </>\r</ge
    normal! gg=G
    call setpos('.', save_pos)
endfunc

nmap :fx :call FormatXML()<CR>

" Search for selected text, forwards or backwards.
vnoremap <silent> * :<C-U>
  \let old_reg=getreg('"')<Bar>let old_regtype=getregtype('"')<CR>
  \gvy/<C-R><C-R>=substitute(
  \escape(@", '/\.*$^~['), '\_s\+', '\\_s\\+', 'g')<CR><CR>
  \gV:call setreg('"', old_reg, old_regtype)<CR>
vnoremap <silent> # :<C-U>
  \let old_reg=getreg('"')<Bar>let old_regtype=getregtype('"')<CR>
  \gvy?<C-R><C-R>=substitute(
  \escape(@", '?\.*$^~['), '\_s\+', '\\_s\\+', 'g')<CR><CR>
  \gV:call setreg('"', old_reg, old_regtype)<CR>

"" remove search highlight after search with ,/
noremap <silent> ,/ :nohlsearch<CR>
"" toggle paste mode
noremap <silent> ,p :set pastetoggle<CR>



filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'
Plugin 'nvie/vim-flake8'
Plugin 'vim-scripts/indentpython.vim'
" Plugin 'scrooloose/syntastic'

" Add all your plugins here (note older versions of Vundle used Bundle instead of Plugin)


" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required


