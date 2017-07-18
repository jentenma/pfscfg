#!/bin/bash
#
# time dd  if=/dev/dpump0 of=/dev/null count=100000000 bs=512 2>/dev/null &
# 
# Assumes drives are starting at "c" and there are 24 of them
#
#    dd if=/dev/dpump0 count=1 bs=512 2>/dev/null | od -t x8 -A n
#    time dd  if=/dev/dpump0 of=/dev/null count=10000000 bs=512 2>/dev/null &
#
#      --------  Examples of how to look for errors --------
#
#    If a drive encounters an error the "dd" will
#    stop and the "used_count" for the corresponding dpump will stop incrementing.
#
#    Finding error information if a drive stops....
#    dmesg | grep "\[$drive\]" | grep -i error
#    
#    Finding a drive that has stopped....
#    for f in `seq 0 23`;do cat /sys/class/dpadmin/dpump$f/used_count;done
# 
#    Get a list of drives for a particular host. This tool is highly dependent 
#    on parsing the hostname to 
#    for drive in `lsscsi | awk '{print $NF}'`;do sginfo -s $drive ;done > /tmp/xxx.txt
#    cat /tmp/xxx.txt | sort | awk '{print $NF}' | while read CMD; do if [ "$LCMD" !=  "$CMD" ];then echo $CMD; fi;LCMD=$CMD;done | wc
#    
#    lsscsi -w | grep 0x | sort -k3 | awk '{print $(NF-1)}' > /tmp/wwids.txt
#


#debugging on
#set -x

usage ()
{
echo -e -n "\033[1;32m"
cat <<EOF
 Usage:
     $0 -n <node index> 

 Options:
     n   Node index starting from 1-n
EOF
echo -e "\033[0m"
}


node_index_start=1

while getopts ":n:s:" opt; do
    case $opt in
	s)
	    node_index_start=${OPTARG}
	    ;;
	n)
	    number_of_nodes=${OPTARG}
	    ;;
	\?)
	    usage
	    exit 1
	    ;;
	:)
	    echo "Option -$OPTARG requires an argument." >&2
	    usage
	    exit 1
	    ;;
    esac
done

PWD=$(pwd)

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

wwid_list=`lsscsi -w | grep 0x | sort -k3 | awk '{print $(NF-1)}'`

block_devices=()

i=$((node_index_start-1))
last_index=`echo $wwid_list | wc -w`
last_index=$((last_index-1))
my_drives=`seq $i $number_of_nodes $last_index`

#echo $my_drives

j=0
declare -a wwid_array

for wwid in $wwid_list
do
	wwid_array[$j]=$wwid 
	#echo "** $wwid ${wwid_array[j]}"
	j=$((j+1))
done

j=0
for mi in $my_drives
do
	#echo "$mi ${wwid_array[$mi]}"
	sgdev=`lsscsi -w | grep ${wwid_array[$mi]} | awk '{print $NF}'`
	block_devices[${j}]=$sgdev
	j=$((j+1))
done

echo ${block_devices[*]}

STATUS=$?

exit $STATUS

