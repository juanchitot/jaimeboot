#!/bin/bash
i=0
sleep_time='10m'
graph=$1
from=$2
to=$3
from_account=$4
proxy_host=$5
proxy_port=$6
pid=$$

echo "From $from, To $to , From account $from_account"
proxy=''

if [[ -n "$proxy_host" && -n "$proxy_port" ]] ; then
    proxy="-o proxy_host=$proxy_host -o proxy_port=$proxy_port"
    echo 'Voy con proxy '$proxy
fi

while read line  ; do
    let i=$i+1;
    if [[ i -lt "$from" ]] ; then
	continue;
    fi
    account=`echo $line | sed -re 's/([^ ]*) (.*)/\1/'`
    passwd=`echo $line | sed -re 's/[^ \t]+[ \t]+(.*)/\1/'`
    username=`echo $line | sed -re 's/([^@]*).*/\1/'`
    
    if [ -n "$from_account" ] ; then
	if [[ "$from_account" ==  "$account" ]] ; then
	    from_account='';
	fi
	continue;
    fi
    echo 'Entering on account '$account' with pass '$passwd
    d=`date  '+%Y-%m-%d-%T'`
    ./jaime.py -g $graph -l 'jaime_'$pid'.log' -l $account'_'$d'.log' -o "username=$account" -o "password=$passwd" $proxy > $account'_data_'$d'.log'
    echo "sleeping $sleep_time"
    sleep $sleep_time
    if [[ i -ge "$to" ]] ; then
	break;
    fi

done < /home/juanmr/Downloads/not_witness_accounts.txt
