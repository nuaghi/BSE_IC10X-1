import os
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math
import datetime
import subprocess
import sys
import numpy as np
import gc
from alive_progress import alive_bar
from matplotlib.pyplot import MultipleLocator
import pandas as pd
import matplotlib.colors as mcolors
from matplotlib.gridspec import GridSpec

presentlist=[
    ["blue",    "solid",    "Stable Mass Transfer"],
    ["orange",  "solid",    "Common Envelope"],
    ["black",   "solid",    "Other Channels"]
]
# "Stable Mass Transfer",
listname=["Stable Mass Transfer","Common Envelope","Other Channels"]

def nowtime():
    return datetime.datetime.now().strftime('%m%d-%H%M%S ')

def printformat(i1,i2,content):
    print(nowtime()+str(i1)+"."+str(i2)+str(content))
    i2=i2+1
    return i2

def onetwentieth(i):
    return(min(1000000,i*100//5000)) if i*100//5000 > 0 else 1

def pltxyticksnameclose(plt,xticksftsz,yticksftsz,name):
    plt.xlim(0,)
    plt.ylim(0.00001,)
    plt.xticks(fontsize=xticksftsz)
    plt.yticks(fontsize=yticksftsz)
    plt.savefig(name)
    plt.close()

def colorbar(fig, gs, ax, plt, weight):
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    cbar_ax = fig.add_subplot(gs[0, :])
    cbar = fig.colorbar(weight, cax=cbar_ax, orientation='horizontal')
    cbar.set_label('Number', fontsize=17)
    cbar.ax.xaxis.set_label_position('top')
    cbar.ax.xaxis.set_ticks_position('top')
    cbar.ax.tick_params(labelsize=14)

#检查数据文件及部分参数，返回路径等
def locationCheck(dataRunTime):
    LocationList=[["/Files/git/data/","Ubuntu"],["/Users/nuaghi/Files/BSE_workbench/data/","MacOS"],["/data2/wgy/git/data/","Ubuntu228"],["/Files/data/","Ubuntu125-BaoGuoMa"],["/mnt/d/Files/BSE_workbench/data/","WinUbuntu"],["/Files/BSE_workbench/data/","lenovo@GranduateRoom"]]
    for i in LocationList:
        if os.path.exists(i[0]):
            dataFolderLocation=i[0]
            print(nowtime()+"OS: "+i[1])
            break

    #dataParas:rdc.num记录全部内容
    dataParas=[subprocess.getoutput("grep "+dataRunTime[i]+" "+dataFolderLocation+"rdc.num |awk -F '[,:]' '{for(i=1;i<=NF;i++)if(i%2==0) print $(i-1),\":\",$i}' | tr \"\n\" \",\"").split(",") for i in range(len(dataRunTime))]

    #rdcContent(数据集总量，alphaCE值), dataFileLocation(小文件:仅记录kstar和ces,中文件:CO+WR源,大文件:能形成目标源的全部数据)
    rdcContent,dataFileLocation=[[],[],[]],[[],[],[]]
    for j in range(len(dataRunTime)):
        rdcContent[j].append(subprocess.getoutput("grep "+dataRunTime[j]+" "+dataFolderLocation+"rdc.num | awk -F '[,:]' '{print $2}'"))
        if bool(rdcContent[j][0].strip()):
            rdcContent[j].append(round(float(subprocess.getoutput("grep "+dataRunTime[j]+" "+dataFolderLocation+"rdc.num | awk -F '[,:]' '{print $10}'")),2))
            rdcContent[j].extend(dataParas[j])
        else:
            print(nowtime()+"FATAL ERROR: [Cannot find content "+str(dataRunTime[j])+" in rdc.num.] Exit.")
            exit(1)
        dataFileLocation[0].append(dataFolderLocation+"N"+dataRunTime[j]+"_"+str(rdcContent[0][0])+"ss.csv")
        dataFileLocation[1].append(dataFolderLocation+"N"+dataRunTime[j]+"_"+str(rdcContent[0][0])+"s.csv")
        dataFileLocation[2].append(dataFolderLocation+"N"+dataRunTime[j]+"_"+str(rdcContent[0][0])+".csv")

        for k in range(2):
            if not os.path.exists(dataFileLocation[k][-1]):
                print(nowtime()+"FATAL ERROR: [File '"+dataFileLocation[k][-1]+"' Not Found.] Exit.")
                exit(1)
        if not os.path.exists(dataFileLocation[2][-1]):
            print(nowtime()+"WARNING: [File '"+dataFileLocation[k][-1]+"' Not Found.]")

    if rdcContent[0][0] == rdcContent[-1][0]:
        htmlFolderLocation = dataFolderLocation+str(rdcContent[0][0])+"_["
        for i in range(len(rdcContent)):
            htmlFolderLocation += "-"+str(rdcContent[i][1])
        htmlFolderLocation+="]-["
        for i in range(len(dataRunTime)):
            htmlFolderLocation += "-"+dataRunTime[i]
        htmlFolderLocation+="]/"
        if not os.path.exists(htmlFolderLocation):
            os.mkdir(htmlFolderLocation)
        os.system("cp "+dataFolderLocation+"/jquery.js "+htmlFolderLocation)
    else:
        print(nowtime()+"FATAL ERROR: "+str(rdcContent)+"_"+str(dataRunTime[0])+" Exit.")
        exit(1)
    gc.collect()
    return dataFolderLocation,dataFileLocation,htmlFolderLocation

#演化时长-WR星质量 分布图
def plotAgeMassDonorKw(data,fnamelist,htmlFolderLocation,AlphaCElist):
    content = [
        ["NS", 13],
        ["BH", 14]
    ]
    fig = plt.figure(figsize=(16, 9))
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.05, right=0.98, hspace=0)
    gs = GridSpec(3, 3, width_ratios=[1, 1, 1], height_ratios=[0.1, 1, 1], hspace=0, wspace=0)

    for i in range(len(fnamelist)):
        for j in range(len(AlphaCElist)):
            ax = fig.add_subplot(gs[i+1, j])
            cmap = plt.cm.get_cmap('viridis')
            cmap.set_under(color='white')
            hist = ax.hist2d(data[j][data[j]["kw"]==content[i][1]]["t1"],data[j][data[j]["kw"]==content[i][1]]["mx2"],bins=40,weights=data[j][data[j]["kw"]==content[i][1]]["ndt"], range=[[0,65], [0,50]], norm=LogNorm(), cmap=cmap)
            hist[3].set_clim(0.001, np.max(hist[0]))
            ax.set_xlim(0,)
            ax.set_ylim(0,49)
            plt.text(20,45,r"Accretor: "+content[i][0]+", $α_{CE}=$"+str(AlphaCElist[j]),fontsize=18)
            ax.fill_between([0,10],[17,17],[35,35], color='gray', alpha=0.3)
            if j == 0:
                plt.ylabel(r"$\mathrm{M_{WR} ({M_{\odot}})}$", fontsize=16)
            else:
                ax.set_yticklabels([])
            if i == 1:
                plt.xlabel(r"Age (Myr)", fontsize=16)
            else:
                ax.set_xticklabels([])
    colorbar(fig, gs, ax, plt, hist[3])
    plt.savefig(htmlFolderLocation+fnamelist[0])

#演化时长-WR星质量 分布图 分类：演化过程
def plotAgeMassDonor(data,fname,htmlFolderLocation,AlphaCE=[],listI=[]):
    fig = plt.figure(figsize=(16, 9))
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.05, right=0.98, hspace=0)
    gs = GridSpec(3, 3, width_ratios=[1, 1, 1], height_ratios=[0.1, 1, 1], hspace=0, wspace=0)
    for i in range(1,3):
        for j in range(len(AlphaCE)):
            if len(listI[j][i])>0:
                ax = fig.add_subplot(gs[i, j])
                cmap = plt.cm.get_cmap('viridis')
                cmap.set_under(color='white')
                hist = ax.hist2d(data[j][data[j]["i"].isin(listI[j][i])]["t1"],data[j][data[j]["i"].isin(listI[j][i])]["mx2"],bins=40,weights=data[j][data[j]["i"].isin(listI[j][i])]["ndt"],range=[[0, 53], [0,50]],norm=LogNorm(), cmap=cmap)
                if np.max(hist[0])>0.001:
                    hist[3].set_clim(0.001, np.max(hist[0]))
                    ax.set_xlim(0,49)
                    ax.set_ylim(0,49)
                    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
                    plt.text(10,45,r"$α_{CE}=$"+str(AlphaCE[j])+", "+listname[i],fontsize=15)
                    ax.fill_between([0,10],[17,17],[35,35], color='gray', alpha=0.3)
                    if i == 2:
                        plt.xlabel(r"Age (Myr)", fontsize=15)
                    else:
                        ax.set_xticklabels([])
                    if j == 0:
                        plt.ylabel(r"$\mathrm{M_{WR} ({M_{\odot}})}$", fontsize=15)
                    else:
                        ax.set_yticklabels([])
                    plt.xticks(fontsize=12)
                    plt.yticks(fontsize=12)
    colorbar(fig, gs, ax, plt, hist[3])
    plt.savefig(htmlFolderLocation+fname)


#演化时长-WR星质量 分布图 分类：演化过程
def plotAgeMassDonorSingle(data,fname,htmlFolderLocation,AlphaCE=1,listI=[]):
    dataLength=len(data)
    listname=["Stable Mass Transfer"]
    for i in range(1):
        if len(listI[i])>0:
            print(nowtime()+"Plot: "+fname+"-"+listname[i]+"-a"+str(int(AlphaCE)))
            fig, ax = plt.subplots()
            cmap = plt.cm.get_cmap('viridis')
            cmap.set_under(color='white')
            hist = ax.hist2d(data[data["i"].isin(listI[i])]["t1"],data[data["i"].isin(listI[i])]["mx2"],bins=40,weights=data[data["i"].isin(listI[i])]["ndt"],range=[[0, 50], [0,50]],norm=LogNorm(), cmap=cmap)
            if np.max(hist[0])>0.001:
                hist[3].set_clim(0.001, np.max(hist[0]))
                cb = fig.colorbar(hist[3], ax=ax)
                cb.ax.set_ylabel('N', fontsize=13)
                cb.ax.tick_params(labelsize=12)
                ax.set_xlim(0,50)
                ax.set_ylim(0,50)
                DataNdt=list(data[data["i"].isin(listI[i])]["ndt"])
                plt.text(10,45,listname[i],fontsize=15)
                ax.fill_between([0,10],[17,17],[35,35], color='gray', alpha=0.3)
                plt.xlabel(r"$Age(Myr)$", fontsize=13)
                plt.ylabel(r"$M_{WR}({M_{\odot}}$)", fontsize=13)
                plt.xticks(fontsize=12)
                plt.yticks(fontsize=12)
                plt.savefig(htmlFolderLocation+fname)
            plt.close()
    del data,fname,dataLength,htmlFolderLocation
    gc.collect()


#WR星质量-lg轨道周期
def plotMassDonorLogPeriod(data,fname,htmlFolderLocation,AlphaCE=1,listI=[], agesign = 0):
    fig = plt.figure(figsize=(16, 9))
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.05, right=0.98, hspace=0)
    gs = GridSpec(3, 3, width_ratios=[1, 1, 1], height_ratios=[0.1, 1, 1], hspace=0, wspace=0)
    # fig = plt.figure(figsize=(18, 14))
    # plt.subplots_adjust(top=0.94, bottom=0.05, left=0.05, right=0.98, hspace=0)
    # gs = GridSpec(3, 3, width_ratios=[1, 1, 1], height_ratios=[0.1, 1, 1], hspace=0, wspace=0)
    for i in range(1,3):
        for j in range(len(AlphaCE)):
            if len(listI[j][i])>0:
                ax = fig.add_subplot(gs[i, j])
                cmap = plt.cm.get_cmap('viridis')
                cmap.set_under(color='white')
                hist = ax.hist2d(data[j][data[j]["i"].isin(listI[j][i])]["mx2"], data[j][data[j]["i"].isin(listI[j][i])]["tbx"].apply(lambda x:math.log10(x)), bins=30, weights=data[j][data[j]["i"].isin(listI[j][i])]["ndt"],range=[[0, 50], [-2, 5]],norm=LogNorm(), cmap=cmap)
                if np.max(hist[0])>0.001:
                    hist[3].set_clim(0.001, np.max(hist[0]))
                    ax.set_xlim(0,49)
                    ax.set_ylim(-2,4.9)
                    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
                    if i == 2:
                        plt.xlabel(r"$\mathrm{{M_{WR}} ({M_{\odot}})}$", fontsize=15)
                    else:
                        ax.set_xticklabels([])
                    if j == 0:
                        plt.ylabel(r"$\mathrm{{log P_{orb}} (d)}$", fontsize=15)
                    else:
                        ax.set_yticklabels([])

                    if agesign == 1:
                        plt.errorbar(26, 0.163, xerr=[[9],[9]], yerr=[[0],[0]], ecolor="red", ms=4, marker='o', markerfacecolor='red', mec="red", elinewidth=2, capsize=3, capthick=3)
                        plt.text(36, 0, "IC 10 X-1", fontsize=15, color="red")
                    else:
                        plt.errorbar(26, 0.135, xerr=[[5],[7]], yerr=[[0],[0]], ecolor="red",  ms=6, marker='o', markerfacecolor='red', elinewidth=2, mec="red", capsize=3, capthick=3)
                        plt.text(23,-0.4,"NGC 300 X-1",fontsize=15, color="red")
                        plt.errorbar(19, 0.9138, xerr=[[1],[1]], yerr=[[0],[0]], ecolor="red",  ms=6, marker='o', markerfacecolor='red', elinewidth=3, mec="red", capsize=3, capthick=3)
                        plt.text(10, 1.1, "M 101 ULX-1",fontsize=15, color="red")
                        plt.errorbar(9.2, -0.699, xerr=[[2],[8.3]], yerr=[[0],[0]], ecolor="red", ms=6, marker='o', markerfacecolor='red', mec="red", elinewidth=2, capsize=3, capthick=3)
                        plt.text(10, -1.3,"Cyg X-3",fontsize=15, color="red")
                    plt.text(18,-1.8,r"$α_{CE}=$"+str(AlphaCE[j])+", "+listname[i],fontsize=15)
    colorbar(fig, gs, ax, plt, hist[3])
    plt.savefig(htmlFolderLocation+fname)

#WR星质量-lg轨道周期
def plotMassDonorLogPeriodSingle(data,fname,htmlFolderLocation,AlphaCE=1,listI=[], agesign = 1):
    dataLength=len(data)
    listname=["Stable Mass Transfer"]
    if dataLength > 0:
        for i in range(1):
            if len(listI[i])>0:
                print(nowtime()+"Plot: "+fname+"-"+listname[i]+"-a"+str(AlphaCE))
                fig, ax = plt.subplots()
                plt.subplots_adjust(top=0.95, bottom=0.13, left=0.12, right=0.95, wspace=0)
                gs = GridSpec(1, 2, width_ratios=[1, 0.1],wspace=0)
                cmap = plt.cm.get_cmap('viridis')
                cmap.set_under(color='white')
                hist = ax.hist2d(data[data["i"].isin(listI[i])]["mx2"],data[data["i"].isin(listI[i])]["tbx"].apply(lambda x:math.log10(x)),bins=20,weights=data[data["i"].isin(listI[i])]["ndt"],range=[[0, 50], [-2, 5]],norm=LogNorm(), cmap=cmap)
                hist[3].set_clim(0.001, np.max(hist[0]))
                if np.max(hist[0])>0.00001:
                    cb = fig.colorbar(hist[3], ax=ax)
                    cb.ax.set_ylabel('Number', fontsize=17)
                    cb.ax.tick_params(labelsize=12)
                    ax.set_xlim(0,50)
                    ax.set_ylim(-2,5)
                    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
                    if agesign == 1:
                        plt.errorbar(26, 0.163, xerr=[[9],[9]], yerr=[[0],[0]], ecolor="red", ms=4, marker='o', markerfacecolor='red', mec="red", elinewidth=2, capsize=3, capthick=3)
                        plt.text(36, 0, "IC 10 X-1", fontsize=15, color="red")
                    else:
                        plt.errorbar(26, 0.135, xerr=[[5],[7]], yerr=[[0],[0]], ecolor="red",  ms=6, marker='o', markerfacecolor='red', elinewidth=2, mec="red", capsize=3, capthick=3)
                        plt.text(23,-0.4,"NGC 300 X-1",fontsize=15, color="red")
                        plt.errorbar(19, 0.9138, xerr=[[1],[1]], yerr=[[0],[0]], ecolor="red",  ms=6, marker='o', markerfacecolor='red', elinewidth=3, mec="red", capsize=3, capthick=3)
                        plt.text(10, 1.1, "M 101 ULX-1",fontsize=15, color="red")
                        plt.errorbar(9.2, -0.699, xerr=[[2],[8.3]], yerr=[[0],[0]], ecolor="red", ms=6, marker='o', markerfacecolor='red', mec="red", elinewidth=2, capsize=3, capthick=3)
                        plt.text(10, -1.3,"Cyg X-3",fontsize=15, color="red")
                    if i == 0:
                        plt.text(20,-1.8,listname[i],fontsize=15)
                    else:
                        plt.text(1,4.5,listname[i],fontsize=15)
                    plt.xlabel(r"$\mathrm{{M_{WR}} ({M_{\odot}})}$", fontsize=15)
                    plt.ylabel(r"$\mathrm{{log P_{orb}} (d)}$", fontsize=15)
                    plt.xticks(fontsize=15)
                    plt.yticks(fontsize=15)
                    plt.savefig(htmlFolderLocation+fname)
                plt.close()
    else:
        print(nowtime()+"[WARNING] Empty Data: "+fname)
    del data,fname,htmlFolderLocation,dataLength,AlphaCE,listI
    gc.collect()


#质量-质量图
def plotMDonorAccretor(data,fname,htmlFolderLocation,AlphaCE=1,listI=[], agesign = 0):
    # fig = plt.figure(figsize=(18, 14))
    # plt.subplots_adjust(top=0.94, bottom=0.05, left=0.05, right=0.98, hspace=0)
    # gs = GridSpec(4, 3, width_ratios=[1, 1, 1], height_ratios=[0.1, 1, 1, 1], hspace=0, wspace=0)
    fig = plt.figure(figsize=(16, 9))
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.05, right=0.98, hspace=0)
    gs = GridSpec(3, 3, width_ratios=[1, 1, 1], height_ratios=[0.1, 1, 1], hspace=0, wspace=0)
    for i in range(1,3):
        for j in range(len(AlphaCE)):
            if len(listI[j][i])>0:
                ax = fig.add_subplot(gs[i, j])
                cmap = plt.cm.get_cmap('viridis')
                cmap.set_under(color='white')
                hist = ax.hist2d(data[j][data[j]["i"].isin(listI[j][i])]["mx2"], data[j][data[j]["i"].isin(listI[j][i])]["mx"], bins=40, weights=data[j][data[j]["i"].isin(listI[j][i])]["ndt"], range=[[0, 50], [0,80]], norm=LogNorm(), cmap=cmap)
                if np.max(hist[0])>0.001:
                    hist[3].set_clim(0.001, np.max(hist[0]))
                    ax.set_xlim(0.1,42)
                    ax.set_ylim(0.1,75)
                    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
                    if i == 2:
                        plt.xlabel(r"$\mathrm{M_{WR} ({M_{\odot}})}$", fontsize=15)
                    else:
                        ax.set_xticklabels([])
                    if j == 0:
                        plt.ylabel(r"$\mathrm{M_{BH} ({M_{\odot}})}$", fontsize=15)
                    else:
                        ax.set_yticklabels([])
                    if agesign == 0:
                        plt.text(2,92,r"$α_{CE}=$"+str(AlphaCE)+", "+listname[i],fontsize=15)
                        plt.errorbar(28, 20, xerr=[[7],[5]], yerr=[[4],[4]], ecolor="red",  ms=6, marker='o', markerfacecolor='red', mec="red", elinewidth=2, capsize=3, capthick=3)
                        plt.text(29,14,"NGC 300 X-1",fontsize=15,color="red")
                        plt.errorbar(9.2, 2.4, xerr=[[2],[8.3]], yerr=[[1.1],[2.1]], ecolor="red", ms=6, marker='o', markerfacecolor='red', mec="red", elinewidth=2, capsize=3, capthick=3)
                        plt.text(14, 4,"Cyg X-3",fontsize=15,color="red")
                        plt.errorbar(19, 20, xerr=[[1],[1]], yerr=[[15],[10]], ecolor="red",  ms=6, marker='o', markerfacecolor='red', mec="red", elinewidth=2, capsize=3, capthick=3)
                        plt.text(3, 21, "M101 ULX-1",fontsize=15,color="red")
                    plt.errorbar(26, 26, xerr=[[9],[9]], yerr=[[9],[8]], ecolor="red",  ms=6, marker='o', markerfacecolor='red', mec="red", elinewidth=2, capsize=3, capthick=3)
                    plt.text(30, 20, "IC 10 X-1",fontsize=15,color="red")
                    plt.text(2,65,r"$α_{CE}=$"+str(AlphaCE[j])+", "+listname[i],fontsize=15)
    colorbar(fig, gs, ax, plt, hist[3])
    plt.savefig(htmlFolderLocation+fname)


#质量-质量图
def plotMDonorAccretorSingle(data,fname,htmlFolderLocation,AlphaCE=1,listI=[], agesign = 0):
    dataLength=len(data)
    listname=["Stable Mass Transfer"]
    if dataLength > 0:
        for i in range(1):
            if len(listI[i])>0:
                print(nowtime()+"Plot: "+fname+"-"+listname[i]+"-a"+str(AlphaCE))
                fig, ax = plt.subplots()
                cmap = plt.cm.get_cmap('viridis')
                cmap.set_under(color='white')
                hist = ax.hist2d(data[data["i"].isin(listI[i])]["mx2"],data[data["i"].isin(listI[i])]["mx"],bins=40,weights=data[data["i"].isin(listI[i])]["ndt"],range=[[0, 50], [0,100]],norm=LogNorm(), cmap=cmap)
                hist[3].set_clim(0.001, np.max(hist[0]))
                if np.max(hist[0])>0.001:
                    cb = fig.colorbar(hist[3], ax=ax)
                    cb.ax.set_ylabel('N', fontsize=13)
                    cb.ax.tick_params(labelsize=12)
                    ax.set_xlim(0,50)
                    ax.set_ylim(0,100)
                    if agesign == 0:
                        plt.text(2,92,listname[i],fontsize=15)
                        plt.errorbar(28, 20, xerr=[[7],[5]], yerr=[[4],[4]], ecolor="red",  ms=6, marker='o', markerfacecolor='red', mec="red", elinewidth=2, capsize=3, capthick=3)
                        plt.text(29,14,"NGC 300 X-1",fontsize=15,color="red")
                        plt.errorbar(9.2, 2.4, xerr=[[2],[8.3]], yerr=[[1.1],[2.1]], ecolor="red", ms=6, marker='o', markerfacecolor='red', mec="red", elinewidth=2, capsize=3, capthick=3)
                        plt.text(14, 4,"Cyg X-3",fontsize=15,color="red")
                        plt.errorbar(19, 20, xerr=[[1],[1]], yerr=[[15],[10]], ecolor="red",  ms=6, marker='o', markerfacecolor='red', mec="red", elinewidth=2, capsize=3, capthick=3)
                        plt.text(3, 21, "M101 ULX-1",fontsize=15,color="red")
                    plt.errorbar(26, 26, xerr=[[9],[9]], yerr=[[9],[8]], ecolor="red",  ms=6, marker='o', markerfacecolor='red', mec="red", elinewidth=2, capsize=3, capthick=3)
                    plt.text(36, 24, "IC 10 X-1",fontsize=15,color="red")
                    plt.xlabel(r"${M_{WR}}$(${M_{\odot}}$)", fontsize=13)
                    plt.ylabel(r"${M_{BH}}$(${M_{\odot}}$)", fontsize=13)
                    plt.xticks(fontsize=12)
                    plt.yticks(fontsize=12)
                    plt.savefig(htmlFolderLocation+fname)
                plt.close()
    else:
        print(nowtime()+"[WARNING] Empty Data: "+fname)
    del data,fname,htmlFolderLocation,dataLength
    gc.collect()


#WR星质量分布
def plotDistribution(data, title, htmlFolderLocation, AlphaList=[], list=[]):
    print(nowtime()+"Plot: "+title)
    fig = plt.figure(figsize=(16, 5))
    gs = GridSpec(1, 3, width_ratios=[1, 1, 1], hspace=0, wspace=0)
    plt.subplots_adjust(top=0.92, bottom=0.12, left=0.05, right=0.98, hspace=0)
    for j in range(len(presentlist)):
        ax = fig.add_subplot(gs[0, j])
        for i in range(len(presentlist)):
            if len(list[j][i]) > 0 and np.max(data[j][data[j]["i"].isin(list[j][i])]["ndt"]) >= 0.000001:
                plt.hist(data[j][data[j]["i"].isin(list[j][i])]["mx2"],
                         bins=20, 
                         histtype='step',
                         weights=data[j][data[j]["i"].isin(list[j][i])]["ndt"], 
                         color=presentlist[i][0], 
                         linestyle=presentlist[i][1], 
                         linewidth=1, 
                         log=True, 
                         label="$α_{CE}=$"+str(round(AlphaList[j],2))+", "+presentlist[i][2],
                         facecolor="white")
        plt.axvspan(17,35,alpha=0.3,color='gray')
        plt.legend(loc='upper right')
        plt.xlabel(r"$\mathrm{M_{WR} ({M_{\odot}})}$", fontsize=15)
        if j == 0:
            plt.ylabel(r"Number", fontsize=15)
        else:
            ax.set_yticklabels([])
        plt.xlim(0,49)
        plt.ylim(0.00001,5)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
    plt.savefig(htmlFolderLocation+title)

#致密星质量分布
def plotCODistribution(data, title, htmlFolderLocation, AlphaList=[], list=[]):
    print(nowtime()+"Plot: "+title)
    fig = plt.figure(figsize=(16, 5))
    gs = GridSpec(1, 3, width_ratios=[1, 1, 1], hspace=0, wspace=0)
    plt.subplots_adjust(top=0.92, bottom=0.12, left=0.05, right=0.98, hspace=0)
    for j in range(len(presentlist)):
        ax = fig.add_subplot(gs[0, j])
        for i in range(len(presentlist)):
            if len(list[j][i]) > 0 and np.max(data[j][data[j]["i"].isin(list[j][i])]["ndt"]) >= 0.000001:
                plt.hist(data[j][data[j]["i"].isin(list[j][i])]["mx"],
                         bins=20,
                         histtype='step',
                         weights=data[j][data[j]["i"].isin(list[j][i])]["ndt"],
                         color=presentlist[i][0],
                         linestyle=presentlist[i][1],
                         linewidth=1,
                         log=True,
                         label="$α_{CE}=$"+str(round(AlphaList[j],2))+", "+presentlist[i][2],
                         facecolor="white")
        plt.axvspan(23,34,alpha=0.3,color='gray')
        plt.legend()
        plt.xlabel(r"$\mathrm{M_{BH} ({M_{\odot}})}$", fontsize=15)
        if j == 0:
            plt.ylabel(r"Number", fontsize=15)
        else:
            ax.set_yticklabels([])
        plt.xlim(0,74)
        plt.ylim(0.00001,5)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
    plt.savefig(htmlFolderLocation+title)
