#!/bin/bash
outdir="outsmi"
if ! [ -d $outdir ]; then mkdir $outdir; fi
rm outsmi/*
while IFS="" read -r line
do 
    #echo $line 
    echo $line | awk -F '\t' '{print $2 $1}' > output.csv
    filename=$(awk '{print $2}' output.csv)
    echo $filename
    mv output.csv $outdir/$filename.smi
done < input_smi/input_template.csv
