### 0.4版本更新说明

修复了0.3版本的单文件覆盖源文件判断bug

### 0.3版本更新说明

1.完善了程序逻辑。

2.增加了异常处理。

3.使用主题进行美化。

4.增加了“关于”页面



### 软件截图

![image-20210430210208796](./docImage/appWIn.png)

![image-20210430210208796](./docImage/about.png)



### 安装说明

安装前请务必使用命令

```bash
sudo dpkg --purge nexfia.PDFDecryptionTool
```

将旧版本先自行删除



### 功能说明

只能解除PDF文件的所有者权限的密码，用户密码解不了。

说人话就是，只能解除你能打开但编辑和复制需要密码的PDF文件。

那种打开就要密码的解不了，除非暴力破解。



### 原理

设置了所有者权限的PDF文件的内容实质上并未加密，使用 **pikepdf**  读取置了所有者权限的PDF文件，并将读取的内容保存为新的PDF文件即可解除加密，可以愉快的编辑和复制文档内容了。



### 警告

1.解密PDF文档前请确定你有权编辑及移除这个文件的密码。

使用本程序造成的任何责任由使用者自己承担。

2.deb的打包是野包，升级时请务必安装安装说明先卸载上一个版本



### 准备工作

pip3安装命令

```shell
sudo apt-get install python3-pip
```

pikepdf模块安装命令

``` shell
pip3 install pikepdf
```



### 程序运行

Windows

``` shell
python PDFDecryptionTool.py 
```

Linux

```shell
python3 PDFDecryptionTool.py 
```



### 程序说明

GUI框架：Tkinter

PDF读写模块：pikepdf 

使用主题：ttkthemes 

https://github.com/TkinterEP/ttkthemes/tree/master/ttkthemes



### 题外话

本程序将不再更新，因为使用tkinter写GUI实在太操蛋了

可能会用pyqt5进行重写，或者直接做一个pdf工具箱。

因为好像没有再deepin见到好用的pdf处理软件。

有知道好用的可以推荐下。



### 写在最后

#### Q：0.2版本哪去了？

A：在你心里。

#### Q：使用pyinstaller打包时需要注意什么？

A：需要注意直接使用

```bash
pyinstaller -Dw PDFDecryptionTool.py 
```

进行打包是不会将**/src/images**内的图片资源文件打包进去的。

#### 解决方法一：

你使用打包命令打包一次生成了**PDFDecryptionTool.spec**文件后，在**PDFDecryptionTool.spec**文件中的data参数里加上('images','images')

![image-20210430210208796](./docImage/data参数.png)

保存，运行命令

```bash
pyinstaller PDFDecryptionTool.spec
```

即可。

#### 解决方法二：

将**/src/images**文件夹直接复制到**/src/dist/PDFDecryptionTool**中。



#### Q：我尝试用pyinstaller打包为什么文件这么大？

A：

额，因为把太多没用的东西打包进来了，建立个专用的虚拟环境﻿就好了。

Pipenv安装与使用可以看这篇文章：https://www.return520.com/posts/18616/

首先安装pipenv

```shell
pip3 install pipenv
```

使用pipenv创建一个虚拟环境（3.7是我Python版本，你可以换成你自己的，注意python和版本号3.7之间有一个空格）

```shell
pipenv --python 3.7
```

安装pikepdf模块

``` shell
pip install pikepdf
```

安装pyinstaller模块，pyinstaller的使用可以看这篇文章：https://blog.csdn.net/weixin_39000819/article/details/80942423

``` shell
pip install pyinstaller
```

进入源代码的py文件所在目录

``` shell
cd /xxx/xxx/xxx/xxx
```

使用pyinstaller -D xxx.py进行打包，Windows使用pyinstaller -Dw xxx.py

``` shell
pyinstaller -D PDFDecryptionTool.py 
pyinstaller -Dw PDFDecryptionTool.py 
```

进入到  /xxx/xxx/xxx/xxx/dist/PDFDecryptionTool 目录，找到PDFDecryptionTool文件执行即可。

Linux建议在终端执行，可以看到报错信息。

``` shell
./xxx/xxx/xxx/xxx/dist/PDFDecryptionTool/PDFDecryptionTool
```

