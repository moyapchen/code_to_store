#!/bin/bash

######

# If tmux is weird hanging, try `tmux kill-server`

####




SESSIONNAME=$1
tmux has-session -t $SESSIONNAME &> /dev/null

if [ $? != 0 ]
then
    echo "making new session $SESSIONNAME"
    tmux new-session -s $SESSIONNAME -n script -d
#    tmux send-keys -t $SESSIONNAME "~/bin/script" C-m
else
    echo "taking over"
    TAKEOVER_SESSION='temp_takeover_session'

    if ! tmux has-session -t "$TAKEOVER_SESSION"; then
        tmux new-session -d -s "$TAKEOVER_SESSION"
        tmux set-option -t "$TAKEOVER_SESSION" set-remain-on-exit on
        tmux new-window -kt "$TAKEOVER_SESSION":0  \
            'echo "Use Prefix + L (^B L) to return to session."'
    fi

    # switch sessions to takeover
    for client in $(tmux list-clients -t "$SESSIONNAME" | cut -f 1 -d :); do
        tmux switch-client -c "$client" -t "$TAKEOVER_SESSION"
    done
fi

tmux attach -t $SESSIONNAME

