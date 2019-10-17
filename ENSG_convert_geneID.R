rm(list=ls())
gc()
args=commandArgs(T)
path = args[1]
library(org.Hs.eg.db)
library(clusterProfiler)
# 转化symbol id
change_symbolid <- function(data){
        genes = rownames(data)
        # 获取表达量数据
        genes <- gsub(pattern = "[.]\\S+",replacement = "",x = genes)
        symboldata = bitr(genes, fromType="ENSEMBL", toType=c("ENTREZID","SYMBOL"), OrgDb="org.Hs.eg.db")
	#构建一个布尔向量，索引  
        index <- duplicated(symboldata$SYMBOL)
        #筛选非重复的数据 
        symboldata <- symboldata[!index,]
        #rownames(symboldata) <- symboldata$ENSEMBL
        symbolid <- c()
        match_index <- match(genes,symboldata$ENSEMBL)  
        for(i in 1:length(match_index)){
                if(is.na(match_index[i])){symbolid=cbind(symbolid,'')}  
                else{symbolid=cbind(symbolid,symboldata$SYMBOL[match_index[i]])}
        }
	symbolid = t(symbolid)
	count <- cbind(symbolid,data[,-1])
	index = which(count$symbolid!='')
	count <- count[index,]
	return(count)
        
}
# 合并重复基因（累计）
get_count <- function(count){
	geneidfactor<-factor(count$symbolid)
	tep=count[,2:ncol(count)]
	gene_exp_matrix<-apply(tep,2,function(x) tapply(x,geneidfactor,sum))
	rownames(gene_exp_matrix)<-levels(geneidfactor)
	return(gene_exp_matrix)
}
setwd(path)
# 读取原始文件
rna_count = read.table('rnaseq_count.txt',sep='\t',header=T)
rownames(rna_count) = rna_count$gene_id

count <- change_symbolid(rna_count)
new_count <- get_count(count)
save(file='rna-seq-count-symbol.RData',new_count)
new_count_w <- cbind(rownames(new_count),new_count)
write.table(file='rna-seq-count-symbol.txt',new_count_w,sep='\t',row.names=F,col.names=T)
