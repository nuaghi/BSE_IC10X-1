import os
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math
import datetime
import subprocess
import sys
import numpy as np
import gc
from matplotlib import colors

def nowtime():
    return datetime.datetime.now().strftime('%m%d-%H%M%S ')

def onetwentieth(i):
    if int(i)>0:
        j =  i*100//5000
        if j>=1000000:
            return 1000000
        elif j > 0:
            return j
        else:
            return 1
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
        exit(1)
    try:
        # print("grep "+dataRunTime+" "+dataFolderLocation+"rdc.num | awk '{print $4}'")
        # exit(0)
        totalFormationCount=int(subprocess.getoutput("grep "+dataRunTime+" "+dataFolderLocation+"rdc.num | awk '{print $4}'"))
        if totalFormationCount > 0:
            htmlFolderLocation=dataFolderLocation+dataRunTime+"_"+str(totalFormationCount)+"/"
        else:
            htmlFolderLocation=dataFolderLocation+dataRunTime+"/"
    except (NameError, IndexError) as e:
        print("Error content: ", e)
        exit(1)

    os.system("cp "+dataFolderLocation+"/jquery.js "+htmlFolderLocation)
    dataFileLocation=dataFolderLocation+"N"+dataRunTime+".csv"
    if not os.path.exists(dataFileLocation):
        print(nowtime()+"FATAL ERROR: [File '"+dataFileLocation+"' Not Found.] Exit.")
        exit(1)
    elif not os.path.exists(htmlFolderLocation):
        os.mkdir(htmlFolderLocation)
    del dataRunTime,totalFormationCount,htmlFolderLocation,dataFileLocation
    gc.collect()
    return dataFolderLocation

plotFileNameList=[]
def plotSingle(xdata,ydata,scale,xl,yl,wei,ptitle,fname,htmlFolderLocation):
    if scale==0:
        plt.hist2d(xdata,ydata,bins=25,density=50,weights=wei,norm=LogNorm())
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

def plotSingleAgeMassDonor(data,ptitle,fname,htmlFolderLocation):
    dataLength=len(data)
    if dataLength > 0:
        fig, ax = plt.subplots()
        cmap = plt.cm.get_cmap('viridis')
        cmap.set_under(color='white')
        hist = ax.hist2d(data["t1"],data["mx2"],bins=50, weights=data["ndt"],norm=None, cmap=cmap)
        cb = fig.colorbar(hist[3], ax=ax)
        cb.ax.set_ylabel('N')
        hist[3].set_clim(0.0001, np.max(hist[0]))
        lenListSetDataI=len(list(set(data["i"])))
        DataNdt=list(data["ndt"])
        listDataNdt=[sum(DataNdt),min(DataNdt),max(DataNdt)]
        plt.title("Age-Mass,dataset:"+ptitle+" ["+str(dataLength)+"->"+str(lenListSetDataI)+"]\nN: Total: "+str(round(listDataNdt[0],4))+" Section: ["+str(round(listDataNdt[1],4))+" , "+str(round(listDataNdt[2],4))+"], Average: "+str(round(listDataNdt[0]/lenListSetDataI,4)))
        del lenListSetDataI,DataNdt,listDataNdt
        plt.savefig(htmlFolderLocation+fname)
        plt.close()
        plotFileNameList.append(fname)
        print(nowtime()+"Plot: "+fname)
        del cmap,fig,ax,cb,hist
        gc.collect
    else:
        print(nowtime()+"[WARNING] Empty Data: "+fname)
        plt.hist2d([0],[0],bins=25,density=50,weights=[1],norm=LogNorm())
        plt.xlabel(r"$\mathit{Age}}$[Myrs]")
        plt.ylabel(r"$\mathit{M_{d,ini}}$[${M_{sun}}$]")
        plt.title(ptitle+" [0]")
        plt.savefig(htmlFolderLocation+fname)
        plt.close()
        plotFileNameList.append(fname)
    del data,ptitle,fname,dataLength,htmlFolderLocation
    gc.collect()

def plotSingleMassDonorLogPeriod(data,ptitle,fname,htmlFolderLocation):
    try:
        dataLength=len(data)
        if dataLength > 0:
            print(nowtime()+"Plot: "+fname)
            lenListSetDataI=len(list(set(data["i"])))
            plt.hist2d(data["mx2"],data["tbx"].apply(lambda x:math.log10(x)),bins=25,density=50,weights=data["ndt"],norm=LogNorm())
            DataNdt=list(data["ndt"])
            listDataNdt=[sum(DataNdt),min(DataNdt),max(DataNdt)]
            subtitle=ptitle+" ["+str(dataLength)+"->"+str(lenListSetDataI)+"]\nN: Total: "+str(round(listDataNdt[0],4))+" Section: ["+str(round(listDataNdt[1],4))+" , "+str(round(listDataNdt[2],4))+"], Average: "+str(round(listDataNdt[0]/lenListSetDataI,4))
            del data,DataNdt
            plt.colorbar()
            plt.title(r"$\mathit{M2-lg(P),dataset:}$"+subtitle)
            del listDataNdt,subtitle
        else:
            del data
            print(nowtime()+"[WARNING] Empty Data: "+fname)
            plt.hist2d([0],[0],bins=25,density=50,weights=[1],norm=LogNorm())
            plt.title(r"$\mathit{M2-lg(P),dataset:}$"+ptitle+" [0]")
        plt.xlabel(r"$\mathit{M_{donor}}$[${M_{sun}}$]")
        plt.ylabel(r"$\mathit{log P_{orb,cur}}$[d]")
        plt.savefig(htmlFolderLocation+fname)
        plt.close()
        plotFileNameList.append(fname)
        del ptitle,fname,htmlFolderLocation,dataLength
        gc.collect()
    except (NameError, IndexError) as e:
        print("Error content: ", e)

def plotDistribution(xdata,weights,range,title,xlabel,ylabel,htmlFolderLocation):
    try:
        dataLength=len(xdata)
        if dataLength > 0:
            print(nowtime()+"Plot: "+title)
            plt.hist(xdata, bins=50,histtype='step',weights=weights, color='tomato', linewidth=1.5,label=r'$Z=0.004$',range=range)
        else:
            print(nowtime()+"[WARNING] Empty Data: "+title)
            plt.hist([0], bins=50,histtype='step',weights=[1], color='tomato', linewidth=1.5,label=r'$Z=0.004$',range=range)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(htmlFolderLocation+title)
        plt.close()
        plotFileNameList.append(title)
        del xdata,weights,range,title,xlabel,ylabel,htmlFolderLocation
        gc.collect()
    except (NameError, IndexError) as e:
        print(nowtime()+"Error content: ", e)

def plotMain(data,htmlFolderLocation):
    data=data[data["tbx"]>0]
    Num=1
    plotSingleAgeMassDonor(data, "All", str(Num)+"-AgeMassAllWeight",htmlFolderLocation)
    # Num+=1
    # plotSingleAgeMassDonor(data[(data["ndt"]>=0.00000001)&(data["tbx"]>=0.000001)], "N>=10^-8,tbx>=10^-6d", str(Num)+"-AgeMassReasonableAll",htmlFolderLocation)
    # Num+=1
    # plotSingleAgeMassDonor(data[(data["kw"]==13)&(data["ndt"]>=0.00000001)&(data["tbx"]>=0.000001)], "N>=10^-8 tbx>=10^-6d,NS", str(Num)+"-AgeMassReasonableNS",htmlFolderLocation)
    # Num+=1
    # plotSingleAgeMassDonor(data[(data["kw"]==14)&(data["ndt"]>=0.00000001)&(data["tbx"]>=0.000001)], "N>=10^-8 tbx>=10^-6d,BH", str(Num)+"-AgeMassReasonableRBH",htmlFolderLocation)
    # for i in [2,5,10]:
    #     Num+=1
    #     plotSingleAgeMassDonor(data[(data["kw"]==13)&(data["mx2"]>=i)], "Mass2>="+str(i)+",NS", str(Num)+"-AgeMass2GT"+str(i)+"NS",htmlFolderLocation)
    #     Num+=1
    #     plotSingleAgeMassDonor(data[(data["kw"]==14)&(data["mx2"]>=i)], "Mass2>="+str(i)+",BH", str(Num)+"-AgeMass2GT"+str(i)+"BH",htmlFolderLocation)
    #     for j in [10,20,50,100]:
    #         Num+=1
    #         plotSingleAgeMassDonor(data[(data["kw"]==13)&(data["mx2"]>=i)&(data["t1"]<=j)], "Mass2>="+str(i)+",Age<="+str(j)+",NS", str(Num)+"-AgeLT"+str(j)+"Mass2GT"+str(i)+"NS",htmlFolderLocation)
    #         Num+=1
    #         plotSingleAgeMassDonor(data[(data["kw"]==14)&(data["mx2"]>=i)&(data["t1"]<=j)], "Mass2>="+str(i)+",Age<="+str(j)+",BH", str(Num)+"-AgeLT"+str(j)+"Mass2GT"+str(i)+"BH",htmlFolderLocation)
    # Num+=1
    # plotSingleMassDonorLogPeriod(data[(data["kw"]==13)&(data["ndt"]>=0.00000001)&(data["tbx"]>=0.000001)],"N>=10^-8,tbx>=10^-6d,NS",str(Num)+"-Mass2lgPeriodReasonableNS",htmlFolderLocation)
    # Num+=1
    # plotSingleMassDonorLogPeriod(data[(data["kw"]==14)&(data["ndt"]>=0.00000001)&(data["tbx"]>=0.000001)],"N>=10^-8,tbx>=10^-6d,BH",str(Num)+"-Mass2lgPeriodReasonableBH",htmlFolderLocation)
    # for i in [2,5,10]:
    #     for j in [10,15,20]:
    #         for k in [1000,10000]:
    #             Num+=1
    #             plotSingleMassDonorLogPeriod(data[(data["kw"]==13)&(data["mx2"]>=i)&(data["t1"]<=j)&(data["tbx"]<=k)], "M2>="+str(i)+",Age<="+str(j)+",Period<="+str(k)+", NS", str(Num)+"-Mass2GT"+str(i)+"AgeLT"+str(j)+"lgPeriodLT"+str(k)+"NS",htmlFolderLocation)
    #             Num+=1
    #             plotSingleMassDonorLogPeriod(data[(data["kw"]==14)&(data["mx2"]>=i)&(data["t1"]<=j)&(data["tbx"]<=k)], "M2>="+str(i)+",Age<="+str(j)+",Period<="+str(k)+", BH", str(Num)+"-Mass2GT"+str(i)+"AgeLT"+str(j)+"lgPeriodLT"+str(k)+"BH",htmlFolderLocation)
    # Num+=1
    # plotDistribution(data["mx2"],data["ndt"],(0,100),str(Num)+"-Mass_donor_N0-100",r"$\mathit{M_{donor}}$[${M_{sun}}$]",r"$\mathit{N}$]",htmlFolderLocation)
    # Num+=1
    # plotDistribution(data["mx2"],data["ndt"],(0,40),str(Num)+"-Mass_donor_N0-40",r"$\mathit{M_{donor}}$[${M_{sun}}$]",r"$\mathit{N}$]",htmlFolderLocation)
    # Num+=1
    # plotDistribution(data["mx2"],data["ndt"],(0,20),str(Num)+"-Mass_donor_N0-50",r"$\mathit{M_{donor}}$[${M_{sun}}$]",r"$\mathit{N}$]",htmlFolderLocation)
    # Num+=1
    # plotDistribution(data["mx2"],data["ndt"],(0,10),str(Num)+"-Mass_donor_N0-10",r"$\mathit{M_{donor}}$[${M_{sun}}$]",r"$\mathit{N}$]",htmlFolderLocation)
    # Num+=1
    # plotDistribution(data["tbx"].apply(lambda x:math.log10(x)),data["ndt"],(-4,5),str(Num)+"-log(Period)_N-4-5",r"$\mathit{log P_{orb,cur}}$[d]",r"$\mathit{N}$]",htmlFolderLocation)
    # Num+=1
    # plotDistribution(data["tbx"].apply(lambda x:math.log10(x)),data["ndt"],(-2,4),str(Num)+"-log(Period)_N-2-4",r"$\mathit{log P_{orb,cur}}$[d]",r"$\mathit{N}$]",htmlFolderLocation)
    # Num+=1
    # plotDistribution(data["tbx"].apply(lambda x:math.log10(x)),data["ndt"],(0,3),str(Num)+"-log(Period)_N0-3",r"$\mathit{log P_{orb,cur}}$[d]",r"$\mathit{N}$]",htmlFolderLocation)
    # Num+=1
    # plotDistribution(data["tbx"].apply(lambda x:math.log10(x)),data["ndt"],(1,3),str(Num)+"-log(Period)_N1-3",r"$\mathit{log P_{orb,cur}}$[d]",r"$\mathit{N}$]",htmlFolderLocation)
    return plotFileNameList

