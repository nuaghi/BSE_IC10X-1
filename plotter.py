import pandas as pd
import subprocess
from alive_progress import alive_bar
import functions
import sys
import gc




# 先画整体的图，先不做细致的切割
#已解决 1.colorbar有无上下限，既然已经限制了N>10^-8，为什么还有10^-9出现 是dtt太短还是什么原因
  # 确实有上下限vmin vmax 之后不会再出现这个级别的数字了 只会大于0


# 2.M2>2 age<100Myrs即可 +N>10^-4 +tbx>10^-4
# 3.检查下<10^-4形成原因 r/rL是否填满洛希瓣 对于密近系统，可能伴星之后演化成白矮星 图边角看下演化总过程  tbx很大是否是偏心率问题
# 未解决，详细计划：popbin.f 增加全量演化文件 增加ecc列        修改plotter逻辑 对于边角部分进行检查

# 4.确定下最近的观测值 伴星质量 黑洞质量
# 5.添加误差棒十字
# 未解决，详细计划：看最近论文 并找到最近比较可信的约束条件

# 6.并排 质量-质量图 或者黑洞质量-周期图
# 未解决，最后弄



#定义变量与参数
dataRunTime="20230325_212246" # 10,000-20230324_013259 20230325_212216 100,000-20230324_015309 20230325_212246 1,000,000-20230324_015630 20230325_212743  10,000,000-20230324_025538 20230325_221712
eTimeEdgeList=[10,20,100,1000]
ePeriodEdgeList=[0.0001,10,100,1000,10000]
dataFolderLocation=functions.locationCheck(dataRunTime)
dataFileLocation=dataFolderLocation+"N"+dataRunTime+".csv"
print(functions.nowtime()+str(dataRunTime)+" Stage 1.1: Loading data: All")
dataAll=pd.read_csv(dataFileLocation,usecols=["i","t1","mx","mx2","tbx","kw","kw2","sepx","ndt"])
dataAll=dataAll[(dataAll["t1"]>0)&(dataAll["t1"]>0)&(dataAll["mx"]>0)&(dataAll["mx2"]>0)&(dataAll["tbx"]>0)&(dataAll["sepx"]>0)&(dataAll["ndt"]>0)]
totalFormationCount=int(subprocess.getoutput("grep "+dataRunTime+" "+dataFolderLocation+"rdc.num | awk '{print $4}'"))
if totalFormationCount > 0:
    htmlFolderLocation=dataFolderLocation+dataRunTime+"_"+str(totalFormationCount)+"/"
else:
    htmlFolderLocation=dataFolderLocation+dataRunTime+"/"
effectiveFormationCount=int(subprocess.getoutput("grep "+dataRunTime+" "+dataFolderLocation+"rdc.num | awk '{print $4-$9}'"))
htmlFileLocation=htmlFolderLocation+str(totalFormationCount)+"-"+dataRunTime+"-Analysis.html"
dataZ=subprocess.getoutput("grep 'z =' ~/Documents/git/BSE_workbench/popbin.f | awk '{print $NF}'")
dataSFR=subprocess.getoutput("grep '^ *sfr' ~/Documents/git/BSE_workbench/popbin.f | awk '{print $NF}' | awk -F '=' '{print $2}'")
print(functions.nowtime()+str(dataRunTime)+" Stage 1 running successfully: Initialization completed.")

def NumAnalytics(data):
    NumAnalyticsCount,k=[],0
    with alive_bar(6, ctrl_c=False, title=f'NumAnalytics: ') as bar:
        for i in [13,14]:
            for j in [7,8,9]:
                NumAnalyticsCount.append([[],[],[],[],[],[],[],[],[],[],[],[]])
                NumAnalyticsCount[k][0]=len(list(set(data[(data["kw"]==i)&(data["kw2"]==j)]["i"])))
                NumAnalyticsCount[k][1]=sum(list(data[(data["kw"]==i)&(data["kw2"]==j)]["ndt"]))
                NumAnalyticsCount[k][2]=min(list(data[(data["kw"]==i)&(data["kw2"]==j)]["t1"]))
                NumAnalyticsCount[k][3]=max(list(data[(data["kw"]==i)&(data["kw2"]==j)]["t1"]))
                NumAnalyticsCount[k][4]=min(list(data[(data["kw"]==i)&(data["kw2"]==j)]["mx"]))
                NumAnalyticsCount[k][5]=max(list(data[(data["kw"]==i)&(data["kw2"]==j)]["mx"]))
                NumAnalyticsCount[k][6]=min(list(data[(data["kw"]==i)&(data["kw2"]==j)]["mx2"]))
                NumAnalyticsCount[k][7]=max(list(data[(data["kw"]==i)&(data["kw2"]==j)]["mx2"]))
                NumAnalyticsCount[k][8]=min(list(data[(data["kw"]==i)&(data["kw2"]==j)]["tbx"]))
                NumAnalyticsCount[k][9]=max(list(data[(data["kw"]==i)&(data["kw2"]==j)]["tbx"]))
                NumAnalyticsCount[k][10]=min(list(data[(data["kw"]==i)&(data["kw2"]==j)]["sepx"]))
                NumAnalyticsCount[k][11]=max(list(data[(data["kw"]==i)&(data["kw2"]==j)]["sepx"]))
                k+=1
                bar()
    del data,k,bar
    gc.collect()
    return NumAnalyticsCount

def dataAnalytics(data):
    eTimeEdgeMyrsCount,ePeriodEdgeCount="",""
    listSetDataI=[len(list(set(data[data['kw']==13]['i']))),len(list(set(data[data['kw']==14]['i'])))]
    for ageEdgeNum in range(len(eTimeEdgeList)):
        eTimeEdgeMyrs=[list(set(data[(data['t1']<=eTimeEdgeList[ageEdgeNum])&(data['kw']==13)]['i'])),0,list(set(data[(data['t1']>eTimeEdgeList[ageEdgeNum])&(data['kw']==13)]['i'])),list(set(data[(data['t1']<=eTimeEdgeList[ageEdgeNum])&(data['kw']==14)]['i'])),0,list(set(data[(data['t1']>eTimeEdgeList[ageEdgeNum])&(data['kw']==14)]['i']))]
        eTimeEdgeMyrsNumber=[len(eTimeEdgeMyrs[0]),0,len(eTimeEdgeMyrs[2]),len(eTimeEdgeMyrs[3]),0,len(eTimeEdgeMyrs[5])]
        if eTimeEdgeMyrsNumber[0] < eTimeEdgeMyrsNumber[2]:
            totalnumNS=eTimeEdgeMyrsNumber[0]
            numberList=[0,2]
        else:
            totalnumNS=eTimeEdgeMyrsNumber[2]
            numberList=[2,0]
        with alive_bar(totalnumNS, ctrl_c=False, title=f'Uniqueness the NS data in Age Edge: {eTimeEdgeList[ageEdgeNum]}') as bar:
            for i in range(totalnumNS):
                if eTimeEdgeMyrs[numberList[0]][i] in eTimeEdgeMyrs[numberList[1]]:
                    eTimeEdgeMyrsNumber[0]-=1
                    eTimeEdgeMyrsNumber[1]+=1
                    eTimeEdgeMyrsNumber[2]-=1
                bar()
        if eTimeEdgeMyrsNumber[3] < eTimeEdgeMyrsNumber[5]:
            totalnumBH=eTimeEdgeMyrsNumber[3]
            numberList=[3,5]
        else:
            totalnumBH=eTimeEdgeMyrsNumber[5]
            numberList=[5,3]
        with alive_bar(totalnumBH, ctrl_c=False, title=f'Uniqueness the BH data in Age Edge: {eTimeEdgeList[ageEdgeNum]}') as bar:
            for i in range(totalnumBH):
                if eTimeEdgeMyrs[numberList[0]][i] in eTimeEdgeMyrs[numberList[1]]:
                    eTimeEdgeMyrsNumber[3]-=1
                    eTimeEdgeMyrsNumber[4]+=1
                    eTimeEdgeMyrsNumber[5]-=1
                bar()
        del eTimeEdgeMyrs
        gc.collect()
        eTimeEdgeMyrsCount+="NS Age < "+str(eTimeEdgeList[ageEdgeNum])+" Count: "+str(eTimeEdgeMyrsNumber[0])+" , Cross the edge: "+str(eTimeEdgeMyrsNumber[1])+" , > "+str(eTimeEdgeList[ageEdgeNum])+" : "+str(eTimeEdgeMyrsNumber[2])+"\nBH Age < "+str(eTimeEdgeList[ageEdgeNum])+" Count: "+str(eTimeEdgeMyrsNumber[3])+" , Cross the edge: "+str(eTimeEdgeMyrsNumber[4])+" , > "+str(eTimeEdgeList[ageEdgeNum])+" : "+str(eTimeEdgeMyrsNumber[5])+"\n"
    print(functions.nowtime()+str(dataRunTime)+" Stage 2.2: Data Analytics: Period")
    for periodEdgeNum in range(len(ePeriodEdgeList)):
        ePeriodEdge=[list(set(data[(data['tbx']<=ePeriodEdgeList[periodEdgeNum])&(data['kw']==13)]['i'])),0,list(set(data[(data['tbx']>ePeriodEdgeList[periodEdgeNum])&(data['kw']==13)]['i'])),list(set(data[(data['tbx']<=ePeriodEdgeList[periodEdgeNum])&(data['kw']==14)]['i'])),0,list(set(data[(data['tbx']>ePeriodEdgeList[periodEdgeNum])&(data['kw']==14)]['i']))]
        ePeriodEdgeMyrsNumber=[len(ePeriodEdge[0]),0,len(ePeriodEdge[2]),len(ePeriodEdge[3]),0,len(ePeriodEdge[5])]
        if ePeriodEdgeMyrsNumber[0] < ePeriodEdgeMyrsNumber[2]:
            totalnumNS=ePeriodEdgeMyrsNumber[0]
            numberList=[0,2]
        else:
            totalnumNS=ePeriodEdgeMyrsNumber[2]
            numberList=[2,0]
        with alive_bar(totalnumNS, ctrl_c=False, title=f'Uniqueness the NS data in Period Edge: {ePeriodEdgeList[periodEdgeNum]}') as bar:
            for i in range(totalnumNS):
                if ePeriodEdge[numberList[0]][i] in ePeriodEdge[numberList[1]]:
                    ePeriodEdgeMyrsNumber[0]-=1
                    ePeriodEdgeMyrsNumber[1]+=1
                    ePeriodEdgeMyrsNumber[2]-=1
                bar()
        if ePeriodEdgeMyrsNumber[3] < ePeriodEdgeMyrsNumber[5]:
            totalnumBH=ePeriodEdgeMyrsNumber[3]
            numberList=[3,5]
        else:
            totalnumBH=ePeriodEdgeMyrsNumber[5]
            numberList=[5,3]
        with alive_bar(totalnumBH, ctrl_c=False, title=f'Uniqueness the BH data in Period Edge: {ePeriodEdgeList[periodEdgeNum]}') as bar:
            for i in range(totalnumBH):
                if ePeriodEdge[numberList[0]][i] in ePeriodEdge[numberList[1]]:
                    ePeriodEdgeMyrsNumber[3]-=1
                    ePeriodEdgeMyrsNumber[4]+=1
                    ePeriodEdgeMyrsNumber[5]-=1
                bar()
        ePeriodEdgeCount+="NS Period < "+str(ePeriodEdgeList[periodEdgeNum])+" Count: "+str(ePeriodEdgeMyrsNumber[0])+" , Cross the edge: "+str(ePeriodEdgeMyrsNumber[1])+" , > "+str(ePeriodEdgeList[periodEdgeNum])+" : "+str(ePeriodEdgeMyrsNumber[2])+"\nBH Period < "+str(ePeriodEdgeList[periodEdgeNum])+" Count: "+str(ePeriodEdgeMyrsNumber[3])+" , Cross the edge: "+str(ePeriodEdgeMyrsNumber[4])+" , > "+str(ePeriodEdgeList[periodEdgeNum])+" : "+str(ePeriodEdgeMyrsNumber[5])+"\n"
    del data,totalnumNS,totalnumBH
    gc.collect()
    return eTimeEdgeMyrsCount,ePeriodEdgeCount,listSetDataI

def ListAnalytics(f,data):
    PeriodMinimumList=[0.000001,0.00001,0.0001]
    PeriodMaximumList=[1000000,10000000]
    for i in PeriodMinimumList:
        ilist=list(set(data[data["tbx"]<=i]["i"]))
        ilist.sort()
        lenIList=len(ilist)
        if lenIList > 0:
            f.write("<div><b style='background: yellow;' onclick='$(this).siblings(\'table\').each(function(){$(this).show()})'>Period <= "+str(i)+"d ~ "+str(i*86400)+"s, Count: "+str(lenIList)+" : "+str(ilist)+"</b>")
            with alive_bar(lenIList, ctrl_c=False, title=f'Appending data when Period lower than {i}') as bar:
                for k in range(lenIList):
                    f.write("<table style='display: none;max-height: 300px;overflow: auto;'><tr><th>i</th><th>t1(百万年)</th><th>mx(太阳质量)</th><th>mx2(太阳质量)</th><th>tbx(天)</th><th>kw</th><th>kw2</th><th>sepx(太阳半径)</th><th>N(数量)</th>")
                    runRecords=subprocess.getoutput("grep '"+str(dataRunTime)+", *"+str(ilist[k])+" ' "+dataFolderLocation+"records.dat").split(",")
                    if runRecords[0].find("directory") == -1:
                        f.write("<tr><th>"+str(runRecords[1].strip())+"</th><th>0</th><th>"+str(runRecords[2].split()[0].strip())+"</th><th>"+str(runRecords[2].split()[1].strip())+"</th><th>"+str(runRecords[3].strip())+"</th><th>0</th><th>0</th><th>"+str(runRecords[-1].strip())+"</th><th>0</th>")
                    l=data[(data["i"]==ilist[k])&(data["tbx"]<=i)].values.tolist()
                    for li in range(len(l)):
                        f.write("<tr><td>"+str(int(l[li][0]))+"</td><td>"+str(l[li][1])+"</td><td>"+str(l[li][2])+"</td><td>"+str(l[li][3])+"</td><td>"+str(l[li][4])+"</td><td>"+str(int(l[li][5]))+"</td><td>"+str(int(l[li][6]))+"</td><td>"+str(l[li][7])+"</td><td>"+str(l[li][8])+"</td></tr>")
                    f.write("</table>")
                    bar()
            f.write("</div>")
        else:
            f.write("<div><b style='background: yellow;'>Period <= "+str(i)+"d ~ "+str(i*86400)+"s, Count: 0</b></div>")
    for i in PeriodMaximumList:
        ilist=list(set(data[data["tbx"]>=i]["i"]))
        ilist.sort()
        lenIList=len(ilist)
        if lenIList > 0:
            f.write("<div><b style='background: yellow;' onclick='$(this).siblings(\'table\').each(function(){$(this).show()})'>Period >= "+str(i)+"d, Count: "+str(lenIList)+" : "+str(ilist)+"</b>")
            with alive_bar(lenIList, ctrl_c=False, title=f'Appending data when Period greater than {i}') as bar:
                for k in range(lenIList):
                    f.write("<table style='display: none;max-height: 300px;overflow: auto;'><tr><th>i</th><th>t1(百万年)</th><th>mx(太阳质量)</th><th>mx2(太阳质量)</th><th>tbx(天)</th><th>kw</th><th>kw2</th><th>sepx(太阳半径)</th><th>N(数量)</th>")
                    runRecords=subprocess.getoutput("grep '"+str(dataRunTime)+", *"+str(ilist[k])+" ' "+dataFolderLocation+"records.dat").split(",")
                    if runRecords[0].find("directory") == -1:
                        f.write("<tr><th>"+str(runRecords[1].strip())+"</th><th>0</th><th>"+str(runRecords[2].split()[0].strip())+"</th><th>"+str(runRecords[2].split()[1].strip())+"</th><th>"+str(runRecords[3].strip())+"</th><th>0</th><th>0</th><th>"+str(runRecords[-1].strip())+"</th><th>0</th>")
                    l=data[(data["i"]==ilist[k])&(data["tbx"]>=i)].values.tolist()
                    for li in range(len(l)):
                        f.write("<tr><td>"+str(int(l[li][0]))+"</td><td>"+str(l[li][1])+"</td><td>"+str(l[li][2])+"</td><td>"+str(l[li][3])+"</td><td>"+str(l[li][4])+"</td><td>"+str(int(l[li][5]))+"</td><td>"+str(int(l[li][6]))+"</td><td>"+str(l[li][7])+"</td><td>"+str(l[li][8])+"</td></tr>")
                    f.write("</table>")
                    bar()
            f.write("</div>")
        else:
            f.write("<div><b style='background: yellow;'>Period >= "+str(i)+"d, Count: 0</b><br /></div>")
    del data,lenIList,ilist
    gc.collect()

def entrance():
    # kwList=["中子星+主序星阶段裸露氦星","中子星+赫氏空隙裸露氦星","中子星+巨星支裸露氦星","黑洞+主序星阶段裸露氦星","黑洞+赫氏空隙裸露氦星","黑洞+巨星支裸露氦星"]
    # print(functions.nowtime()+str(dataRunTime)+" Stage 2.1: Data Analytics")
    # dataReturn=dataAnalytics(dataAll)
    # print(functions.nowtime()+str(dataRunTime)+" Stage 3.1: NumAnalytics")
    # dataNakeHeStarCount=NumAnalytics(dataAll)
    with open(htmlFileLocation, 'w') as f:
        f.write("<html><head><title>"+str(totalFormationCount)+"-"+dataRunTime+"-"+"-Analysis"+"</title><style>table,tr,td,th{border:1px solid #000;padding:0 2px 0 2px;white-space:pre-line;}div{padding:1px}</style><script type='text/javascript' src='./jquery.js'></script></head><body>\n")
        f.write("<div><div class='summary'>运行起始时间：<b>"+dataRunTime+"</b>, 设置双星总数量: <b>"+str(totalFormationCount)+"</b>, 实际双星演化数量: <b>"+str(effectiveFormationCount)+"</b>, Z=<b>"+dataZ+"</b>, SFR=<b>"+str(dataSFR)+"</b><br />")
    #     f.write("其中致密星为中子星或黑洞，伴星为裸露氦星(含:7-MS,8-HG,9-GB)的数量/比例为: <b>"+str(sum(dataReturn[2]))+"/"+str(effectiveFormationCount)+"={:.2%}".format(sum(dataReturn[2])/effectiveFormationCount)+"</b><br />")
    #     f.write("双星中致密星为中子星的数量/比例为: <b>"+str(dataReturn[2][0])+"/"+str(sum(dataReturn[2]))+"={:.2%}".format(dataReturn[2][0]/sum(dataReturn[2]))+","+str(dataReturn[2][0])+"/"+str(effectiveFormationCount)+"={:.2%}".format(dataReturn[2][0]/effectiveFormationCount)+"</b><br />")
    #     f.write("双星中致密星为黑洞的数量/比例为: <b>"+str(dataReturn[2][1])+"/"+str(sum(dataReturn[2]))+"={:.2%}".format(dataReturn[2][1]/sum(dataReturn[2]))+","+str(dataReturn[2][1])+"/"+str(effectiveFormationCount)+"={:.2%}".format(dataReturn[2][1]/effectiveFormationCount)+"</b></div><br />")
    #     f.write("<table><tr><th>双星组成</th><th>数量/比例</th><th>总数量(Ri*dtt)</th><th>Age范围[Myrs]</th><th>致密星质量范围[Msun]</th><th>伴星质量范围[Msun]</th><th>轨道周期范围[d]</th><th>轨道间距范围[Rsun]</th></tr>")
    #     for i in range(6):
    #         writeContent="<tr><td style='width: max-content;'>"+kwList[i]+"</td><td style='width: max-content;'>"+str(dataNakeHeStarCount[i][0])+" / "+str(dataReturn[2][i//3])+" = {:.2%}".format(dataNakeHeStarCount[i][0]/dataReturn[2][i//3])+","+str(dataNakeHeStarCount[i][0])+" / "+str(effectiveFormationCount)+" = {:.2%}".format(dataNakeHeStarCount[i][0]/effectiveFormationCount)+"</td><td>"+str(dataNakeHeStarCount[i][1])+"</td>"
    #         for j in [2,4,6,8,10]:
    #             writeContent+="<td>Min: "+str(dataNakeHeStarCount[i][j])+"\nMax: "+str(dataNakeHeStarCount[i][j+1])+"</td>"
    #         f.write(writeContent)
    #     f.write("</table></div>\n\n<div class='EdgeNumber' style='border:1px solid #000;'>不同分界点的演化数量: <br /><p style='margin:0;white-space:pre-line;width:auto;margin:2px;padding:2px;border:1px solid #000;display:inline-block;'>"+dataReturn[0]+"</p><p style='margin:0;white-space:pre-line;width:auto;margin:2px;padding:2px;border:1px solid #000;display:inline-block;'>"+dataReturn[1]+"</p></div><div class='Plot'>")
    # del kwList,dataReturn,dataNakeHeStarCount

    plotFileNameList=functions.plotMain(dataAll,htmlFolderLocation)
    print(functions.nowtime()+str(dataRunTime)+" Stage 3.2: Summarizing")
    with open(htmlFileLocation, 'a') as f:
        for i in range(len(plotFileNameList)):
            f.write("<img src='"+plotFileNameList[i]+".png' alt='"+plotFileNameList[i]+"'>\n")
            if (i+1) % 2 == 0:
                f.write("<textarea style='width:450px;height:450px;font-size:25px;padding:5px;border:1px solid #999'></textarea>\n")
        f.write("</div><div style='display:block;border:1px solid #000;'>")
        ListAnalytics(f,dataAll)
        f.write("</div></body></html>")
    print(functions.nowtime()+str(dataRunTime)+" Stage 3.4: End.")
    gc.collect()
entrance()
del dataAll
gc.collect()