#!/bin/bash
exec python autoscouter_docker.py &
exec echo "end" &
exec ls
#exec python copyschedule.py