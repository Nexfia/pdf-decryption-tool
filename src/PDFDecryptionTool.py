from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import *
import threading
import pikepdf
from pikepdf import _cpphelpers
import os
from ttkthemes import *
from tkinter import messagebox

def __selectInputPath():
    if isPDFFile.get()==0:
        inputPath=askdirectory(parent=root, mustexist=True)
        inputEntry.delete(0, END)
        inputEntry.insert(0, inputPath)
    elif isPDFFile.get()==1:
        inputPath=askopenfilename(title="Select PDF file", filetypes=(("pdf files", "*.pdf"),("PDF files", "*.PDF")), parent=root)
        inputEntry.delete(0, END)
        inputEntry.insert(0, inputPath)

def selectInputPath():
    T=threading.Thread(target=__selectInputPath())
    T.start()

def __clearInputPath():
    inputEntry.delete(0, END)

def clearInputPath():
    T=threading.Thread(target=__clearInputPath())
    T.start()

def __selectOutputPath():
    outputPath=askdirectory(parent=root, mustexist=True)
    outputEntry.delete(0, END)
    outputEntry.insert(0, outputPath)

def selectOutputPath():
    T=threading.Thread(target=__selectOutputPath())
    T.start()

def makeOutFilePath(outFile):
    if os.path.exists(outFile)==False:
            os.makedirs(outFile)

def __jiemi():
    inFile = inputPath.get()
    outFile = outputPath.get()

    parentinFile = ''
    if inFile!='' and outFile!='': 
        #判断目标路径和输出路径是否一致，一致则询问是否覆盖源文件
        overwriteFlag=''
        if isPDFFile.get()==0:
            if inFile==outFile:
                overwriteFlag=messagebox.askyesno(message="覆盖文件",detail="目标路径和输出路径一致\n是否允许覆盖源文件?")
        elif isPDFFile.get()==1:
            parentinFile = os.path.dirname(inFile)
            if parentinFile==outFile:
                overwriteFlag=messagebox.askyesno(message="覆盖文件",detail="目标路径所在文件夹与出路径一致\n是否允许覆盖源文件?")
        if overwriteFlag==False:
            messagebox.showinfo(message='提示', detail='请重新选择输出路径！')

        #判断是否为单个pdf(0表明不是)且目标路径时候存在，都是则对整个文件夹的pdf文件进行解密
        if isPDFFile.get()==0 and os.path.exists(inFile)==True and (overwriteFlag==True or inFile!=outFile):
            filelist = os.listdir(inFile)
            count=0
            jiemiInfo=''
            try:
                if len(filelist)>0:
                    for file in filelist:
                        if file.endswith(".pdf")and ("~$" not in file):#当文件为pdf文件且不是临时文件
                            filePath = inFile + "/"+ file
                            makeOutFilePath(outFile) #判断输出目录是否存在，不存在则创建
                            tips="正在转换第"+str(count+1)+"个文件"
                            updateStatusLable(tips)
                            with pikepdf.open(filePath, allow_overwriting_input=overwriteFlag) as pdf:
                                num_pages = len(pdf.pages)
                                del pdf.pages[-1]
                                pdf.save(outFile + "/"+ file)
                            count+=1
                    if count==0:
                        messagebox.showinfo(message='提示', detail='未检测到pdf文件！\n（不包含子文件夹）')
                    else:
                        messagebox.showinfo(message='提示', detail='已完成')
                        updateStatusLable("状态：空闲中")
                else:
                    messagebox.showinfo(message='提示', detail='目标路径为空文件夹\n请重新选择路径')
            except Exception as e:
                messagebox.showerror(message='错误', detail=e)    
        elif isPDFFile.get()==1 and os.path.exists(inFile)==True and (overwriteFlag==True or inFile!=parentinFile): #判断是否为单个pdf，1表明是
            try:    
                
                with pikepdf.open(inFile,allow_overwriting_input=overwriteFlag) as pdf:
                        num_pages = len(pdf.pages)
                        del pdf.pages[-1]
                        fileName=os.path.basename(inFile)
                        updateStatusLable("正在转换:"+fileName)
                        makeOutFilePath(outFile)
                        pdf.save(outFile + "/"+ fileName)
                        messagebox.showinfo(message='提示', detail='已完成')
                updateStatusLable("状态：空闲中")
            except ValueError:
                messagebox.showerror(message='错误', detail='无法写入文件!\n请检查文件是否已被其他软件打开！')  
            except pikepdf._qpdf.PdfError:
                messagebox.showerror(message='错误', detail='未能被识别的pdf文件！\n请确认pdf文件完整性！')         
            except pikepdf._qpdf.PasswordError:
                messagebox.showerror(message='错误', detail='暂不支持解除用户密码！')         
            except Exception as e:
                messagebox.showerror(message='错误', detail=e)         
        elif os.path.exists(inFile)==False:
            messagebox.showerror(message='错误', detail='目标路径不存在！请重新选择')
    elif inFile=='' and outFile!='':
        messagebox.showinfo(message='提示', detail='请选择目标路径')
    elif outFile=='' and inFile!='':
        messagebox.showinfo(message='提示', detail='请选择输出路径')
    elif inFile=='' and outFile=='' :
        messagebox.showinfo(message='提示', detail='请选择目标路径和输出路径')

def updateStatusLable(info):
    statusLable.config(text = info)
    statusLable.update()

def jiemi():
    T=threading.Thread(target=__jiemi())
    T.start()
 
def aboutInfo(event):
    root.withdraw() 
    global aboutWindow
    aboutWindow=Toplevel(root)
    aboutWindow.title("关于")
    aboutWidth=460
    aboutHeight=200
    aboutLeft = (screenWidth - aboutWidth) / 2
    aboutTop = (screenHeight - aboutHeight) / 2
    aboutWindow.focus()
    aboutWindow.geometry("%dx%d+%d+%d" % (aboutWidth, aboutHeight, aboutLeft, aboutTop))
    aboutWindow.resizable(False,False)
    
    aboutText=Text(aboutWindow, width=200)

    aboutText.tag_config('link', foreground='#646464')

    aboutText.insert('1.0', "本软件用于解除pdf文件所有者密码\n")
    aboutText.insert('2.0',"从而解除编辑、复制等限制\n")
    aboutText.insert('3.0',"作者：Nexfia\n")
    aboutText.insert('4.0',"项目主页：\n")
    aboutText.insert('5.0',"https://gitee.com/nexfia/pdf-decryption-tool\n", 'link')
    aboutText.insert('6.0',"感谢以下项目：\n")
    aboutText.insert('7.0',"pikepdf，tkinter，ttkthemes\n", 'link')
    aboutText.insert('8.0',"图标来自Ikonate:\n")
    aboutText.insert('9.0',"https://ikonate.com/", 'link')

    aboutText.grid(row = 0, column = 0, columnspan=2)
    #设置窗口管理器接到关闭前的动作
    aboutWindow.protocol("WM_DELETE_WINDOW", t_close_handler)

def t_close_handler():
    root.deiconify()
    aboutWindow.destroy()
    

if __name__ == "__main__":
    #theme="arc" 使用名为arc的主题
    # toplevel=True 设置子窗口的背景颜色与主窗口一致 themebg=True 设置主窗口背景颜色为主题颜色
    root = ThemedTk(theme="arc", toplevel=True, themebg=True) 
    root.title("PDF解密工具")
    inputPath = StringVar()
    outputPath = StringVar()
    isPDFFile = IntVar()

    # 获取显示区域的宽度和高度
    screenWidth = root.winfo_screenwidth()  
    screenHeight = root.winfo_screenheight() 
    #设置窗口大小
    width = 370  # 设定窗口宽度
    height = 150  # 设定窗口高度
    left = (screenWidth - width) / 2
    top = (screenHeight - height) / 2
    root.geometry("%dx%d+%d+%d" % (width, height, left, top))
    #禁止用户调整窗口大小
    root.resizable(False,False)
    #设置图标
    root.iconphoto(False, PhotoImage(file='/opt/apps/nexfia.PDFDecryptionTool/images/logo/icon.png'))
    
    inputLabel=Label(root,text = "目标路径:")
    inputLabel.grid(row = 0, column = 0)
    inputEntry=Entry(root, textvariable = inputPath)
    inputEntry.grid(row = 0, column = 1)
    inputButton=Button(root, text = "路径选择", command = selectInputPath)
    inputButton.grid(row = 0, column = 2)

    outputLabel=Label(root,text = "输出路径:")
    outputLabel.grid(row = 1, column = 0)
    outputEntry=Entry(root, textvariable = outputPath)
    outputEntry.grid(row = 1, column = 1)
    outputButton=Button(root, text = "路径选择", command = selectOutputPath)
    outputButton.grid(row = 1, column = 2)

    jiemiButton=Button(root, text = "解密", command = jiemi)
    jiemiButton.grid(row = 2, column = 2)

    #是否是单个PDF文件，默认不是
    isPDFFile.set(0)
    setOnePDFFile = Checkbutton(root, text="转换单个PDF文件", variable=isPDFFile, command=clearInputPath)
    setOnePDFFile.grid(row = 2, column = 0,columnspan=2)

    statusLable=Label(root,text = "状态：空闲中")
    statusLable['font'] = "TkSmallCaptionFont"
    statusLable.grid(row = 3, column = 0, columnspan=2)

    aboutLable=Label(root,text = "关于")
    aboutLable['font'] = "TkSmallCaptionFont"
    aboutLable.grid(row = 3, column = 2)
    aboutLable.bind('<Button-1>', aboutInfo)

    root.mainloop()