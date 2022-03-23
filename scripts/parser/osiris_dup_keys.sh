#!/bin/bash
key=${1}
file=${2}


is_dup_key=$(grep "\"${key}\":{" ${file} | wc -l)

if [[ ${is_dup_key} -gt 1 ]]; then
    line_numbers=$(grep -nri "\"${key}\":" ${file} |  awk -F':' '{print $1}')
    i=1
    for l in ${line_numbers[@]}
    do
       sed -i ''${l}'s/'${key}'/'${key}'-'${i}'/g' ${file} 
       ((i++))
    done
fi



