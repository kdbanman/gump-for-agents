#!/bin/bash
cd "$(dirname "$0")"
while [ ! -e stop ]; do
  if [ -s prio.txt ]; then cmd=$(head -1 prio.txt); sed -i 1d prio.txt
  elif [ -s queue.txt ]; then cmd=$(head -1 queue.txt); sed -i 1d queue.txt
  else sleep 2; continue; fi
  echo "$(date -u +%H:%M:%S) START $cmd" >> runner.log
  eval "$cmd"
  echo "$(date -u +%H:%M:%S) END" >> runner.log
done
