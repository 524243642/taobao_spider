# mall_spider

#### 项目介绍
mall spider

#### 软件架构
软件架构说明


#### 安装教程

1. mac安装python3.7，windows安装python3.6
2. pip 安装相关依赖
2. windows or mac os x

#### 使用说明
mac os x
1. 创建目录并修改写入权限/var/log/tiger/
2. 运行deploy下脚本即可

windows7 sp1
1. 创建目录并修改写入权限c:/log/tiger/
2. 配置当前项目环境变量
3. 运行deploy下脚本即可

windows server 2008 R2
1. 创建目录并修改写入权限c:/log/tiger/
2. 配置当前项目环境变量
3. 运行deploy下脚本即可

eq.2008 r2上mysql 5.7sqlalchemy连接db方式为mysqlconnector不然会报中文错误warning

#### windows运行环境

##### 1.netframework4.5.2

https://www.microsoft.com/en-us/download/details.aspx?id=42642

##### 2.mysql connector(选择对应python版本)

https://dev.mysql.com/downloads/connector/python/

##### 3.vc_redist_x64

https://www.microsoft.com/en-us/download/details.aspx?id=48145

##### 4.visualcppbuildtools_full

安装environment/win下的文件或者下载安装 

http://go.microsoft.com/fwlink/?LinkId=691126

##### 5.安装pip依赖（设置阿里pip源提升依赖包下载速度）

在文件夹路径上输入%AppData%，新建pip文件夹，新建pip.ini文件，文件内容如下
```
[global]  
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
```
或者直接执行

pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com

#### 参与贡献

1. Fork 本项目
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request