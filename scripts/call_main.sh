#!/bin/bash
parallel_processes=${1}
choice=${2} # Choice Options= all, majority_all, majority_unique

files=$(cat ../results/sample_results.txt)
# files=(./0x711256406c2e9072fbaee5b67d5a893f66a3e707_ext.sol)



file_seq_no=1
j=1
rm temp_*

if [[ ${choice} != 'all' && ${choice} != 'majority_all' && ${choice} != 'majority_unique' ]]; then
    echo "Choice is Wrong"
    exit
fi
for file in ${files[@]}
do
      if [[ ${j} -lt ${parallel_processes} ]]; then
        python3 main.py ${file_seq_no} ${file} ${choice} > temp_${j} &
        ((j++))
      else
        wait
        python3 main.py ${file_seq_no} ${file} ${choice} > temp_${j}
        wait
        j=1
        for (( i = 1; i <= ${parallel_processes}; i++ ))
        do
          cat temp_${i}
          rm temp_${i}
        done
      fi
      ((file_seq_no++))
done

wait
cat temp_*
rm temp_*
