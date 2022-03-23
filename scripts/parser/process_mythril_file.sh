filename=${1}
rm -rf ${filename/.json/_bak.json}
error_lines=$(grep -nv "{\"error\": null" ${filename}  | awk -F: '{print $1}' | wc -l)
total_lines=$(cat ${filename} | wc -l)
print_lines=$((total_lines-error_lines))
tail -n ${print_lines} ${filename} >> ${filename/.json/_bak.json}
