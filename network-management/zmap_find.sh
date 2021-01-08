#! /bin/bash
path=`cd $(dirname $0); pwd`
cd $path
echo $path
DATE=$(date +%d-%k)
echo $DATE
mkdir $DATE
cd $DATE

networks="$path/networks"
ports="$path/ports"


port_name=`awk '{print $1}' $ports`
port_num=(`awk '{print $2}' $ports`)

for line in `cat $networks`
do
	subnet=`echo $line | awk -F '/' '{print $1}'`
	mkdir $subnet
	cd $subnet	
	echo $subnet
	cnt=0
	for name in $port_name
	do
		port=${port_num[$cnt]}
		echo $name
		zmap $line -p $port -o $port --output-fields "saddr" --output-filter="success = 1 || success = 0" -r 1800
		cnt=`expr $cnt + 1`
	done
	cd ..
done
