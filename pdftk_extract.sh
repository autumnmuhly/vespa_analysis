
data_file=${1}
phase=${2}
for pdffile in `ls $data_file`; do
    # echo pdffile $pdffile
    pdftk $pdffile dump_data_fields | grep FieldValue

    pdftk "$pdffile" dump_data_fields | awk '/^FieldName:/ {name=$2} /^FieldValue:/ {if ($2 != "" && name ~ /^BoxName_[12]_/) {sub(/^BoxName_[12]_/, "", name); print name}}' >> pdffile_list_$phase
    
    # pdftk $pdffile dump_data_fields | grep FieldValue -B2 | grep BoxName_1 -A2 | grep FieldName | sed -e 's/\&quot\;//g' -e 's/BoxName_1_//g' | awk '{print $2}' >> pdffile_list
    # pdftk $pdffile dump_data_fields | grep FieldValue -B2 | grep BoxName_2 -A2 | grep FieldName | sed -e 's/\&quot\;//g' -e 's/BoxName_2_//g' | awk '{print $2}' >> pdffile_list

    # echo ---
    # cat "pdffile_list"
    # echo ---

done