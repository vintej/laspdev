
OUTPUT=$(ps -aef | grep lasp_main | awk 'NR==1{print $2}')
kill -9 $OUTPUT
