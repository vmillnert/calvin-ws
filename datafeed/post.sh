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
	  IFS=$';';
		arr=(${LINE});
		if [ ${arr[0]} == "B" ];
		then
			data=${arr[1]};
			h=${arr[2]};
			while read DEST; do
				echo $(date +%H:%m:%S) UPDATE CELL ${DEST}: ${data} | tee -a ~/datafeed.log;
				echo $data | curl --connect-timeout 1 -d @- -H "Content-Type: application/json" ${DEST}/node/attribute/imeicells;
			done < $2;
		else
			index=${arr[1]};
			data=${arr[2]};
			h=${arr[3]};
			to=$(tail -n +${index} ${2} | head -n 1);
			echo $(date +%H:%m:%S) UPDATE HEALTH ${to}: ${data} | tee -a ~/datafeed.log;
			echo $data | curl --connect-timeout 1 -d @- -H "Content-Type: application/json" ${to}/node/attribute/healthMetric;
		fi;
    sleep $h;
  done < $1;
done;
