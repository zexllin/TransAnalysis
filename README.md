# TransAnalysis
TransAnalysis 用于RNAseq下机数据质控，去接头，比对及表达定量，结果为miRNA或者mRNA表达丰度矩阵。


配置需要的环境

1 安装 htseq-count \
2 安装star 比对软件 \
3 去接头软件 \
4 下机数据质控软件

使用方法

$ python TransAnalysis.py -i \<input path\> -o \<output path\>

将TransAnalysis.py连接到/usr/bin,或者/usr/local/bin,等等配置了系统环境变量的目录下，或者你自己的目录/home/zhaoxl/.local/bin/，/home/zhaoxl/.local/bin/只能当前用户为自己的时候可以用。

$ sudo ln -s /home/zhaoxl/TransAnalysis.py  /home/zhaoxl/.local/bin/TransAnalysis

TransAnalysis -i \<input path\> -o \<output path\>

