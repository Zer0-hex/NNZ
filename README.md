# NNZ

> 重保的告警数量还可以，写写工具，看看S12，慢慢长夜很快就过去了。

## 简介

一款模块化工具，可以为命令行工具提供通用GUI界面。让你拥有自己喜欢的工具包。不论是在虚拟机里！还是装在U盘里！都可即插即用！

技术栈：Python + tkinter + toml 

另外，作为一个Linuxer，我还是很喜欢终端界面的🤭

## [使用说明](Wiki.md)

## 几个好处

1. 在肾透厕视或者攻防演练的时候，打开各种终端窗口，然后整个电脑乱的一批，很让人烦躁，NNZ可以减轻你在这方面的痛苦。

2. 对于小白来说，很多工具不会用，不好学，有了前辈写好的配置文件，拿来可以直接梭哈了。

3. 有一天你不小心运行了一个exe，发现中招了，这个时候电脑不干净了，你左思右想还是选择了重装系统，TA可以让你一小时恢复工作状态。

## 校验

```
PS C:\> certutil -hashfile nnz.exe [md5, SHA1, SHA256]
MD5 的 dist/nnz.exe 哈希:
8396f27b74a5af53baf58d46e78675c9
SHA1 的 dist/nnz.exe 哈希:
5b3333889f742b67aee9f35ac0b6b459547db67d
SHA256 的 dist/nnz.exe 哈希:
d5673d6ac5b7c2e4f19ce3bc3b760057bbad78744f24a2fbbca17b395060b7cb
```

## 构建方法

```
python -m pip install pip --upgrade
pip install -r requirements.txt
build.bat
```

## 主要功能

* 启动器 (把其他有GUI界面的工具集成一下) ~随便加了几个工具，没别的意思~

![image](assets/runs.png)

* 渗透小工具 (现在还什么都没有，牛奶会有的，面包也会有的)

![image](assets/simple_tools.png)

* 命令行工具 (通用GUI界面，只需要写一份极其简单的配置文件即可，摆脱了在命令行里面切换各种目录的繁琐。)

![image](assets/terminal_tools.png)
