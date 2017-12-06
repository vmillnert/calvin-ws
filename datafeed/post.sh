#!/bin/bash
# We should probably do this:
#   Set the CellId as a property on the runtime
#
#   Set the IMEI as a property of the application instance
#     A generic call to some POST method matches the 'emei' key to the application and sets the parameter 'cellid' on the application.
#    Trigger a deployment decision and the 'cellid' will match a new cell. DC must somehow also be in the list. 

if [ "x$1" == "x-d" ];
then
  echo $@ > /tmp/log.1;
  shift 1;
  setsid $0 $@ >/tmp/log 2>&1 &
  exit;
fi; 

while true; do
  while read LINE; do
    while read DEST; do
      echo UPDATE $(date) ${DEST}
      echo $LINE | curl -d @- -H "Content-Type: application/json" ${DEST}/actor/putmatch;
    done < $2;
    sleep 1;
  done < $1;
done;
