R1=$1
outdir=$2
gtffile=/media/adata/bioproject/refdata/genome/hg38/gencode.v28.annotation.gtf
STAR_index=/data/biopro/rawdata/rnaseq/00.GC/INDEX_150/
R2=${R1//R1_001.paired.fastq.gz/R2_001.paired.fastq.gz}
R1File=`basename ${R1}`
prefix=${R1File//.R1_001.paired.fastq.gz/}
echo "begin to align ${R1}"
/opt/comprogram/biogram/star/2.4.2/bin/Linux_x86_64/STAR \
  --genomeDir ${STAR_index} \
  --sjdbGTFfile ${gtffile} \
  --limitBAMsortRAM 40000000000 \
  --runThreadN 12 \
  --limitIObufferSize 500000000 \
  --outFilterType BySJout \
  --outFilterMismatchNmax 999 \
  --outFilterMismatchNoverLmax 0.04 \
  --outFilterMultimapNmax 20 \
  --outFilterMatchNminOverLread 0.66 \
  --outFilterIntronMotifs None \
  --outSJfilterReads All \
  --outSAMtype BAM SortedByCoordinate \
  --outSAMunmapped Within \
  --outSAMstrandField intronMotif \
  --outSAMattrRGline ID:${prefix} SM:${prefix} PL:Illumina \
  --alignSJoverhangMin 8 \
  --alignSJDBoverhangMin 1 \
  --alignIntronMin 20 \
  --alignIntronMax 1000000 \
  --alignMatesGapMax 1000000 \
  --chimSegmentMin 15 \
  --chimJunctionOverhangMin 15 \
  --chimScoreMin 0 \
  --chimScoreDropMax 20 \
  --chimScoreSeparation 10 \
  --chimScoreJunctionNonGTAG -1 \
  --quantMode TranscriptomeSAM \
  --quantTranscriptomeBan IndelSoftclipSingleend \
  --outReadsUnmapped Fastx \
  --readFilesIn ${R1} ${R2} \
  --readFilesCommand zcat \
  --outFileNamePrefix ${outdir}/${prefix}.
echo "finish to anign ${R1}"


