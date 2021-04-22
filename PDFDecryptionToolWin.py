from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import *
import threading
import pikepdf
import os
import ctypes
 
def __selectInputPath():
    if isPDFFile.get()==0:
        inputPath=askdirectory(parent=root, mustexist=True)
        inputEntry.delete(0, END)
        inputEntry.insert(0, inputPath)
    elif isPDFFile.get()==1:
        inputPath=askopenfilename(title="Select PDF file", filetypes=(("pdf files", "*.pdf"),("PDF files", "*.PDF")))
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

def __jiemi():
    inFile = inputPath.get()
    outFile = outputPath.get()
    if inFile!='' and outFile!='':
        if isPDFFile.get()==0:
            filelist = os.listdir(inFile)
            count=0
            k=len(filelist)
            for file in filelist:
                if file.endswith(".pdf")and ("~$" not in file):#当文件为pdf文件且不是临时文件
                    filePath = inFile + "/"+ file
                    
                    tips="正在转换第"+str(count+1)+"个文件"
                    statusLable.config(text = tips)
                    statusLable.update()
                    with pikepdf.open(filePath) as pdf:
                        num_pages = len(pdf.pages)
                        del pdf.pages[-1]
                        pdf.save(outFile + "/"+ file)
                count+=1
            updateStatusLable("已完成")
        elif isPDFFile.get()==1:
            with pikepdf.open(inFile) as pdf:
                    num_pages = len(pdf.pages)
                    del pdf.pages[-1]
                    fileName=os.path.basename(inFile)
                    print(fileName)
                    print(type(fileName))
                    pdf.save(outFile + "/"+ fileName)
                    updateStatusLable("已完成")
    elif inFile=='' and outFile!='':
        updateStatusLable("请选择目标路径")
    elif outFile=='' and inFile!='':
        updateStatusLable("请选择输出路径")
    elif inFile=='' and outFile=='' :
        updateStatusLable("请选择目标路径和输出路径")

def updateStatusLable(info):
    statusLable.config(text = info)
    statusLable.update()

def jiemi():
    T=threading.Thread(target=__jiemi())
    T.start()

if __name__ == "__main__":
    root = Tk()
    root.title("PDF解密工具")
    inputPath = StringVar()
    outputPath = StringVar()
    isPDFFile = IntVar()
    
    #告诉操作系统使用程序自身的dpi适配
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    #获取屏幕的缩放因子
    ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
    #设置程序缩放
    root.tk.call('tk', 'scaling', ScaleFactor/75)
    # 获取显示区域的宽度和高度
    screenWidth = root.winfo_screenwidth()  
    screenHeight = root.winfo_screenheight() 
    #设置窗口大小
    width = 358  # 设定窗口宽度
    height = 115  # 设定窗口高度
    left = (screenWidth - width) / 2
    top = (screenHeight - height) / 2
    root.geometry("%dx%d+%d+%d" % (width, height, left, top))
    #禁止用户调整窗口大小
    root.resizable(False,False)
    
    
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
    statusLable.grid(row = 3, column = 0, columnspan=3)

    root.mainloop()