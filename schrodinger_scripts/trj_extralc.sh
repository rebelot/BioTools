#!/bin/bash

if [ "$1" = "-h" ]; then
    echo usage: extralc IN.cms IN_trj extract_asl align_asl center_asl
    exit
fi

in_cms=$1
in_trj=$2
extr_asl=$3
al_asl=$4
c_asl=$5

echo "extracting \"$extr_asl\" subsystem from ${in_cms%.*}..."
$SCHRODINGER/run trj_extract_subsystem.py "$in_cms" extracted -t "$in_trj" -asl "$extr_asl"
echo "extracted-out.cms extracted_trj written"
echo
echo "aligning \"$al_asl\" subsystem..."
$SCHRODINGER/run trj_align.py extracted-out.cms extracted_trj aligned -asl "$al_asl"
echo "aligned-out.cms aligned_trj written"
echo   
echo "centering \"$c_asl\" subsystem..."
$SCHRODINGER/run trj_center.py aligned-out.cms extralc -t aligned_trj -asl "$c_asl"
echo "extralc-out.cms extralc_trj written"
echo

echo "removing
$(find . -name 'extracted*')"
echo "proceed? y/n"
read input
[[ $input = "y" ]] && rm -rf extracted* 

echo
echo "removing
$(find . -name 'aligned*')"
echo "proceed? y/n"
read input
[[ $input = "y" ]] && rm -rf aligned* 

