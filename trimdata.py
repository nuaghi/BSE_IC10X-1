import os
import datetime
import subprocess
import sys

def nowtime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')

def onetwentieth(i):
    if i//1000000>0:
        return 1000000
    else:
        j =  i//500*100
        if j>=1:
            return j
        else:
            return 1

def alter(file,old_str,new_str):
    file_data = ""
    tempfile=file+".tmp"
    totalnum=int(subprocess.getoutput("wc -l %s | awk '{print $1}'" % file))
    otnum=onetwentieth(totalnum)
    i=0
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            i+=1
            if old_str in line:
                line = line.replace(old_str,new_str)
            if i == 1:
                file_data += line
            #检查数据合法性: tbx 是否<=0
            if i > 1 and float(line.split(",")[3].strip()) > 0:
                file_data += line
                if i%otnum==0 or i%totalnum==0:
                    print(nowtime()+"Trim blank of file: "+file+": "+str(i)+"/"+str(totalnum)+", "+"percent: {:.2%}".format(i/totalnum))
                    if len(file_data) > 0:
                        with open(tempfile,"a",encoding="utf-8") as f:
                            f.write(file_data)
                    else:
                        print(nowtime()+"ERROR: Empty Data")
                        sys.exit(0)
                    file_data = ""
            else:
                print(nowtime()+"Warning data: "+str(i)+" - "+line.split(",")[3].strip())
                continue
    os.rename(tempfile,file)

def init():
    if os.path.exists("/home/hp/Documents/git/data/"):
        dataFolderLocation="/home/hp/Documents/git/data/"
        print(nowtime()+"OS: Ubuntu")
    elif os.path.exists("/Users/nuaghi/Documents/git/data/"):
        dataFolderLocation="/Users/nuaghi/Documents/git/data/"
        print(nowtime()+"OS: MacOS")
    else:
        dataFolderLocation="./"
        print(nowtime()+"FATAL ERROR: [OS: Unknown] Exit.")
        exit(0)
    rdclogfile=dataFolderLocation+"rdc.num"
    if os.path.exists(rdclogfile):
        with open(rdclogfile, 'r', encoding='utf-8') as f:
            last_line = f.readlines()[-1]
            runtime=last_line.split('|')[0].strip()
        alter(dataFolderLocation+"N"+runtime+".csv", " ", "")
    else:
        print("ERROR: File Not Found!!!")
        sys.exit(0)

init()