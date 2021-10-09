# qtapp2.0

#### 介绍

PySide6.1.1

#### 软件架构

C/S

#### 安装教程

#### 换源

1 路径下新建文件: C:\Users\<用户>\pip\pip.ini
2 写入:
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host = mirrors.aliyun.com

#### 环境

[VSCode]
.vscode -> settings.json
"python.linting.flake8Enabled": true, 
"python.linting.enabled": false

1 pip install --upgrade pip
2 pip install requests
3 pip install PySide6
4 pip install cx_Freeze
5 pip install intensio-obfuscator
6 更新 pip install --upgrade ***

#### 打包

1调试打包 cxfreeze -c main.py --target-dir dist
2发布打包 cxfreeze -c ./qtbox/main.py --target-dir ./BitBox --base-name=win32gui --include-files="./qtbox/source"

#### 使用说明

运行 main.py

#### 参与贡献

#### 特技

#### 未实现功能

#### BUG
