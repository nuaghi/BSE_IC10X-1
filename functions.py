import os
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math
import datetime
import subprocess
import sys

def nowtime():
    return datetime.datetime.now().strftime('%m%d-%H%M%S ')

def onetwentieth(i):
    if int(i)>0:
        j =  i//2000*100
        if j>=1000000:
            return 1000000
        elif j > 0:
            return j
        else:
            return 1

def alter(file,old_str,new_str):
    file_data = ""
    totalnum=int(subprocess.getoutput("wc -l %s | awk '{print $1}'" % file))
    otnum=onetwentieth(totalnum)
    i=0
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            i+=1
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
            if i%otnum==0 or i%totalnum==0:
                print(nowtime()+"Step1: Replace the contents of data file: "+str(i)+"/"+str(totalnum)+", "+"percent: {:.2%}".format(i/totalnum))
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)

def locationCheck(dataRunTime):
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
    htmlFolderLocation=dataFolderLocation+dataRunTime+"/"
    dataFileLocation=dataFolderLocation+"N"+dataRunTime+".csv"
    if not os.path.exists(dataFileLocation):
        print(nowtime()+"FATAL ERROR: [File '"+dataFileLocation+"' Not Found.] Exit.")
        exit(0)
    else:
        if not os.path.exists(htmlFolderLocation):
            os.mkdir(htmlFolderLocation)
        return dataFolderLocation

plotFileNameList=[]
def plotSingle(xdata,ydata,scale,xl,yl,weights2,ptitle,fname,htmlFolderLocation):
    if scale==0:
        plt.hist2d(xdata,ydata,bins=25,density=50,weights=weights2,norm=LogNorm())
        plt.colorbar()
    else:
        plt.scatter(xdata,ydata,s=scale)
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.title(ptitle)
    plt.savefig(htmlFolderLocation+fname)
    plt.close()
    plotFileNameList.append(fname)
    print(nowtime()+"Plot"+fname)

def plotDistribution(xdata,weights,label,range,title,xlabel,ylabel,htmlFolderLocation):
    plt.hist(xdata, bins=100,histtype='step',weights=weights, color='tomato', linewidth=1.5,label=label,range=range)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(htmlFolderLocation+title)
    plt.close()
    plotFileNameList.append(title)

def plotMain(data,htmlFolderLocation):
    plotSingle(data["t1"], data["mx2"], 0, r"$\mathit{Age}}$[Myrs]", r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", data["ndt"], "Age - Mass, dataset: All", "2-AgeMassAllWeight",htmlFolderLocation)
    plotSingle(data[data["tbx"]>0]["mx2"], data[data["tbx"]>0]["tbx"].apply(lambda x:math.log10(x)), 0, r"$\mathit{M_{donor}}$[${M_{sun}}$]", r"$\mathit{log P_{orb,cur}}$[d]", data[data["tbx"]>0]["ndt"], r"$\mathit{Mass - log(Period), dataset: All}$", "8-MasslgPeriodWeight",htmlFolderLocation)
    plotSingle(data[data["kw"]==13]["t1"], data[data["kw"]==13]["mx2"], 0, r"$\mathit{Age}}$[Myrs]", r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", data[data["kw"]==13]["ndt"],r"$\mathit{Age - Mass, dataset: NS}$", "4-AgeMassNSWeight",htmlFolderLocation)
    plotSingle(data[data["kw"]==14]["t1"], data[data["kw"]==14]["mx2"], 0, r"$\mathit{Age}}$[Myrs]", r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", data[data["kw"]==14]["ndt"],r"$\mathit{Age - Mass, dataset: BH}$", "6-AgeMassBHWeight",htmlFolderLocation)
    # plotSingle(data[(data["mx2"]>=2)&(data["kw"]==13)]["t1"],data[(data["mx2"]>=2)&(data["kw"]==13)]["mx2"],0,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]",data[(data["mx2"]>=i)&(data["kw"]==13)]["ndt"],r"$\mathit{Age - Mass, dataset: M_{donor}}$>="+str(i)+"${M_{sun}},NS$",str(i)+"AgeMassGT2WeightNS",htmlFolderLocation)
    # plotSingle(data[(data["mx2"]>=2)&(data["kw"]==13)]["t1"],data[(data["mx2"]>=2)&(data["kw"]==13)]["mx2"],0,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", data[(data["mx2"]>=2)&(data["kw"]==13)]["ndt"], r"$\mathit{Age - Mass, dataset: M_{donor}}$>=2${M_{sun}},NS$","AgeMassGT2WeightNS",htmlFolderLocation)
    # i=2
    # plotSingle(data[(data["mx2"]>=i)&(data["kw"]==13)]["t1"],data[(data["mx2"]>=i)&(data["kw"]==13)]["mx2"],0,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", data[(data["mx2"]>=i)&(data["kw"]==13)]["ndt"], r"$\mathit{Age - Mass, dataset: M_{donor}}$>="+str(i)+"${M_{sun}},NS$",str(i)+"AgeMassGT2WeightNS",htmlFolderLocation)

    # for i in [2,5,10,20]:
        # print(type(i))
        # sys.exit(0)
    i=2
    plotSingle(data[(data["mx2"]>=i)&(data["kw"]==13)&(data["ndt"]>=0.00001)&(data["tbx"]>=0.00001)]["t1"],data[(data["mx2"]>=i)&(data["kw"]==13)&(data["ndt"]>=0.00001)&(data["tbx"]>=0.00001)]["mx2"],0,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", data[(data["mx2"]>=i)&(data["kw"]==13)&(data["ndt"]>=0.00001)&(data["tbx"]>=0.00001)]["ndt"], r"$\mathit{Age - Mass, dataset: M_{donor}}$>="+str(i)+"${M_{sun}},NS$",str(i)+"AgeMassGT2WeightNS",htmlFolderLocation)
    plotSingle(data[(data["mx2"]>=i)&(data["kw"]==14)&(data["ndt"]>=0.00001)&(data["tbx"]>=0.00001)]["t1"],data[(data["mx2"]>=i)&(data["kw"]==14)&(data["ndt"]>=0.00001)&(data["tbx"]>=0.00001)]["mx2"],0,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", data[(data["mx2"]>=i)&(data["kw"]==14)&(data["ndt"]>=0.00001)&(data["tbx"]>=0.00001)]["ndt"], r"$\mathit{Age - Mass, dataset: M_{donor}}$>="+str(i)+"${M_{sun}},BH$",str(i)+"AgeMassGT2WeightBH",htmlFolderLocation)
    #     # 质量大于列表中的 Age - Mass, dataset: M2>2Msun     - Scatter fig
    #     # plotSingle(data[data["mx2"]>=i]["t1"],    data[data["mx2"]>=i]["mx2"],1,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]",0,r"$\mathit{Age - Mass, dataset: M_{donor}}$>="+str(i)+"${M_{sun}}$",    "AgeMassGT2Scatter",htmlFolderLocation)
    #     # 质量大于列表中的 Age - Mass, dataset: M2>2Msun     - Weight fig
    #     plotSingle(data[(data["mx2"]>=i)&(data["kw"]==13)]["t1"],data[(data["mx2"]>=i)&(data["kw"]==13)]["mx2"],0,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", data[(data["mx2"]>=i)&(data["kw"]==13)]["ndt"], r"$\mathit{Age - Mass, dataset: M_{donor}}$>="+str(i)+"${M_{sun}},NS$",str(i)+"AgeMassGT2WeightNS",htmlFolderLocation)
    #     plotSingle(data[(data["mx2"]>=i)&(data["kw"]==14)]["t1"],data[(data["mx2"]>=i)&(data["kw"]==14)]["mx2"],0,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]",data[(data["mx2"]>=i)&(data["kw"]==14)]["ndt"],r"$\mathit{Age - Mass, dataset: M_{donor}}$>="+str(i)+"${M_{sun}},BH$",str(i)+"AgeMassGT2WeightBH",htmlFolderLocation)
    #     # j+=1
    #     # 质量大于列表中的 mx2-lg(tbx)关系
    plotSingle(data[(data["mx2"]>=i)&(data["kw"]==13)&(data["ndt"]>=0.00001)]["mx2"], data[(data["mx2"]>=i)&(data["kw"]==13)&(data["ndt"]>=0.00001)]["tbx"].apply(lambda x:math.log10(x)),0,r"$\mathit{M_{donor}}$[${M_{sun}}$]",r"$\mathit{log P_{orb,cur}}$[d]",data[(data["mx2"]>=i)&(data["kw"]==13)&(data["ndt"]>=0.00001)]["ndt"],r"$\mathit{Mass - log(Period), dataset: M_{donor}}$>="+str(i)+"${M_{sun}}$,NS",str(i)+"-MasslgPeriodMGTNS"+str(i)+"Weight",htmlFolderLocation)
    plotSingle(data[(data["mx2"]>=i)&(data["kw"]==14)&(data["ndt"]>=0.00001)]["mx2"], data[(data["mx2"]>=i)&(data["kw"]==14)&(data["ndt"]>=0.00001)]["tbx"].apply(lambda x:math.log10(x)),0,r"$\mathit{M_{donor}}$[${M_{sun}}$]",r"$\mathit{log P_{orb,cur}}$[d]",data[(data["mx2"]>=i)&(data["kw"]==14)&(data["ndt"]>=0.00001)]["ndt"],r"$\mathit{Mass - log(Period), dataset: M_{donor}}$>="+str(i)+"${M_{sun}}$,BH",str(i)+"-MasslgPeriodMGTBH"+str(i)+"Weight",htmlFolderLocation)
        #     质量大于列表中,周期小于列表中的 mx2-lg(tbx)关系

    # for i in [2,5,10,20]:
    #     # 质量大于列表中的 Age - Mass, dataset: M2>2Msun     - Scatter fig
    #     plotSingle(data[data["mx2"]>=i]["t1"],    data[data["mx2"]>=i]["mx2"],1,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]",0,r"$\mathit{Age - Mass, dataset: M_{donor}}$>="+str(i)+"${M_{sun}}$",    "AgeMassGT2Scatter",htmlFolderLocation)
    #     # 质量大于列表中的 Age - Mass, dataset: M2>2Msun     - Weight fig
    #     plotSingle(data[data["mx2"]>=i]["t1"],    data[data["mx2"]>=i]["mx2"],0,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]",data[data["mx2"]>=i]["ndt"],r"$\mathit{Age - Mass, dataset: M_{donor}}$>="+str(i)+"${M_{sun}}$",    str(j)+"-AgeMassGT2Weight",htmlFolderLocation)
    #     j+=1
    #     # 质量大于列表中的 mx2-lg(tbx)关系
    #     plotSingle(data[data["mx2"]>=i]["mx2"], data[data["mx2"]>=i]["tbx"].apply(lambda x:math.log10(x)),0,r"$\mathit{M_{donor}}$[${M_{sun}}$]",r"$\mathit{log P_{orb,cur}}$[d]",data[data["mx2"]>=i]["ndt"],r"$\mathit{Mass - log(Period), dataset: M_{donor}}$>="+str(i)+"${M_{sun}}$",str(j)+"-MasslgPeriodMGT"+str(i)+"Weight",htmlFolderLocation)
    #     #     质量大于列表中,周期小于列表中的 mx2-lg(tbx)关系

    # #Age - Mass, dataset: All          - Scatter fig
    # plotSingle(data["t1"], data["mx2"], 1, r"$\mathit{Age}}$[Myrs]", r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", 0,"Age - Mass, dataset: All","1-AgeMassAllScatter",htmlFolderLocation)
    # #Age - Mass, dataset: All          - Weight fig
    # plotSingle(data["t1"], data["mx2"], 0, r"$\mathit{Age}}$[Myrs]", r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", data["ndt"], "Age - Mass, dataset: All", "2-AgeMassAllWeight",htmlFolderLocation)
    # #Age - Mass, dataset: NS           - Scatter fig
    # plotSingle(data[data["kw"]==13]["t1"], data[data["kw"]==13]["mx2"], 1, r"$\mathit{Age}}$[Myrs]", r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", 0, r"$\mathit{Age - Mass, dataset: NS}$", "3-AgeMassNSScatter",htmlFolderLocation)
    # #Age - Mass, dataset: NS           - Weight fig
    # plotSingle(data[data["kw"]==13]["t1"], data[data["kw"]==13]["mx2"], 0, r"$\mathit{Age}}$[Myrs]", r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", data[data["kw"]==13]["ndt"],r"$\mathit{Age - Mass, dataset: NS}$", "4-AgeMassNSWeight",htmlFolderLocation)
    # #Age - Mass, dataset: BH           - Scatter fig
    # plotSingle(data[data["kw"]==14]["t1"], data[data["kw"]==14]["mx2"], 1, r"$\mathit{Age}}$[Myrs]", r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", 0, r"$\mathit{Age - Mass, dataset: BH}$", "5-AgeMassBHScatter",htmlFolderLocation)
    # #Age - Mass, dataset: BH           - Weight fig
    # plotSingle(data[data["kw"]==14]["t1"], data[data["kw"]==14]["mx2"], 0, r"$\mathit{Age}}$[Myrs]", r"$\mathit{M_{d,ini}}$[${M_{sun}}$]", data[data["kw"]==14]["ndt"],r"$\mathit{Age - Mass, dataset: BH}$", "6-AgeMassBHWeight",htmlFolderLocation)
    # #Mass - log(Period), dataset: All  - Scatter fig
    # plotSingle(data["mx2"], data["tbx"].apply(lambda x:math.log10(x)), 1, r"$\mathit{M_{donor}}$[${M_{sun}}$]", r"$\mathit{log P_{orb,cur}}$[d]", 0, r"$\mathit{Mass - log(Period), dataset: All}$", "7-MasslgPeriodScatter",htmlFolderLocation)
    # #Mass - log(Period), dataset: All  - Weight fig
    # plotSingle(data["mx2"], data["tbx"].apply(lambda x:math.log10(x)), 0, r"$\mathit{M_{donor}}$[${M_{sun}}$]", r"$\mathit{log P_{orb,cur}}$[d]", data["ndt"], r"$\mathit{Mass - log(Period), dataset: All}$", "8-MasslgPeriodWeight",htmlFolderLocation)
    # # #Mass - log(Period), dataset: NS   - Weight fig
    # plotSingle(data[data["kw"]==13]["mx2"], data[data["kw"]==13]["tbx"].apply(lambda x:math.log10(x)), 0, r"$\mathit{M_{donor}}$[${M_{sun}}$]", r"$\mathit{log P_{orb,cur}}$[d]", data[data["kw"]==13]["ndt"], r"$\mathit{Mass - log(Period), dataset: NS}$", "9-MasslgPeriodNSWeight",htmlFolderLocation)
    # # #Mass - log(Period), dataset: BH   - Weight fig
    # plotSingle(data[data["kw"]==14]["mx2"], data[data["kw"]==14]["tbx"].apply(lambda x:math.log10(x)), 0, r"$\mathit{M_{donor}}$[${M_{sun}}$]", r"$\mathit{log P_{orb,cur}}$[d]",data[data["kw"]==14]["ndt"], r"$\mathit{Mass - log(Period), dataset: BH}$", "10-MasslgPeriodBHWeight",htmlFolderLocation)
    # j=11
    # for i in [2,5,10,20]:
    #     # 质量大于列表中的 Age - Mass, dataset: M2>2Msun     - Scatter fig
    #     # plotSingle(data[data["mx2"]>=i]["t1"],    data[data["mx2"]>=i]["mx2"],1,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]",0,r"$\mathit{Age - Mass, dataset: M_{donor}}$>="+str(i)+"${M_{sun}}$",    "AgeMassGT2Scatter",htmlFolderLocation)
    #     # 质量大于列表中的 Age - Mass, dataset: M2>2Msun     - Weight fig
    #     plotSingle(data[data["mx2"]>=i]["t1"],    data[data["mx2"]>=i]["mx2"],0,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]",data[data["mx2"]>=i]["ndt"],r"$\mathit{Age - Mass, dataset: M_{donor}}$>="+str(i)+"${M_{sun}}$",    str(j)+"-AgeMassGT2Weight",htmlFolderLocation)
    #     j+=1
    #     # 质量大于列表中的 mx2-lg(tbx)关系
    #     plotSingle(data[data["mx2"]>=i]["mx2"], data[data["mx2"]>=i]["tbx"].apply(lambda x:math.log10(x)),0,r"$\mathit{M_{donor}}$[${M_{sun}}$]",r"$\mathit{log P_{orb,cur}}$[d]",data[data["mx2"]>=i]["ndt"],r"$\mathit{Mass - log(Period), dataset: M_{donor}}$>="+str(i)+"${M_{sun}}$",str(j)+"-MasslgPeriodMGT"+str(i)+"Weight",htmlFolderLocation)
    #     #     质量大于列表中,周期小于列表中的 mx2-lg(tbx)关系
    # for i in [2,5,10,20]:
    #     for j in [10,100,1000,10000]:
    #         plotSingle(data[(data["mx2"]>=i)&(data["tbx"]<=j)]["mx2"], data[(data["mx2"]>=i)&(data["tbx"]<=j)]["tbx"].apply(lambda x:math.log10(x)),0,r"$\mathit{M_{donor}}$[${M_{sun}}$]",r"$\mathit{log P_{orb,cur}}$[d]",data[(data["mx2"]>=i)&(data["tbx"]<=j)]["ndt"],r"$\mathit{Mass - log(Period), dataset: M_{donor}}$>="+str(i)+"${M_{sun}}$, Period<="+str(j)+"-d",str(j)+"-MasslgPeriodMGT"+str(i)+"PLT"+str(j)+"-Weight",htmlFolderLocation)
    #         j+=1

    # # NS/BH 演化时间小于列表中的Age-Mass关系
    # for i in [10,15,20,25]:
    #     if len(data[(data["kw"]==13)&(data["t1"]<=i)]["t1"]) > 0:
    #         plotSingle(data[(data["kw"]==13)&(data["t1"]<=i)]["t1"],    data[(data["kw"]==13)&(data["t1"]<=i)]["mx2"],0,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]",           data[(data["kw"]==13)&(data["t1"]<=i)]["ndt"],r"$\mathit{Age - Mass, dataset: NS, Age<="+str(i)+"Myrs}$", str(j)+"-AgeMassNSALT"+str(i),htmlFolderLocation)
    # for i in [10,15,20,25]:
    #     if len(data[(data["kw"]==14)&(data["t1"]<=i)]["t1"]) > 0:
    #         plotSingle(data[(data["kw"]==14)&(data["t1"]<=i)]["t1"],    data[(data["kw"]==14)&(data["t1"]<=i)]["mx2"],0,  r"$\mathit{Age}}$[Myrs]",   r"$\mathit{M_{d,ini}}$[${M_{sun}}$]",           data[(data["kw"]==14)&(data["t1"]<=i)]["ndt"],r"$\mathit{Age - Mass, dataset: BH, Age<="+str(i)+"Myrs}$", str(j)+"-AgeMassBHALT"+str(i),htmlFolderLocation)

    # plotDistribution(data["mx2"],data["ndt"],r'$Z=0.02$',(2,60),"91-Mass_donor_Ndtt2-60","Mass_donor","N",htmlFolderLocation)
    # plotDistribution(data["mx2"],data["ndt"],r'$Z=0.02$',(5,50),"92-Mass_donor_Ndtt5-50","Mass_donor","N",htmlFolderLocation)
    # plotDistribution(data["tbx"].apply(lambda x:math.log10(x)),data["ndt"],r'$Z=0.02$',(0,4),"93-log(Period)_Ndtt0-4","log(Period)","N",htmlFolderLocation)
    # plotDistribution(data["tbx"].apply(lambda x:math.log10(x)),data["ndt"],r'$Z=0.02$',(0,3),"94-log(Period)_Ndtt0-3","log(Period)","N",htmlFolderLocation)
    # plotDistribution(data["tbx"].apply(lambda x:math.log10(x)),data["ndt"],r'$Z=0.02$',(0,2),"95-log(Period)_Ndtt0-2","log(Period)","N",htmlFolderLocation)
    # plotDistribution(data["tbx"].apply(lambda x:math.log10(x)),data["ndt"],r'$Z=0.02$',(0,1),"96-log(Period)_Ndtt0-1","log(Period)","N",htmlFolderLocation)

    return plotFileNameList

