import pandas as pd
import subprocess
from alive_progress import alive_bar
import functions
import sys

#定义变量与参数
dataRunTime="20230324_025538" # 10,000-20230324_013259 100,000-20230324_015309 1,000,000-20230324_015630 10,000,000-20230324_025538
eTimeEdgeList=[10,20,100,1000]
ePeriodEdgeList=[0.0001,10,100,1000,10000]
dataFolderLocation=functions.locationCheck(dataRunTime)
htmlFolderLocation=dataFolderLocation+dataRunTime+"/"
dataFileLocation=dataFolderLocation+"N"+dataRunTime+".csv"
print(functions.nowtime()+str(dataRunTime)+" Stage 1.1: Loading data: All")
dataAll=pd.read_csv(dataFileLocation,usecols=["i","t1","mx","mx2","tbx","kw","kw2","sepx","ndt"])
totalFormationCount=int(subprocess.getoutput("grep "+dataRunTime+" "+dataFolderLocation+"rdc.num | awk '{print $4}'"))
effectiveFormationCount=int(subprocess.getoutput("grep "+dataRunTime+" "+dataFolderLocation+"rdc.num | awk '{print $4-$9}'"))
htmlFileLocation=htmlFolderLocation+str(totalFormationCount)+"-"+dataRunTime+"-Analysis.html"
dataZ=subprocess.getoutput("grep 'z =' "+dataFolderLocation+"popbin.f | awk '{print $NF}'")
dataSFR=subprocess.getoutput("grep '^ *sfr' "+dataFolderLocation+"popbin.f | awk '{print $NF}'")
print(functions.nowtime()+str(dataRunTime)+" Stage 1 running successfully: Initialization completed.")

def NumAnalytics(data):
    NumAnalyticsCount,k=[],0
    with alive_bar(6, ctrl_c=False, title=f'NumAnalytics: ') as bar:
        for i in [13,14]:
            for j in [7,8,9]:
                NumAnalyticsCount.append([[],[]])
                NumAnalyticsCount[k][0]=list(set(data[(data["kw"]==i)&(data["kw2"]==j)]["i"]))
                NumAnalyticsCount[k][1]=list(data[(data["kw"]==i)&(data["kw2"]==j)]["ndt"])
                # print(functions.nowtime()+"NumAnalytics: "+str(i)+"-"+str(j))
                NumAnalyticsCount[k][0].sort()
                NumAnalyticsCount[k][0]=len(NumAnalyticsCount[k][0])
                NumAnalyticsCount[k][1]=sum(NumAnalyticsCount[k][1])
                k+=1
                bar()
    # for i in range(0,len(NumAnalyticsCount)):
    #     NumAnalyticsCount[i][0].sort()
    #     NumAnalyticsCount[i][0]=len(NumAnalyticsCount[i][0])
    #     NumAnalyticsCount[i][1]=sum(NumAnalyticsCount[i][1])
    # print(functions.nowtime()+"NumAnalytics: End")
    return NumAnalyticsCount

def dataAnalytics(data):
    eTimeEdgeMyrsCount,ePeriodEdgeCount="",""
    for ageEdgeNum in range(0,len(eTimeEdgeList)):
        eTimeEdgeMyrs=[list(set(data[data['t1']<=eTimeEdgeList[ageEdgeNum]]['i'])),list(set(data[data['t1']>eTimeEdgeList[ageEdgeNum]]['i']))]
        eTimeEdgeMyrsNumber=[len(eTimeEdgeMyrs[0]),0,len(eTimeEdgeMyrs[1])]
        totalnum=len(eTimeEdgeMyrs[1])
        with alive_bar(totalnum, ctrl_c=False, title=f'Uniqueness the data file in Age Edge: {eTimeEdgeList[ageEdgeNum]}') as bar:
            for i in range(0,totalnum):
                if eTimeEdgeMyrs[1][i] in eTimeEdgeMyrs[0]:
                    eTimeEdgeMyrsNumber[0]-=1
                    eTimeEdgeMyrsNumber[1]+=1
                    eTimeEdgeMyrsNumber[2]-=1
                bar()
        del eTimeEdgeMyrs
        eTimeEdgeMyrsCount+="Age < "+str(eTimeEdgeList[ageEdgeNum])+" Count: "+str(eTimeEdgeMyrsNumber[0])+" , Cross the edge: "+str(eTimeEdgeMyrsNumber[1])+" , > "+str(eTimeEdgeList[ageEdgeNum])+" : "+str(eTimeEdgeMyrsNumber[2])+"\n"
    for periodEdgeNum in range(0,len(ePeriodEdgeList)):
        ePeriodEdge=[list(set(data[data['tbx']<=ePeriodEdgeList[periodEdgeNum]]['i'])),list(set(data[data['tbx']>ePeriodEdgeList[periodEdgeNum]]['i']))]
        ePeriodEdgeMyrsNumber=[len(ePeriodEdge[0]),0,len(ePeriodEdge[1])]
        totalnum=len(ePeriodEdge[1])
        with alive_bar(totalnum, ctrl_c=False, title=f'Uniqueness the data file in Period Edge: {ePeriodEdgeList[periodEdgeNum]}') as bar:
            for i in range(0,totalnum):
                if ePeriodEdge[1][i] in ePeriodEdge[0]:
                    ePeriodEdgeMyrsNumber[0]-=1
                    ePeriodEdgeMyrsNumber[1]+=1
                    ePeriodEdgeMyrsNumber[2]-=1
                bar()
        del ePeriodEdge
        ePeriodEdgeCount+="Period < "+str(ePeriodEdgeList[periodEdgeNum])+" Count: "+str(ePeriodEdgeMyrsNumber[0])+" , Cross the edge: "+str(ePeriodEdgeMyrsNumber[1])+" , > "+str(ePeriodEdgeList[periodEdgeNum])+" : "+str(ePeriodEdgeMyrsNumber[2])+"\n"
    return eTimeEdgeMyrsCount,ePeriodEdgeCount,len(list(set(data['i'])))

def ListAnalytics(data):
    PeriodMinimumList=[0.00001,0.0001]
    PeriodMaximumList=[100000,1000000]
    with open(htmlFileLocation, 'w') as f:
        for i in PeriodMinimumList:
            ilist=list(set(data[data["tbx"]<=i]["i"]))
            ilist.sort()
            if len(ilist) > 0:
                f.write("Period <= "+str(i)+"d ~ "+str(i*86400)+"s, Count: "+str(len(ilist))+" : "+str(ilist)+"<br />")
                for k in range(0,len(ilist)):
                    f.write("<table><tr><th>i</th><th>t1(百万年)</th><th>mx(太阳质量)</th><th>mx2(太阳质量)</th><th>tbx(天)</th><th>kw</th><th>kw2</th><th>sepx(太阳半径)</th><th>N(数量)</th>")
                    runRecords=subprocess.getoutput("grep '"+str(dataRunTime)+", *"+str(ilist[k])+" ' "+dataFolderLocation+"data/records.dat").split(",")
                    f.write("<tr><th>"+str(runRecords[1].strip())+"</th><th>0</th><th>"+str(runRecords[2].split()[0].strip())+"</th><th>"+str(runRecords[2].split()[1].strip())+"</th><th>"+str(runRecords[3].strip())+"</th><th>0</th><th>0</th><th>"+str(runRecords[-1].strip())+"</th><th>0</th>")
                    l=data[(data["i"]==ilist[k])&(data["tbx"]<=i)].values.tolist()
                    for li in range(0,len(l)):
                        f.write("<tr><td>"+str(int(l[li][0]))+"</td><td>"+str(l[li][1])+"</td><td>"+str(l[li][2])+"</td><td>"+str(l[li][3])+"</td><td>"+str(l[li][4])+"</td><td>"+str(int(l[li][5]))+"</td><td>"+str(int(l[li][6]))+"</td><td>"+str(l[li][7])+"</td><td>"+str(l[li][8])+"</td></tr>")
                    f.write("</table>")
        for i in PeriodMaximumList:
            ilist=list(set(data[data["tbx"]>=i]["i"]))
            ilist.sort()
            if len(ilist) > 0:
                f.write("Period >= "+str(i)+"d, Count: "+str(len(ilist))+" : "+str(ilist)+"<br />")
                for k in range(0,len(ilist)):
                    f.write("<table><tr><th>i</th><th>t1(百万年)</th><th>mx(太阳质量)</th><th>mx2(太阳质量)</th><th>tbx(天)</th><th>kw</th><th>kw2</th><th>sepx(太阳半径)</th><th>N(数量)</th>")
                    runRecords=subprocess.getoutput("grep '"+str(dataRunTime)+", *"+str(ilist[k])+" ' "+dataFolderLocation+"data/records.dat").split(",")
                    f.write("<tr><th>"+str(runRecords[1].strip())+"</th><th>0</th><th>"+str(runRecords[2].split()[0].strip())+"</th><th>"+str(runRecords[2].split()[1].strip())+"</th><th>"+str(runRecords[3].strip())+"</th><th>0</th><th>0</th><th>"+str(runRecords[-1].strip())+"</th><th>0</th>")
                    l=data[(data["i"]==ilist[k])&(data["tbx"]>=i)].values.tolist()
                    for li in range(0,len(l)):
                        f.write("<tr><td>"+str(int(l[li][0]))+"</td><td>"+str(l[li][1])+"</td><td>"+str(l[li][2])+"</td><td>"+str(l[li][3])+"</td><td>"+str(l[li][4])+"</td><td>"+str(int(l[li][5]))+"</td><td>"+str(int(l[li][6]))+"</td><td>"+str(l[li][7])+"</td><td>"+str(l[li][8])+"</td></tr>")
                    f.write("</table>")

def entrance():
    kwList=["中子星+主序星阶段裸露氦星","中子星+赫氏空隙裸露氦星","中子星+巨星支裸露氦星","黑洞+主序星阶段裸露氦星","黑洞+赫氏空隙裸露氦星","黑洞+巨星支裸露氦星"]
    # print(functions.nowtime()+str(dataRunTime)+" Stage 2.1: Entrance : All")
    # dataAllReturn=dataAnalytics(dataAll)
    # print(functions.nowtime()+str(dataRunTime)+" Stage 2.2: Entrance : NS")
    # dataNSReturn=dataAnalytics(dataAll[dataAll["kw"]==13])
    # print(functions.nowtime()+str(dataRunTime)+" Stage 2.3: Entrance : BH")
    # dataBHReturn=dataAnalytics(dataAll[dataAll["kw"]==14])
    # print(functions.nowtime()+str(dataRunTime)+" Stage 3.1: NumAnalytics")
    # dataNakeHeStarCount=NumAnalytics(dataAll)
    plotFileNameList=functions.plotMain(dataAll,htmlFolderLocation)
    print(functions.nowtime()+str(dataRunTime)+" Stage 3.2: Summarizing")
    with open(htmlFileLocation, 'w') as f:
        f.write("<html><head><title>"+str(totalFormationCount)+"-"+dataRunTime+"-"+"-Analysis"+"</title><style>table,tr,td,th{border:1px solid #000;padding:0 2px 0 2px}</style></head><body>")
        f.write("<div>运行起始时间：<b>"+dataRunTime+"</b>, 设置双星总数量: <b>"+str(totalFormationCount)+"</b>, 实际双星演化数量: <b>"+str(effectiveFormationCount)+"</b>, Z=<b>"+dataZ+"</b>, SFR=<b>"+str(dataSFR)+"</b><br />")
        f.write("其中致密星为中子星或黑洞，伴星为裸露氦星(含:7-MS,8-HG,9-GB)的数量/比例为: <b>"+str(dataAllReturn[2])+"/"+str(effectiveFormationCount)+"={:.2%}".format(dataAllReturn[2]/effectiveFormationCount)+"</b><br />")
        f.write("双星中致密星为中子星的数量/比例为: <b>"+str(dataNSReturn[2])+"/"+str(dataAllReturn[2])+"={:.2%}".format(dataNSReturn[2]/dataAllReturn[2])+","+str(dataNSReturn[2])+"/"+str(effectiveFormationCount)+"={:.2%}".format(dataNSReturn[2]/effectiveFormationCount)+"</b><br />")
        f.write("双星中致密星为黑洞的数量/比例为: <b>"+str(dataBHReturn[2])+"/"+str(dataAllReturn[2])+"={:.2%}".format(dataBHReturn[2]/dataAllReturn[2])+","+str(dataBHReturn[2])+"/"+str(effectiveFormationCount)+"={:.2%}".format(dataBHReturn[2]/effectiveFormationCount)+"</b><br />")
        f.write("<table><tr><th>双星组成</th><th>数量/比例</th><th>总存在时间(Ri*dtt, 单位为百万年)/平均时间为</th></tr>")
        for i in range(0,3):
            f.write("<tr><td>"+kwList[i]+"</td><td>"+str(dataNakeHeStarCount[i][0])+" / "+str(dataNSReturn[2])+" = {:.2%}".format(dataNakeHeStarCount[i][0]/dataNSReturn[2])+","+str(dataNakeHeStarCount[i][0])+" / "+str(effectiveFormationCount)+" = {:.2%}".format(dataNakeHeStarCount[i][0]/effectiveFormationCount)+"</td><td>"+str(dataNakeHeStarCount[i][1])+" / "+str(dataNakeHeStarCount[i][0])+" ~ "+str(dataNakeHeStarCount[i][1]/dataNakeHeStarCount[i][0])+"(Myrs)</tr>")
        for i in range(3,6):
            f.write("<tr><td>"+kwList[i]+"</td><td>"+str(dataNakeHeStarCount[i][0])+" / "+str(dataBHReturn[2])+" = {:.2%}".format(dataNakeHeStarCount[i][0]/dataBHReturn[2])+","+str(dataNakeHeStarCount[i][0])+" / "+str(effectiveFormationCount)+" = {:.2%}".format(dataNakeHeStarCount[i][0]/effectiveFormationCount)+"</td><td>"+str(dataNakeHeStarCount[i][1])+" / "+str(dataNakeHeStarCount[i][0])+" ~ "+str(dataNakeHeStarCount[i][1]/dataNakeHeStarCount[i][0])+"(Myrs)</tr>")
        f.write("</table><div style='border:1px solid #000;display:inline-block;'>不同分界点的演化数量: <br /><p style='margin:0;white-space:pre-line;width:auto;margin:2px;padding:2px;border:1px solid #000;display:inline-block;'>1.全部:<br />"+dataAllReturn[0]+"</p><p style='margin:0;white-space:pre-line;width:auto;margin:2px;padding:2px;border:1px solid #000;display:inline-block;'>2.NS:<br />"+dataNSReturn[0]+"</p><p style='margin:0;white-space:pre-line;width:auto;margin:2px;padding:2px;border:1px solid #000;display:inline-block;'>3.BH:<br />"+dataBHReturn[0]+"</p>")
        f.write("<br /><hr /><p style='margin:0;white-space:pre-line;width:auto;margin:2px;padding:2px;border:1px solid #000;display:inline-block;'>1.全部:<br />"+dataAllReturn[1]+"</p><p style='margin:0;white-space:pre-line;width:auto;margin:2px;padding:2px;border:1px solid #000;display:inline-block;'>2.NS:<br />"+dataNSReturn[1]+"</p><p style='margin:0;white-space:pre-line;width:auto;margin:2px;padding:2px;border:1px solid #000;display:inline-block;'>3.BH:<br />"+dataBHReturn[1]+"</p></div>\n<div>")
        for i in range(0,len(plotFileNameList)):
            f.write("<img src='"+htmlFolderLocation+plotFileNameList[i]+".png' alt='"+plotFileNameList[i]+"'>\n")
        # ListAnalytics(dataAll)
        f.write("</div></body></html>")
    print(functions.nowtime()+str(dataRunTime)+" Stage 3.4: End.")

entrance()
