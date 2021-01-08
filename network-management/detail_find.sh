if [ $# -ne 1 ]; then
    echo "usage: detail_find.sh \$(filename)"
    exit
fi
start_time=$(date +%s)

nmap -oA "$1" -iL $1 -O --osscan-guess --traceroute -T4

end_time=$(date +%s)
cost_time=$[ $end_time-$start_time ]
echo "nmap cost time is $(($cost_time/60))min $(($cost_time%60))s"