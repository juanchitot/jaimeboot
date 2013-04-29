#!/bin/bash


function get_random_line (){
    names_file=$1    
    names_count=`cat $names_file| wc -l`
    let rand_line=$RANDOM%$names_count
    echo -n `sed -ne "$rand_line,$rand_line p" < $names_file`
}



IFS=","

while read -r line
do

    fst=$(get_random_line '/home/juanmr/nombres.txt' )
    lst=$(get_random_line '/home/juanmr/apellidos.txt')
    randhost=$(get_random_line  '/home/juanmr/ips.txt')

    read -r f1 f2 f3 <<<"$line"
    echo  "$f1 --- $f2 --- $f3";
    echo -e $fst $lst
    echo "esto es el ip "$f2
    who=$(whois $f2)
    user=$( echo $who | sed -nr 's/person: +//p')
    phone=$( echo $who | sed -nr 's/phone: +//p' | sed -nr '1,1  s/[^+ 0-9]+//p' )
    echo este es el phone $phone esto el user $user
    echo ssh -D 10090 -N -f  tunel@$randhost
    ssh -D 10090 -N   tunel@$randhost &
    ssh_pid=$!
    echo "este es el pid ssh $ssh_pid"
    cname=$(echo $f1 |  sed -nr 's/(\.[a-z]+)$//p')
    echo   ./jaime.py -l jaime_att.log -g att_form -o "ipaddress='$f2'"  -o "username='$user'" -o "emailaddress='support@$f1'"  -o "companyname='$cname'" -o "comments='$f3'"  -o "phonenumber='$phone'" -o "title='$title'" -o "domainname='$f1'" -o "proxy_host=127.0.0.1"  -o "proxy_port=10090"
    

#     ./jaime.py -l jaime_att.log -g att_form -o "ipaddress='$f2'"  -o "username='$user'" -o "emailaddress='support@$f1'"  -o "companyname='$cname'" -o "comments='$f3'"  -o "phonenumber='$phone'" -o "title='$title'" -o "domainname='$f1'" -o "proxy_host=127.0.0.1"  -o "proxy_port=10090" >> unblock_activity_att.txt
    
    echo  mato el pid $ssh_pid que es el del tunel    
    skill -9 $ssh_pid
    exit 0 ;
done < ~/backoff-ATT.txt
