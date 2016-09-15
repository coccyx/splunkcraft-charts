IFS='
'
env - `cat /root/env.sh` /bin/bash -c $* > /tmp/cron.log 2>&1