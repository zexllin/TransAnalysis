mature=$1
hairpin=$2
out=$3
filename=`basename ${mature}`
samtools view  -SF 4 -F 16 -q 30 ${mature} |perl -alne '{$h{$F[2]}++}END{print "$_\t$h{$_}" foreach sort keys %h }'  > ${out}/Step_CountMature/${filename}.counts.txt
echo $filename
filename=`basename ${hairpin}`
samtools view  -SF 4 -F 16 -q 30 ${hairpin} |perl -alne '{$h{$F[2]}++}END{print "$_\t$h{$_}" foreach sort keys %h }'  > ${out}/Step_CountHairpin/${filename}.counts.txt

