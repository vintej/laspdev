pkill -f system_main
pkill -f setup_lasp
pkill -f job4overlay
#OUTPUT=$(ps -aef | grep lasp_main | awk 'NR==1{print $2}')
#kill -9 $OUTPUT
