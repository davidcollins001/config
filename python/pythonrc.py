# Add auto-completion and a stored history file of commands to your Python
# interactive interpreter. Requires Python 2.0+, readline. Autocomplete is
# bound to the Esc key by default (you can change it - see readline docs).
#
# Store the file in ~/.pystartup, and set an environment variable to point
# to it:  "export PYTHONSTARTUP=/home/user/.pystartup" in bash.
#
# Note that PYTHONSTARTUP does *not* expand "~", so you have to put in the
# full path to your home directory.


def _completion():
    import atexit
    import os
    import readline
    import rlcompleter  # noqa: F401
    import sys

    readline.parse_and_bind('tab: complete')

    history_dir = os.path.join(os.path.expanduser('~'), '.python/history')
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)

    # Support multiple executables, including virtualenvs, by keying history
    # files against the inode of the current Python executable.
    executable_inode = str(os.stat(sys.executable).st_ino)
    history_file = os.path.join(history_dir, executable_inode)

    if os.path.exists(history_file):
        readline.read_history_file(history_file)
    atexit.register(readline.write_history_file, history_file)


def pp(*a, **k):
    from pprint import pprint
    pprint(*a, **k)


try:
    _completion()
    del _completion
except Exception:
    import sys
    print >>sys.stderr, "Couldn't get completion and history working."
