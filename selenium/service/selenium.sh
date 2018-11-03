#!/bin/bash  
                                                                                                                                                                                                                   
DESC="Selenium Grid Server"
RUN_AS="selenium"
JAVA_BIN="/usr/bin/java"

SELENIUM_DIR="/Data01/selenium"
PID_FILE="$SELENIUM_DIR/selenium-grid.pid"
JAR_FILE="$SELENIUM_DIR/selenium-server.jar"
LOG_DIR="/var/log/selenium"
LOG_FILE="${LOG_DIR}/selenium-grid.log"

USER="selenium"
GROUP="selenium"

MAX_MEMORY="-Xmx256m"
STACK_SIZE="-Xss8m"

DAEMON_OPTS=" $MAX_MEMORY $STACK_SIZE -jar $JAR_FILE -role hub -log $LOG_FILE"

NAME="selenium"

if [ "$1" != status ]; then
    if [ ! -d ${LOG_DIR} ]; then
        mkdir --mode 750 --parents ${LOG_DIR}
        chown ${USER}:${GROUP} ${LOG_DIR}
    fi  
fi


# TODO: Put together /etc/init.d/xvfb
# export DISPLAY=:99.0

. /lib/lsb/init-functions

case "$1" in
    start)
        echo -n "Starting $DESC: "
         
        if [ ! -f $PID_FILE ] ; then
            nohup java -jar $JAR_FILE -role hub & >> selenium.log 2>&1&
            
            echo $(netstat -ltnp | grep -w ':4444' | cut -d '/' -f 1 | awk '{ print $7 }') > $PID_FILE
            echo "Process started"
        else
            echo "Process already started"
        fi
        ;;

    stop)
        echo -n "Stopping $DESC: " 
        if [ -f $PID_FILE ] ; then
            PID=$(netstat -ltnp | grep -w ':4444' | cut -d '/' -f 1 | awk '{ print $7 }');
            echo "Killing process $PID"
            kill $PID;
            rm $PID_FILE
            echo "Stopped $DESC"
        else
	    echo "The process was not running..."
        fi
        ;;

    restart|force-reload)
        echo -n "Restarting $DESC: "
        start-stop-daemon --stop --pidfile $PID_FILE
        sleep 1
        start-stop-daemon -c $RUN_AS --start --background --pidfile $PID_FILE  --make-pidfile --exec $JAVA_BIN -- $DAEMON_OPTS
        echo "$NAME."
        ;;

    status)
        status_of_proc -p "$PID_FILE" "$DAEMON" "selenium" && exit 0 || exit $?
        ;;

    *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|force-reload}" >&2
        exit 1
        ;;
esac
