file=$1
outDir=$2
filename=`basename ${file} .gz`
gzip -cd ${file} | grep AACTGTAGGCACCATCAAT -B 1 -A 2 --no-group-separator | sed 's/AACTGTAGGCACCATCAAT/\t/' > ${outDir}/StepUMI_trim/Cutted.${filename}
/home/appuser/anaconda2/envs/py3/bin/python /home/zhaoxl/miRNAanalysis/TranAnalysis/after_cut.py ${outDir}/StepUMI_trim/Cutted.${filename} > ${outDir}/StepUMI_trim/UMI_trimmed.Cutted.${filename}
