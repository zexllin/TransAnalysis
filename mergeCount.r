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
filename = strsplit(file,split='.txt')
i = 0
for(name in file){
  count = read.table(name)
  line = strsplit(name,split='.txt')
  if (i==0){
      rna_seq_count = as.data.frame(count)
      colnames(rna_seq_count) = c('gene_id',line)
      i = i+1
  }
  else {
    rna_seq_count[line[[1]]] = count$V2
  }
}
# del the last 5 rows, which is not ENSG ID
rna_seq_count = rna_seq_count[1:(length(rna_seq_count[,1])-5),]
write.table(rna_seq_count,file = paste0(outputdir,"rnaseq_count.txt"),sep="\t",row.names=FALSE)
