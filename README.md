# TransAnalysis
配置需要的环境

1 安装 htseq-count \
2 安装star 比对软件 

使用方法
将TransAnalysis.py连接到/usr/bin,或者/usr/local/bin,等等配置了系统环境变量的目录下，或者你自己的目录/home/zhaoxl/.local/bin/，/home/zhaoxl/.local/bin/只能当前用户为自己的时候可以用。

$ sudo ln -s /home/zhaoxl/TransAnalysis.py  /home/zhaoxl/.local/bin/TransAnalysis

TransAnalysis -i <input path> -o <output path>

