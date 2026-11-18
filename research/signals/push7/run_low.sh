#!/bin/bash
# Run a command at below-normal priority (Windows) and wait for it:  bash run_low.sh EXE ARGS...
# Used for every long run of push 7 (the machine is shared).
exe=$(cygpath -w "$1"); shift
cmd //c start //belownormal //b //wait "$exe" "$@"
