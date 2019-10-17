#!/usr/bin/python
#-*- coding:utf8 -*-
#####################################################
# > File Name: TranAnalysis.py
# > Author: zexl
# > Version: V1.01
# > Mail: zexllinlin@gmail.com 
# > Created Time: Fri 25 Jan 2019 09:50:56 AM CST
# > Usage:for RNAsdata analysis    
# > modify:20190313,runQc2 
#####################################################
import os
import re
import sys
import glob
import time
import gzip
from multiprocessing import Pool
from optparse import OptionParser
import subprocess


#def option():
Usage = "\'python %s --input file --outdir path\'" % sys.argv[0]
op = OptionParser()

op.add_option('-i','--input',dest = 'inputdir',action = "store",help = \
              "Determine dir of your rawdata,The default is the current path. ")
op.add_option('-o','--outdir',dest = 'outdir',action = "store",help = \
              "Determine your output dir,The default is the current path.")
op.add_option('-m','--miRNA',dest = 'RNAtype',action = "store_true",help = \
              "default RNA,if -m,work for miRNA")

(options, args) = op.parse_args()
inputdir = options.inputdir
outdir   = options.outdir
RNAtype    = options.RNAtype

if len(sys.argv)>1 and(sys.argv[1] == '--help' or sys.argv[1] == '-h'):
     print("Usage: %s"% Usage)
     print(op.print_help())
     sys.exit(1)

if not inputdir or not outdir:
     print('Message: you dont set outdir and inputdir,The default is the current path,Use -h or --help for more information')
     #sys.exit(1)
if not os.path.exists(outdir):
     os.system('mkdir %s'%outdir)

ScriptPath = sys.path[0]

if not inputdir:
    inputdir = os.getcwd()

if not outdir:
    outdir = os.getcwd()

def printtime(message, *args):
    if args:
        message = message % args
    print("[ " + time.strftime('%X') + " ] " + message)
    sys.stdout.flush()
    sys.stderr.flush()


def runcommand(command,description):
    if description != "" and description != " ":
        printtime(' ')
        printtime("Task: %s"% description)
    printtime('commands: %s'% command)
    stat = subprocess.call(command,shell=True)
    if stat != 0:
        printtime('ERROR: runcommand failed with status %d' % stat)
        sys.exit(1)


class RNAanalysis:

    def __init__(self,inp,out,Type):
        '''
        指定Type是mRNA和micRNA的方法不一样，
        Type:mRNA,micRNA
        '''
        self.inputdir = inp
        self.outdir = out
        self.Type = Type
        self.pool = 15
    def runQc(self,rtype):
        '''
        QC
        '''
        pool = Pool(self.pool)
        if rtype is 'QC':
            printtime("\n--------------------STARTS QC----------------------------")
            if not os.path.exists('%s/StepQC'% self.outdir):
                runcommand("mkdir %s/StepQC"%self.outdir,description='')
            qc_out = "%s/StepQC"% self.outdir 

            Files = glob.glob('%s/*.fastq.gz'% self.inputdir)
            if Files == []:
                printtime('ERROR: No fastq file in %s'% self.inputdir)
                sys.exit()
            for File in Files:
                prefix = '.'.join(re.split('/',File)[-1].split('.')[0:-2])
              
                if (os.path.exists('%s/StepQC/%s_fastqc.html'%(self.outdir,prefix)) and \
                    os.path.exists('%s/StepQC/%s_fastqc.zip'%(self.outdir,prefix))):
                    continue
                shell1 = 'fastqc -o %s %s'%(qc_out,File)
                pool.apply_async(runcommand,(shell1,"runQc:%s"% File))
            pool.close()
            pool.join()

            #if not os.path.exists('%s/multiqc_report.html'%qc_out):
            #    comm_mutqc = 'multiqc %s/StepQC -o %s/StepQC'% (self.outdir,self.outdir)
            #    runcommand(comm_mutqc,"StepQC:multiqc")
        if rtype is 'ReQC':
            printtime("\n---------------------STARTS ReQC--------------------------")
            if not os.path.exists('%s/StepReQC'% self.outdir):
                runcommand("mkdir %s/StepReQC"%self.outdir,description='')
            
            # 判断上一步是否生成文件
            qc_out = "%s/StepReQC"% self.outdir
            if self.Type == "mRNA":
            	Files = glob.glob('%s/StepUMI_trim/*.paired.fastq.gz'%self.outdir)
            if self.Type == "miRNA":
                Files = glob.glob('%s/StepUMI_trim/UMI_trimmed*.fastq'%self.outdir)
            if Files == []:
                printtime('ERROR: No UMI_trimmed*fastq file in %s/StepUMI_trim,'% self.outdir +\
                          ' Check your UMI_trim steps')
                sys.exit()

            for File in Files:
                if self.Type == "miRNA":
                    prefix = '.'.join(re.split('/',File)[-1].split('.')[0:-1])
                if self.Type == "mRNA":
                    prefix = '.'.join(re.split('/',File)[-1].split('.')[0:-2]) #RNA miRNA 的去接头结果文件不一样
                if (os.path.exists('%s/StepReQC/%s_fastqc.html'%(self.outdir,prefix)) and \
                    os.path.exists('%s/StepReQC/%s_fastqc.zip'%(self.outdir,prefix))):
                    continue
                shell1 = 'fastqc -o %s %s'%(qc_out,File)
                pool.apply_async(runcommand,(shell1,"runReQc:%s"% File))
            pool.close()
            pool.join()

           # if not os.path.exists('%s/multiqc_report.html'%qc_out):
           #     comm_mutqc = 'multiqc %s/StepReQC -o %s/StepReQC'% (self.outdir,self.outdir)
           #     runcommand(comm_mutqc,"StepReQC:multiqc")

    def runTrim(self):
        '''
        去接头，mRNA和micRNA的方法有所不同 
        '''
        printtime("\n---------------------UMI_trim for raw reads-----------------------")
        if not os.path.exists("%s/StepUMI_trim"% self.outdir):
            runcommand("mkdir %s/StepUMI_trim"% self.outdir,'')
        out_trim = "%s/StepUMI_trim"% self.outdir
        if self.Type == "mRNA":
            workfile = glob.glob("%s/*R1*.fastq.gz"% self.inputdir)
            useshell = "%s/RNAsequmiTrim.sh"% ScriptPath
            pool = Pool(10)
        if self.Type == "miRNA":
            workfile = glob.glob("%s/*R1_001.fastq.gz"% self.inputdir)
            useshell = "%s/miRNAumiTrim.sh"%ScriptPath
            pool = Pool(2)
        for gzfile in workfile:
            prefix = '.'.join(re.split('/',gzfile)[-1].split('.')[0:-2])
            if os.path.exists('%s/UMI_trimmed.Cutted.%s.fastq'%(out_trim,prefix)) and \
               os.path.exists('%s/Cutted.%s.fastq'%(out_trim,prefix)) and self.Type == "miRNA":
                continue
            if os.path.exists('%s/%s.paired.fastq.gz'%(out_trim,prefix)) and \
               os.path.exists('%s/%s.unpaired.fastq.gz'%(out_trim,prefix)) and \
               self.Type == "mRNA": 
                continue
               
            commands = "sh %s %s %s"%(useshell,gzfile,self.outdir) #mRNA
            pool.apply_async(runcommand, (commands,"UmiTrim:%s"% gzfile,))
        pool.close()
        pool.join()


    def STAR(self):   
        #pool = Pool(1) #STAR 耗内存较高，不能多个进程同时跑，最多两个进程
        printtime("----STARTS ----")
        if not os.path.exists('%s/StepAlign'% self.outdir):
             runcommand("mkdir %s/StepAlign"% self.outdir,'')

        qc_out = "%s/StepAlign"% self.outdir
        workfile = glob.glob("%s/StepUMI_trim/*R1*.paired.fastq.gz"% self.outdir)
        if workfile==[]:
            printtime("ERROR: No *R1_*.paired.fastq.gz file in %s/StepUMI_trim/"%self.outdir)
            sys.exit()

        for infile in workfile:
            commands = "sh %s/Align.sh %s %s"% (ScriptPath,infile,qc_out)
            runcommand(commands,"Align:%s"% infile)
            #pool.apply_async(runcommand, (commands,"Align:%s"% infile,))
        #pool.close()
        #pool.join()
    def bowtie(self):
        pool = Pool(self.pool)
        printtime("\n-----------------bowtie-------------------------")

        if not os.path.exists('%s/StepBowtie'% self.outdir):
            runcommand("mkdir %s/StepBowtie"% self.outdir,'')
        infiles = glob.glob("%s/StepUMI_trim/UMI_trimmed*R1*.fastq"% self.outdir)
        if infiles==[]:
            printtime("ERROR: No UniUMI_trimmed*fastq file in %s/StepUMI_trim/"%self.outdir)
            sys.exit()

        for infile in infiles:
            prefix = '.'.join(re.split('/',infile)[-1].split('.')[0:-1])
            if os.path.exists('%s/StepBowtie/%s.hairpin.sam'%(self.outdir,prefix)) and \
              os.path.exists('%s/StepBowtie/%s.mature.sam'%(self.outdir,prefix)):
                continue
            shell1 = 'bowtie2 -x %s/mature_human/mature_human \
             -U %s -S %s/StepBowtie/%s.mature.sam'%(ScriptPath,infile,self.outdir,prefix)
            shell2 = 'bowtie2 -x %s/hairpin_human/hairpin_human \
             -U %s -S %s/StepBowtie/%s.hairpin.sam'%(ScriptPath,infile,self.outdir,prefix)
            pool.apply_async(runcommand,(shell1,"Align:%s"% infile,))
            pool.apply_async(runcommand,(shell2,"Align:%s"% infile,))
        pool.close()
        pool.join()
    
    def miRNACount(self):

        pool = Pool(self.pool)
        printtime("\n-------------------Counts-----------------------")

        if not os.path.exists('%s/Step_CountMature'% self.outdir):
            runcommand("mkdir %s/Step_CountMature"% self.outdir,'')
        if not os.path.exists('%s/Step_CountHairpin'% self.outdir):
            runcommand("mkdir %s/Step_CountHairpin"% self.outdir,'')
        if not os.path.exists('%s/StepOut'% self.outdir):
            runcommand("mkdir %s/StepOut"% self.outdir,'')

        infiles = glob.glob('%s/StepBowtie/UMI_trimmed*.mature.sam'% self.outdir)
        if infiles == []:
            printtime("ERROR: No Sam file in %s/StepBowtie/, Check your bowtie step"%self.outdir)
            sys.exit()

        for infile in glob.glob('%s/StepBowtie/UMI_trimmed*.mature.sam'% self.outdir):
            hairpin = infile.replace('mature','hairpin')
            prefix_hairpin = '.'.join(re.split('/',hairpin)[-1].split('.')[0:-1])
            prefix_mature = '.'.join(re.split('/',infile)[-1].split('.')[0:-1])
            
            shell1 = "samtools view  -SF 4 -F 16 -q 30 %s |"%infile +\
                     "perl -alne \'{$h{$F[2]}++}END{print \"$_\\t$h{$_}\" foreach sort keys %h }\'"+\
                     "  > %s/Step_CountMature/%s.counts.txt"%(self.outdir,prefix_mature) 

            shell2 = "samtools view  -SF 4 -F 16 -q 30 %s |"%hairpin +\
                     "perl -alne \'{$h{$F[2]}++}END{print \"$_\\t$h{$_}\" foreach sort keys %h }\'"+\
                     "  > %s/Step_CountHairpin/%s.counts.txt"%(self.outdir,prefix_hairpin)
           
            runcommand(shell1,'Counts:%s'% infile)
            runcommand(shell2,'Counts:%s'% hairpin)
         
        printtime("----Merge Counts file---")
        shell3 = 'Rscript %s/mergeCount_miRNA.r \
                 %s/Step_CountMature/ ../StepOut/mature_'%(ScriptPath,self.outdir)
        shell4 = 'Rscript %s/mergeCount_miRNA.r \
                 %s/Step_CountHairpin/ ../StepOut/hairpin_'%(ScriptPath,self.outdir)
        runcommand(shell3,'merge Mature')
        runcommand(shell4,'merge Hairpin')
    def HTSeq(self):
        '''使用HTSeq对有参考基因组的转录组测序数据进行表达量分析'''
        pool = Pool(15)
        printtime("\n----------------STARTS HTSeq--------------------")
        if not os.path.exists('%s/StepHTseq'% self.outdir):
            runcommand("mkdir %s/StepHTseq"% self.outdir,'')

        infiles = glob.glob("%s/StepAlign/*Aligned.sortedByCoord.out.bam"%self.outdir)
        if infiles == []:
             printtime("ERROR: No Bam file in %s/StepAlign/,Check your Star step"%self.outdir)
             sys,exit()           

        for infile in infiles:
            filename = infile.strip().split("/")[-1]
            txtPrefix = filename.replace(".fastq.gz.Aligned.sortedByCoord.out.bam","")
            if os.path.exists('%s/StepHTseq/%s.txt'%(self.outdir,txtPrefix)):
                continue

            commands = ("htseq-count -f bam -r name"
                " -s no -a 10 -t exon -i gene_id -m union %s /media/adata/bioproject"
                "/refdata/genome/hg38/gencode.v28.annotation.gtf > %s/StepHTseq"
                "/%s.txt"%(infile,self.outdir,txtPrefix))
            pool.apply_async(runcommand, (commands,"HTseq:%s"% infile,))
        pool.close()
        pool.join()
    def mRNAmerge(self):
        
        printtime("\n----------------STARTS Merge-------------------")
        if not os.path.exists('%s/StepOut'% self.outdir):
            runcommand("mkdir %s/StepOut"% self.outdir,'')

        infiles = glob.glob('%s/StepHTseq/*txt'% self.outdir)
        if infiles == []:
            printtime("ERROR: No Count file in %s/StepHTseq/, Check your mRNAHTSeq step"%self.outdir)
            sys.exit()

        os.system("Rscript %s/mergeCount.r \
                 %s/StepHTseq/ ../StepOut/"%(ScriptPath,self.outdir))
        printtime("\n----------------STARTS convert_geneID-------------------")
        os.system("Rscript %s/ENSG_convert_geneID.R \
                 %s/StepOut/"% (ScriptPath,self.outdir))
        printtime("----end----")
def main():
    if RNAtype is True:
        analysis = RNAanalysis(inputdir,outdir,'miRNA')   
        analysis.runQc('QC')
        analysis.runTrim()
        analysis.runQc('ReQC')
        analysis.bowtie()
        analysis.miRNACount()
    else:
        analysis = RNAanalysis(inputdir,outdir,'mRNA')
        analysis.runQc('QC')
        analysis.runTrim()
        analysis.runQc('ReQC')
        analysis.STAR()
        analysis.HTSeq()
        analysis.mRNAmerge()

if __name__=='__main__':
    main()
