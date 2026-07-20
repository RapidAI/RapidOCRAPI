#!/bin/sh
### BEGIN INIT INFO
# Provides:          start.sh
# Required-start:    $local_fs $remote_fs $network $syslog
# Required-Stop:     $local_fs $remote_fs $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# chkconfig: 2345 80 90
# Short-Description: starts the API server daemon
# Description:       starts the rapidocr_api API server daemon;
### END INIT INFO

# 从环境变量 WORKERS 读取，如果未设置或为空，则默认为 2
WORKERS=${WORKERS:-2}

rapidocr_api -ip 0.0.0.0 -p 9003 -workers $WORKERS
