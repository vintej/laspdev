#!/usr/bin/python

import pexpect
import subprocess
import sys

bash_rc = """# ~/.bashrc: executed by bash(1) for non-login shells.

# Note: PS1 and umask are already set in /etc/profile. You should not
# need this unless you want different defaults for root.
# PS1='${debian_chroot:+($debian_chroot)}\h:\w\$ '
# umask 022

# You may uncomment the following lines if you want `ls' to be colorized:
    # export LS_OPTIONS='--color=auto'
    # eval `dircolors`
    # alias ls='ls $LS_OPTIONS'
    # alias ll='ls $LS_OPTIONS -l'
    # alias l='ls $LS_OPTIONS -lA'
    #
    # Some more alias to avoid making mistakes:
    # alias rm='rm -i'
    # alias cp='cp -i'
    # alias mv='mv -i'
    export MODE=delta_based
    export PROPAGATE_ON_UPDATE=true
    export PEER_SERVICE=partisan_hyparview_peer_service_manager
    """

print(sys.argv[1])
cont = "mn."+sys.argv[1]
childcont = pexpect.spawn('docker exec -it '+cont+' /bin/bash')
childcont.logfile = sys.stdout
#start(childcont, ip_dict[sys.argv[1]]["ip"],ip_dict[sys.argv[1]]["node"])
#childcont.interact()

def start(child):
    global bash_rc
    c_prompt = 'root@'
    #child = pexpect.spawn ('docker exec -it '+cont+' /bin/bash')
    #child.logfile = sys.stdout
    child.expect (c_prompt)
    child.sendline('echo "'+bash_rc+'" > /root/.bashrc')
    child.expect(c_prompt)
    #return child

start(childcont)
print("env_vars set")
