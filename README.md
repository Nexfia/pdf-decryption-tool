###  说明

只能解除PDF文件的所有者权限的密码，用户密码解不了。

说人话就是，只能解除你能打开但编辑和复制需要密码的PDF文件。

那种打开就要密码的解不了，除非暴力破解。



### 原理

设置了所有者权限的PDF文件的内容实质上并未加密，使用 **pikepdf**  读取置了所有者权限的PDF文件，并将读取的内容保存为新的PDF文件即可解除加密，可以愉快的编辑和复制文档内容了。



### 警告

解密PDF文档前请确定你有权编辑及移除这个文件的密码。

使用本程序造成的任何责任由使用者自己承担。



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

程序主要逻辑：

判断单文件复选框setOnePDFFile是否被勾选

--isPDFFile.get()的值为0表示没有没有被勾选

----选择目标文件夹，既要修改的PDF文档所在的文件夹

----点击“解密”按钮，程序会读取目标文件夹的文件列表，选择pdf文件进行解密，并保存到选择的输出路径。

----解密过程中会不断更新  **statusLable**  标签的内容说明解密到第几个文件。

--isPDFFile.get()的值为1表示没有被勾选

----选择目标文件，既要修改的PDF文档

----点击“解密”按钮，程序会读取目标文件进行解密，并保存到选择的输出路径。

--默认是0不勾选






### 写在最后

Q：为什么不打包好一个deb或者exe？

A：

我也想打包好，可惜能力不够。我用Pyinstaller打包成二进制文件的时候都出问题了。

打包过程没问题不过程序运行的时候，显示找不到pikepdf模块，整了快一天了，各种方法试过了，搞不定。

所以只能直接用源码运行了。

谁有法子的可以交流下。

![输入图片说明](https://images.gitee.com/uploads/images/2021/0422/110713_7b0864ef_7352405.png "image-20210421234842285.png")

![输入图片说明](https://images.gitee.com/uploads/images/2021/0422/110726_bfb43e9a_7352405.png "image-20210422001606402.png")

Q：为什么文件选择器这么丑？而且这么难用？

A：

Linux中Tkinter不知道调用的是哪个文件选择器，我本来想尝试通过调用深度文件管理器的文件选择器来获取路径的。可是查了半天找不到法子，我也很无奈。我太菜了QAQ

Windows的使用了ttk，界面是系统风格还可以啦。

Q：为什么程序容易出问题？

A：没写异常处理。。。

Q：我尝试用pyinstaller打包为什么文件这么大？

A：

额，因为把太多没用的东西打包进来了，建立个专用的虚拟环境﻿就好了。

Pipenv安装与使用可以看这篇文章：https://www.return520.com/posts/18616/

首先安装pipenv

```shell
pip3 install pipenv
```

使用pipenv创建一个虚拟环境（3.7是我Python版本，你可以换成你自己的）

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

