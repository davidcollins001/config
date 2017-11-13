
# Command line history:
def _completion():
    import atexit
    import os
    import readline
    import rlcompleter
    import sys

    readline.parse_and_bind('tab: complete')

    history_dir = os.path.join(os.path.expanduser('~'), '.python/history')
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)

    # Support multiple executables, including virtualenvs, by keying history
    # files against the inode of the current Python executable.
    executable_inode = str(os.stat(sys.executable).st_ino)
    history_file = os.path.join(history_dir, 'pdb_'+executable_inode)

    if os.path.exists(history_file):
        readline.read_history_file(history_file)
    atexit.register(readline.write_history_file, history_file)


def exit_gracefully(signum, frame):
    import signal
    import sys

    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)


def capture_sigint():
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)



try:
    _completion()
    # capture_sigint()
    del _completion#, capture_sigint
except Exception:
    import sys
    print >>sys.stderr, "Couldn't get completion and history working."


