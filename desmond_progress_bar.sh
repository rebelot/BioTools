LOGFILE=$1
TIME=$2

echo

while [[ "$(tail -n 1 $LOGFILE | awk '{ print $1 }')" =~ "Chemical" ]]; do
    ct="$(tail -n 1 $LOGFILE | awk '{ print $3 }')"
    v="$(tail -n 1 $LOGFILE | awk '{ print $8 }')"
    perh=$(python -c "print($v/24.0)")
    comp=$(python -c "print(100*$ct/$TIME)")
    diff=$(python -c "print($TIME - $ct)")
    seta=$(python -c "print(round(3600*($diff/1000.)/$perh))")
    eta=$(printf '%dh:%dm:%ds\n' $(($seta/3600)) $(($seta%3600/60)) $(($seta%60)))
    
    printf "\e[0K\rCompletion: %.2f%%       ETA: %11s" $comp $eta
    sleep 1
done

