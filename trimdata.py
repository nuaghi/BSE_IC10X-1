import os
import datetime
import subprocess
import sys
import pandas as pd
import re

def nowtime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')

def onetwentieth(i):
    if i//1000000>0:
        return 1000000
    elif i//100000>0:
        return 100000
    elif i//10000>0:
        return 10000
    else:
        return i
def alterContent(file):
    file_data = ""
    tempfile=file+".tmp"
    totalnum=int(subprocess.getoutput("wc -l %s | awk '{print $1}'" % file))
    otnum=onetwentieth(totalnum)
    i=0
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            i+=1
            line = line.replace(" ","")
            line = re.sub(r'\*+','-2',line)
            line = re.sub(",0.0*,",",0,",line)
            line = re.sub("\.0*$","",line)
            line = re.sub("\.0*,",",",line)
            line = re.sub(',$','',line)
            line = re.sub('ces$','ces,',line)
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
            if line == "i,t1,mx,mx2,tbx,kw,kw2,ndt,ces,":
                print(nowtime(),i,"WARNING:",line)
    if os.path.exists(tempfile):
        os.rename(tempfile,file)

def init():
    if os.path.exists("/Files/git/data/"):
        dataFolderLocation="/Files/git/data/"
        print(nowtime()+"OS: Ubuntu")
    elif os.path.exists("/Users/nuaghi/Files/BSE_workbench/data/"):
        dataFolderLocation="/Users/nuaghi/Files/BSE_workbench/data/"
        print(nowtime()+"OS: MacOS")
    elif os.path.exists("/data2/wgy/git/data/"):
        dataFolderLocation="/data2/wgy/git/data/"
        print(nowtime()+"OS: Ubuntu228")
    elif os.path.exists("/mnt/d/Files/BSE_workbench/data/"):
        dataFolderLocation=("/mnt/d/Files/BSE_workbench/data/")
        print(nowtime()+"OS: WinUbuntu")
    elif os.path.exists("/Files/BSE/data/"):
        dataFolderLocation=("/Files/BSE/data/")
        print(nowtime()+"OS: BaoGuoMa")
    elif os.path.exists("/Files/BSE_workbench/data/"):
        dataFolderLocation=("/Files/BSE_workbench/data/")
        print(nowtime()+"OS: GraduateRoom")
    else:
        dataFolderLocation="./data/"
        print(nowtime()+"ERROR: [OS: Unknown] Try to find the data directory.")
    rdclogfile=dataFolderLocation+"rdc.num"
    if os.path.exists(rdclogfile):
        with open(rdclogfile, 'r', encoding='utf-8') as f:
            last_line = f.readlines()[-1]
            runtime=last_line.split('|')[0].strip()
            runtimelist=[runtime,runtime.split("_")[0]+"_"+str(int(runtime.split("_")[1])-1),runtime.split("_")[0]+"_"+str(int(runtime.split("_")[1])-2)]
        totalFormationCount=int(subprocess.getoutput("grep "+runtime+" "+dataFolderLocation+"rdc.num | awk -F '[,:]' '{print $2}'"))
        alterContent(dataFolderLocation+"rdc.num")
        for i in runtimelist:
            for j in ["","s","ss"]:
                if os.path.exists(dataFolderLocation+"N"+i+j+".csv"):
                    try:
                        alterContent(dataFolderLocation+"N"+i+j+".csv")
                    except Exception as e:
                        print(nowtime()+"WARN: [N"+i+j+".csv]: "+e)
                    try:
                        os.rename(dataFolderLocation+"N"+i+j+".csv", dataFolderLocation+"N"+i+"_"+str(totalFormationCount)+j+".csv")
                    except Exception as e:
                        print(nowtime()+"WARN: [N"+i+j+".csv]: "+e)
                else:
                    print(nowtime()+"WARNING: "+dataFolderLocation+"N"+i+j+".csv NOT FOUND.")
    else:
        print("ERROR: File Not Found!!!")
        sys.exit(0)
init()
