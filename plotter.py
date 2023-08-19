import pandas as pd
import subprocess
from alive_progress import alive_bar
import functions
import sys
import gc
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os

#演化过程分类：ST:Stable mass Transfer, CE:Common Envelope
evolist=["Stable Mass Transfer","Common Envelope","Other Channels"]
dataInfo=[[],[],[]]

#定义文件名, 参数或者日志文件rdc.num中取
LocationList=[["/Files/git/data/","Ubuntu"],["/Users/nuaghi/Files/BSE_workbench/data/","MacOS"],["/data2/wgy/git/data/","Ubuntu228"],["/Files/data/","Ubuntu125-BaoGuoMa"],["/mnt/d/Files/BSE_workbench/data/","WinUbuntu"],["/Files/BSE_workbench/data/","lenovo@GranduateRoom"]]
for i in LocationList:
    if os.path.exists(i[0]):
        dataFolderLocation=i[0]
        print(functions.nowtime()+"OS: "+i[1])
        break
dataRunTime = sys.argv[1] if len(sys.argv) > 1 else subprocess.getoutput("grep '^20' "+dataFolderLocation+"/rdc.num | tail -n 1 | awk -F '|' '{print $1}'")
dataRunTime = [(datetime.datetime.strptime(dataRunTime,"%Y%m%d_%H%M%S")-datetime.timedelta(hours=0, minutes=0, seconds=2)).strftime('%Y%m%d_%H%M%S'),(datetime.datetime.strptime(dataRunTime,"%Y%m%d_%H%M%S")-datetime.timedelta(hours=0, minutes=0, seconds=1)).strftime('%Y%m%d_%H%M%S'),dataRunTime]

#functions的locationCheck函数返回文件夹路径、文件路径、生成的html文件夹路径
dataFolderLocation,dataFileLocation,htmlFolderLocation=functions.locationCheck(dataRunTime)

#各参数整理为数组，之后做对比
dataParas=[subprocess.getoutput("grep "+dataRunTime[i]+" "+dataFolderLocation+"rdc.num |awk -F '[,:]' '{for(i=1;i<=NF;i++)if(i%2==0) print $(i-1),\":\",$i}' | tr \"\n\" \",\"").split(",") for i in range(len(dataRunTime))]
print(functions.nowtime()+str(dataRunTime)+" Stage 1: Initializating.")

#每个数据文件在rdc.num记录中要求生成的总数量，也即popbin.f文件中nm1数值
totalFormationCount=int(subprocess.getoutput("grep "+dataRunTime[0]+" "+dataFolderLocation+"rdc.num | awk -F '[,:]' '{print $2}'"))

#读取带s的小文件，并去重
list1=pd.read_csv(dataFileLocation[1][0],usecols=["i","t1","ces"],dtype={'i':int,"ces":int},on_bad_lines="skip").drop_duplicates()
print(functions.nowtime()+str(dataRunTime[0])+" Stage 1.1: Data loaded: dataFileName: "+dataFileLocation[1][0]+", Counts: "+(str(len(set(list1["i"])))))
list2=pd.read_csv(dataFileLocation[1][1],usecols=["i","t1","ces"],dtype={'i':int,"ces":int},on_bad_lines="skip").drop_duplicates()
print(functions.nowtime()+str(dataRunTime[1])+" Stage 1.2: Data loaded: dataFileName: "+dataFileLocation[1][1]+", Counts: "+(str(len(set(list2["i"])))))
list3=pd.read_csv(dataFileLocation[1][2],usecols=["i","t1","ces"],dtype={'i':int,"ces":int},on_bad_lines="skip").drop_duplicates()
print(functions.nowtime()+str(dataRunTime[2])+" Stage 1.3: Data loaded: dataFileName: "+dataFileLocation[1][2]+", Counts: "+(str(len(set(list3["i"])))))

#判断演化过程进行分类  ["SMT+SMT","SMT+CE","CE+SMT","Double-Core CE","CE+CE"]，ces即ce的次数，0：两次都是ST过程，没有调用comenv函数，2：两次都是CE过程。1:中间三个在下方有更细致的分类。
datalist = [ [  list(set(list1[(list1["ces"]==0)&(list1["t1"]>0)]["i"])),[],[]],
             [  list(set(list2[(list2["ces"]==0)&(list2["t1"]>0)]["i"])),[],[]],
             [  list(set(list3[(list3["ces"]==0)&(list3["t1"]>0)]["i"])),[],[]]
            ]

numListSetDataI=[len(list(set(list1["i"]))),len(list(set(list2["i"]))),len(list(set(list3["i"])))]
print(functions.nowtime()+str(dataRunTime)+" Stage 1.4: Data loaded, classifying...")

listCesEQ1 = [ list(set(list1[list1["ces"]==1]["i"])),
               list(set(list2[list2["ces"]==1]["i"])),
               list(set(list3[list3["ces"]==1]["i"]))]

#读取大文件， 目的：从演化过程中经历什么样的公共包层演化来进行分类。i对应的是不同alphaCE下的情况，SMT仅取一个就可以。
for i in range(len(dataRunTime)):
    data=pd.read_csv(dataFileLocation[0][i],usecols=["i","kw","kw2","ces"],dtype={'i':int,'kw':int,'kw2':int,"ces":int},on_bad_lines="skip").drop_duplicates()
    with alive_bar(len(listCesEQ1[i]), ctrl_c=False, title=dataRunTime[i]+f': Classifying: ') as bar:
        for k in range(len(listCesEQ1[i])):
            dataIkwkw2Ces=np.array(data[data["i"]==listCesEQ1[i][k]]).tolist()
            for j in range(len(dataIkwkw2Ces)):
                if int(dataIkwkw2Ces[j][3])==1 and int(dataIkwkw2Ces[j-1][3])==0:
                    #datalist[1].SMT+CE:   致密星kstar未发生变化，WR星的kstar发生变化，所以是WR星的前身星膨胀到洛溪瓣并进入CE演化得到的，即CE后直接生成目标源
                    if dataIkwkw2Ces[j-1][1] == dataIkwkw2Ces[j][1] and dataIkwkw2Ces[j-1][2] != dataIkwkw2Ces[j][2] and dataIkwkw2Ces[j][1] in [13,14] and dataIkwkw2Ces[j][2] in [7,8,9]:
                        datalist[i][1].append(dataIkwkw2Ces[j-1][0])
                    else:
                        datalist[i][2].append(dataIkwkw2Ces[j-1][0])
                    break
            bar()
del list1,list2,list3,data,dataIkwkw2Ces
gc.collect()

#在rdc.num文件中筛选出实际有多少对双星的演化
effectiveFormationCount=[int(subprocess.getoutput("grep "+dataRunTime[i]+" "+dataFolderLocation+"rdc.num | awk -F '[,:]' '{print $2-$4}'")) for i in range(len(dataRunTime))]

#定义输出文件名
htmlFileLocation=htmlFolderLocation+"index.html"

#已得到以不同演化通道分类的两个datalist，准备小文件数据开始画图。
#对数据进行筛选：演化时间大于0且小于100Myrs、WR星质量大于2倍太阳质量(一般都在5个太阳质量以上)、轨道周期大于0(数据的合理性)
print(functions.nowtime()+str(dataRunTime)+" Stage 1.*: Loading data successfully. Filting data: "+str(dataFileLocation[1][0]))
data1=pd.read_csv(dataFileLocation[1][0],usecols=["i","t1","mx","mx2","tbx","kw","kw2","ndt","ces"],dtype={'i':int,'t1':float,'mx':float,'mx2':float,'tbx':float,'kw':int,'kw2':int,'ndt':"float32","ces":int},on_bad_lines="skip")
data1=data1[(data1["t1"]>0)&(data1["t1"]<=100)&(data1["mx2"]>2)&(data1["mx"]>0)&(data1["ndt"]>0)&(data1["tbx"]>0)&(data1["tbx"]<20000)]
print(functions.nowtime()+str(dataRunTime)+" Stage 1.*: Filting data: "+str(dataFileLocation[1][1]))
data2=pd.read_csv(dataFileLocation[1][1],usecols=["i","t1","mx","mx2","tbx","kw","kw2","ndt","ces"],dtype={'i':int,'t1':float,'mx':float,'mx2':float,'tbx':float,'kw':int,'kw2':int,'ndt':"float32","ces":int},on_bad_lines="skip")
data2=data2[(data2["t1"]>0)&(data2["t1"]<=100)&(data2["mx2"]>2)&(data2["mx"]>0)&(data2["ndt"]>0)&(data2["tbx"]>0)&(data2["tbx"]<20000)]
print(functions.nowtime()+str(dataRunTime)+" Stage 1.*: Filting data: "+str(dataFileLocation[1][2]))
data3=pd.read_csv(dataFileLocation[1][2],usecols=["i","t1","mx","mx2","tbx","kw","kw2","ndt","ces"],dtype={'i':int,'t1':float,'mx':float,'mx2':float,'tbx':float,'kw':int,'kw2':int,'ndt':"float32","ces":int},on_bad_lines="skip")
data3=data3[(data3["t1"]>0)&(data3["t1"]<=100)&(data3["mx2"]>2)&(data3["mx"]>0)&(data3["ndt"]>0)&(data3["tbx"]>0)&(data3["tbx"]<20000)]

#不同演化通道分类的数据统计
def NumAnalytics2(data,list):
    NumAnalyticsCount,k=[],0
    for j in list:
        NumAnalyticsCount.append([[],[],[],[],[],[],[],[],[],[]])
        NumAnalyticsCount[k][0]=len(j)
        NumAnalyticsCount[k][1]=sum(data[data["i"].isin(j)]["ndt"])
        NumAnalyticsCount[k][2]=min(data[data["i"].isin(j)]["t1"],default="-")
        NumAnalyticsCount[k][3]=max(data[data["i"].isin(j)]["t1"],default="-")
        NumAnalyticsCount[k][4]=min(data[data["i"].isin(j)]["mx"],default="-")
        NumAnalyticsCount[k][5]=max(data[data["i"].isin(j)]["mx"],default="-")
        NumAnalyticsCount[k][6]=min(data[data["i"].isin(j)]["mx2"],default="-")
        NumAnalyticsCount[k][7]=max(data[data["i"].isin(j)]["mx2"],default="-")
        NumAnalyticsCount[k][8]=min(data[data["i"].isin(j)]["tbx"],default="-")
        NumAnalyticsCount[k][9]=max(data[data["i"].isin(j)]["tbx"],default="-")
        k+=1
    gc.collect()
    return NumAnalyticsCount

#画图程序
def evolutionList(f,data1,data2,data3,dataInfo):
    #演化时间-WR星质量
    Num=1
    htmlContent=""

    #演化时间-WR星质量 - 致密星分类：中子星/黑洞
    functions.plotAgeMassDonorKw([data1, data2, data3], [str(Num)+"-AgeMassNSBH", str(Num)+"-AgeMassNSBH"], htmlFolderLocation, [dataInfo[0][5], dataInfo[1][5], dataInfo[2][5]])
    htmlContent+="<img src='"+str(Num)+"-AgeMassNSBH"+".png'>"
    data1=data1[data1["kw"]==14]
    data2=data2[data2["kw"]==14]
    data3=data3[data3["kw"]==14]


    #演化时间-WR星质量 - 演化过程分类：ST/CE
    Num+=1

    functions.plotAgeMassDonorSingle(data1, str(Num)+"-AgeMassSingle",htmlFolderLocation, dataInfo[0][5],datalist[0])
    htmlContent+="<br /><img src='"+str(Num)+"-AgeMassSingle"+".png'>"
    Num+=1
    functions.plotAgeMassDonor([data1, data2, data3], str(Num)+"-AgeMass",htmlFolderLocation, [dataInfo[0][5], dataInfo[1][5], dataInfo[2][5]],[datalist[0],datalist[1],datalist[2]])
    htmlContent+="<br /><img src='"+str(Num)+"-AgeMass"+".png'>"

    data1=data1[data1["t1"]<=10]
    data2=data2[data2["t1"]<=10]
    data3=data3[data3["t1"]<=10]

    #WR星质量-lg轨道周期
    Num+=1
    functions.plotMassDonorLogPeriodSingle(data1,str(Num)+"-MassPeriodSingle",htmlFolderLocation, dataInfo[0][5],datalist[0])
    htmlContent+="<br /><img src='"+str(Num)+"-MassPeriodSingle.png'>"
    Num+=1
    functions.plotMassDonorLogPeriod([data1, data2, data3], str(Num)+"-MassPeriod", htmlFolderLocation, [dataInfo[0][5], dataInfo[1][5], dataInfo[2][5]], [datalist[0],datalist[1], datalist[2]], agesign = 1)
    htmlContent+="<br /><img src='"+str(Num)+"-MassPeriod.png'>"
    htmlContent+="</div><hr /><div><p>4 WR星质量-BH质量</p>"


    #WR星质量-致密星质量
    Num+=1
    functions.plotMDonorAccretorSingle(data1, str(Num)+"-MassMass2Single", htmlFolderLocation, dataInfo[0][5], datalist[0], agesign = 1)
    htmlContent+="<img src='"+str(Num)+"-MassMass2Single.png'>"

    Num+=1
    functions.plotMDonorAccretor([data1, data2, data3], str(Num)+"-MassMass2", htmlFolderLocation, [dataInfo[0][5], dataInfo[1][5], dataInfo[2][5]], [datalist[0], datalist[1], datalist[2]], agesign = 1)
    htmlContent+="<img src='"+str(Num)+"-MassMass2.png'>"

    #WR星质量分布图
    Num+=1
    functions.plotDistribution([data1, data2, data3], str(Num)+"-Mass2Distribution", htmlFolderLocation, [dataInfo[0][5],dataInfo[1][5],dataInfo[2][5]], [datalist[0],datalist[1],datalist[2]])
    htmlContent+="<img src='"+str(Num)+"-Mass2Distribution.png'>"
    #致密星质量分布图
    Num+=1
    functions.plotCODistribution([data1, data2, data3], str(Num)+"-MassDistribution", htmlFolderLocation, [dataInfo[0][5],dataInfo[1][5],dataInfo[2][5]], [datalist[0],datalist[1],datalist[2]])
    htmlContent+="<img src='"+str(Num)+"-MassDistribution.png'>"
    f.write(htmlContent)
    del htmlContent,Num
    gc.collect()

def entrance():
    print(functions.nowtime()+str(dataRunTime)+" Stage 2.1: Data Analytics")
    dataReturn=numListSetDataI
    print(functions.nowtime()+str(dataRunTime)+" Stage 3.1: NumAnalytics")
    dataNakeHeStarCount2=[NumAnalytics2(data1,datalist[0]),NumAnalytics2(data2,datalist[1]),NumAnalytics2(data3,datalist[2])]
    htmlContent="<html><head><meta charset='UTF-8'><link href='http://www.sucaijishi.com/favicon.ico' rel='shortcut icon' type='image/ico'><title>"+str(totalFormationCount)+"-"+dataRunTime[0]+"-"+dataRunTime[1]+"</title><style>table,tr,td,th{font-size:22px;border:1px solid #000;padding:0 2px;white-space:pre-line;}div{padding:1px}p{font-size:25px}</style><script type='text/javascript' src='./jquery.js'></script></head><body>\n"
    htmlContent+="<table><tr><td>DataSet</td><td><b>Age &isin; (0,100)Myrs & Massaccretion > 0 & MassDonor > 2M<sub>sun</sub> & Period > 0 & separation > 0 & N > 0 & kstar1 = 14(BH) & kstar2 = (7,8,9)(Naked He Star)<b></td></tr></table><div><div class='summary'>\n<table><tr>"

    #演化过程的分类统计
    for i in ["运行时间","Total","Effective","Real","Z","SFR","α<sub>CE</sub>","SNtype","bwind","hewind","ceflag","tflag","ifflag","wdflag","bhflag","nsflag","mxns","sigma","beta","xi","acc2","epsnov","eddfac","gamma"]:
        htmlContent+="<th>"+i+"</th>"
    for i in range(len(dataRunTime)):
        htmlContent+="</tr><tr><td>"+dataRunTime[i]+"</b></td><td>"+str(dataParas[i][0].split(":")[1])+"</td><td>"+str(effectiveFormationCount[i])+"</td>"
        dataInfo[i].extend([dataRunTime[i],int(dataParas[i][0].split(":")[1].strip()),effectiveFormationCount[i]])
        htmlContent+="<td>"+str(dataReturn[i])+"</td>"
        for j in range(2,22):
            dataInfo[i].extend([round(float(dataParas[i][j].split(":")[1]),4)])
            htmlContent+="<td>"+str(round(float(dataParas[i][j].split(":")[1]),4))+"</td>\n"

    #以演化通道为分类的数量统计
    htmlContent+="</tr></table>\n<table><tr><th>演化过程</th><th>α<sub>CE</sub></th><th>数量/比例</th><th>总数量(Ri*dtt)</th><th>Age范围[Myrs]</th><th>致密星质量范围[Msun]</th><th>伴星质量范围[Msun]</th><th>轨道周期范围[d]</th>"
    for i in range(len(evolist)):
        htmlContent+="</tr><tr><th rowspan=4>"+evolist[i]+"</th>"
        for k in range(len(dataRunTime)):
            htmlContent+="</tr><tr><th>"+dataRunTime[k]+"<br />(α<sub>CE</sub>:"+str(round(float(dataParas[k][4].split(":")[1]),4))+")</th>"
            htmlContent+="<td style='width: max-content;'><span style='float:left'>"+str(dataNakeHeStarCount2[k][i][0])+" / "+str(dataReturn[k])+" = {:.2%}".format(dataNakeHeStarCount2[k][i][0]/dataReturn[k])+"</span> , <span style='float:right'>"+str(dataNakeHeStarCount2[k][i][0])+" / "+str(effectiveFormationCount[k])+" = {:.2%}".format(dataNakeHeStarCount2[k][i][0]/effectiveFormationCount[k])+"</span></td><td>"+str(dataNakeHeStarCount2[k][i][1])+"</td>"
            for j in [2,4,6,8]:
                if dataNakeHeStarCount2[k][i][j] == "-" or dataNakeHeStarCount2[k][i][j+1] == "-":
                    htmlContent+="<td><p style='margin:0'>min: "+str(dataNakeHeStarCount2[k][i][j])+"</p><p style='float:right;margin:0'>MAX: "+str(dataNakeHeStarCount2[k][i][j+1])+"</p></td>"
                else:
                    htmlContent+="<td><p style='margin:0'>min: "+str(round(dataNakeHeStarCount2[k][i][j],4))+"</p><p style='float:right;margin:0'>MAX: "+str(round(dataNakeHeStarCount2[k][i][j+1],4))+"</p></td>"

    #写入html文件
    htmlContent+="</tr></table>"
    with open(htmlFileLocation, 'w') as f:
        f.write(htmlContent)
        print(functions.nowtime()+str(dataRunTime)+" Stage 3.2: Summarizing")
        f.write("</tr></table></div><div style='border:1px solid #000;margin:2px'>")
        evolutionList(f,data1,data2,data3,dataInfo)
        f.write("</div></body></html>")
    print(functions.nowtime()+str(dataRunTime)+" Stage 3.4: End.")


#入口程序
entrance()
gc.collect()
