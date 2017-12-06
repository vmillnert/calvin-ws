#!/bin/bash 

## configuration. 
CR1=10.32.0.7
CR2=10.32.0.8
INTERFACE=eth0
## end of configuration

function start() 
{
  ## outbound.

  ip link set eth0 qlen 1000

  tc qdisc add dev $INTERFACE root handle 1:0 htb default 10
  # default class
  tc class add dev $INTERFACE parent 1:0 classid 1:10 htb rate 1024mbit 

  # "CR1" traffic class - outbound bandwidth limit
  tc class add dev $INTERFACE parent 1:0 classid 1:11 htb rate 1024mbit

  # "CR2" traffic class - outbound bandwidth limit
  tc class add dev $INTERFACE parent 1:0 classid 1:12 htb rate 1024mbit

  # network emulation - add latency. 
  tc qdisc add dev $INTERFACE parent 1:11 handle 11:0 netem delay 5ms #5ms 25% distribution normal
  tc qdisc add dev $INTERFACE parent 1:12 handle 12:0 netem delay 25ms #5ms 25% distribution normal
 
  # filter packets into appropriate traffic classes. 
  tc filter add dev $INTERFACE protocol ip parent 1:0 prio 1 u32 match ip dst $CR1 flowid 1:11
  tc filter add dev $INTERFACE protocol ip parent 1:0 prio 1 u32 match ip dst $CR2 flowid 1:12

  ## inbound

  # inbound qdisc. 
  # tc qdisc add dev $INTERFACE handle ffff: ingress 

  # attach a policer for "dB" class.
  #tc filter add dev $INTERFACE protocol ip parent ffff: prio 1 u32 match ip src $CR1 \
  # police rate 128kbit burst 10k drop flowid :1
 
  # attach a policer for "mem cache" traffic class. 
  #tc filter add dev $INTERFACE protocol ip parent ffff: prio 1 u32 match ip src $CR2 \
  # police rate 512kbit burst 10k drop flowid :2
   
  # 
  # touch $LOCKFILE
}

function stop () 
{
  # remove any existing ingress qdisc. 
  # tc qdisc del dev $INTERFACE ingress
  ## remove any existing egress qdiscs
  tc qdisc del dev $INTERFACE root

  # rm -f $LOCKFILE
}

function status ()
{
  echo "Active Queue Disciplines for $INTERFACE"
  tc -s qdisc show dev $INTERFACE
  echo 
  echo "Active Queueing Classes for $INTERFACE "
  tc -s class show dev $INTERFACE
  echo 
  echo "Active Traffic Control Filters for $INTERFACE"
  tc -s filter show dev $INTERFACE 
}

# main 

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart|reload)
    stop
    start
    ;;
  #condrestart)
  #  if [ -f $LOCKFILE ]; then
  #   stop
  #   start
  #  fi
  #  ;;
  status)
    status
    ;;
  *)
    echo $"Usage: $0 {start|stop|restart|status}"
    exit 1
esac

exit 0;
