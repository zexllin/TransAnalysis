#!/usr/bin/env Rscript
##
## Try to combine count of single sample.
##
## usage: Rscript mergeCount.r inputdir outputdir
##
args=commandArgs(T)
inputdir = args[1]
outputdir = args[2]
path = inputdir
setwd(path)
file = dir('./','*.txt')
i <- 0
for(filename in file){
  count = read.table(filename)
  name = strsplit(filename,split='.txt')
  rna_seq_count_tep <- as.data.frame(count)
  colnames(rna_seq_count_tep) <- c('miRNA_name', name)
  if (i==0){
      rna_seq_count = rna_seq_count_tep
      i = i+1
  }
  else {
    rna_seq_count <- merge(rna_seq_count, rna_seq_count_tep, all=T, by.x = 'miRNA_name', by.y = 'miRNA_name')
  }
}

write.table(rna_seq_count,file = paste0(outputdir,"rnaseq_count.txt"),sep="\t",row.names=FALSE)
