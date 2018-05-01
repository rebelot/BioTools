LOGFILE=$1
TIME=$(grep -m 1 ' time = "[[:alnum:]]*\.[[:alnum:]]' $LOGFILE | awk '{print $3}' | sed 's/"//g')
TIME=$(python -c "print($TIME/1000)")

echo

while [[ "$(tail -n 1 $LOGFILE | awk '{ print $1 }')" =~ "Chemical" ]]; do
    ct="$(tail -n 1 $LOGFILE | awk '{ print $3 }')"
    v="$(tail -n 1 $LOGFILE | awk '{ print $8 }')"
    ctns=$(python -c "print($ct/1000)")
    comp=$(python -c "print(100*$ctns/$TIME)")
    sec_left=$(python -c "print(round(24*3600 * ($TIME - $ctns)/$v ))")
    eta=$(printf '%0.2dd:%0.2dh:%0.2dm:%0.2ds\n' $(($sec_left/86400)) $(($sec_left/3600%24)) $(($sec_left%3600/60)) $(($sec_left%60)))
    
    printf "\e[0K\rCompletion: %.2f of $TIME ns (%.2f%%)  @ $v ns/day     ETA: %15s" $ctns $comp $eta
    sleep 1
done

