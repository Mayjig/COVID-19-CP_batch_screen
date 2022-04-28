#!/bin/bash
rm sdf3d/*
rm mol3d/*
rm TMP*
rm *atc
if [ -s rdkit_test.txt ]; then rm rdkit_test.txt; fi
if [ -s gaff_test.txt ]; then rm gaff_test.txt; fi

./read_file.bat

for mol in $(ls outsmi/*)
do
	filename=$(basename -- "$mol")
	filename="${filename%.*}"
	obabel $mol -O sdf3d/${filename}.sdf --gen3d
	obabel $mol -O mol3d/${filename}.mol2 --gen3d
done

# convert gaff
for mol in $(ls mol3d/*)
do
        filename=$(basename -- "$mol");
        filename="${filename%.*}";
         ## turn off the acdoctor mode: -dr no
        antechamber -fi mol2 -fo mol2 -i $mol -o $mol -dr no
        molprop3 -i $mol -o ${filename}.atc -f mol2 -p ~/src/mp/mp_entropy2.dat -c 2
        rm TMP1
        molprop3 -i ${filename}.atc -f atc -o TMP1 -p ~/src/mp/mp_entropy2.dat -c 4 -d 0
	cat TMP1 >> gaff_test.txt
done

## convert rdkit
source /home2/bej22/anaconda3/bin/activate my-rdkit-env
for mol in $(ls sdf3d/*)
do
        filename=$(basename -- "$mol")
        filename="${filename%.*}"
	echo $filename
       python3.7 read_sdf.py $mol
        ./sd_extract_field -i sdf3d/${filename}_desc.sdf -d 0 -f feature -o TMP2 -l 0
	cat TMP2 >> rdkit_test.txt
done
