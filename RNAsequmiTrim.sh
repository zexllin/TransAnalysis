R1=$1
outdir=$2
echo "begin to trim ${R1}"
adapterLength=10
trimmomatic=/opt/comprogram/biogram/trimmomatic/0.38/trimmomatic-0.38.jar
adapter=/opt/comprogram/biogram/trimmomatic/0.38/adapters/TruSeq3-PE.fa:2:30:10
R2=${R1//R1_001.fastq.gz/R2_001.fastq.gz}
R1File=`basename ${R1}`
R1paired=${R1File//.fastq.gz/.paired.fastq.gz}
R1unpaired=${R1File//.fastq.gz/.unpaired.fastq.gz}
R2File=`basename ${R2}`
R2paired=${R2File//.fastq.gz/.paired.fastq.gz}
R2unpaired=${R2File//.fastq.gz/.unpaired.fastq.gz}

java -jar ${trimmomatic} PE -phred33 -trimlog LogTrim.log ${R1} ${R2} \
  ${outdir}/StepUMI_trim/${R1paired} ${outdir}/StepUMI_trim/${R1unpaired} \
  ${outdir}/StepUMI_trim/${R2paired} ${outdir}/StepUMI_trim/${R2unpaired} \
  ILLUMINACLIP:${adapter} \
  SLIDINGWINDOW:5:20 LEADING:5 HEADCROP:${adapterLength} TRAILING:5 MINLEN:50
echo "finish to trim ${R1}"
