# # import pandas as pd
# # import subprocess
# # from alive_progress import alive_bar
# # import functions
# # import sys
# # import gc
# # import numpy as np
# # import re
# # import datetime

# # def nowtime():
# #     return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')

# # #定义变量与参数   20230402_165032_1000000 20230402_125051_10000000
# # dataRunTimeAll="20230402_125051_10000000"
# # dataRunTime=dataRunTimeAll[:15]
# # dataFolderLocation=functions.locationCheck(dataRunTimeAll)
# # # dataFileLocation=dataFolderLocation+"N"+dataRunTimeAll+".csv"
# # dataFileLocation=dataFolderLocation+"N20230402_125051_10000000.csv"
# # file_data = ""
# # tempfile=dataFileLocation+".tmp"
# # totalnum=int(subprocess.getoutput("wc -l %s | awk '{print $1}'" % dataFileLocation))
# # otnum=functions.onetwentieth(totalnum)
# # i=0
# # with open(tempfile,"w",encoding="utf-8") as f:
# #     f.write("i,t1,mx,mx2,tbx,kw,kw2,sepx,rd2rl,ndt,\n")
# # with open(dataFileLocation, "r", encoding="utf-8") as f:
# #     for line in f:
# #         i+=1
# #         if " " in line:
# #             line = line.replace(" ","")
# #         # print(line.split(",")[5].strip() in ["13","14"],line.split(",")[6].strip())
# #         if (line.split(",")[5].strip() in ["13","14"]) & (line.split(",")[6].strip() in ["7","8","9"]):
# #             if i > 1:
# #                 file_data += line
# #                 if i%otnum==0 or i%totalnum==0:
# #                     print(nowtime()+"Trim blank of file: "+dataFileLocation+": "+str(i)+"/"+str(totalnum)+", "+"percent: {:.2%}".format(i/totalnum))
# #                     if len(file_data) > 0:
# #                         with open(tempfile,"a",encoding="utf-8") as f:
# #                             f.write(file_data)
# #                     else:
# #                         print(nowtime()+"ERROR: Empty Data")
# #                         sys.exit(0)
# #                     file_data = ""
# #             else:
# #                 print(nowtime()+"Warning data: "+str(i)+" - "+line)
# #                 continue
# #         else:
# #             continue


# # # print(functions.nowtime()+str(dataRunTime)+" Stage 1.1: Loading data: All")
# # # dataAll=pd.read_csv(dataFileLocation,usecols=["i","t1","mx","mx2","tbx","kw","kw2","ndt"],dtype={'i':int,'t1':float,'mx':float,'mx2':float,'tbx':float,'kw':int,'kw2':int,'ndt':float})
# # # print(functions.nowtime()+str(dataRunTime)+" Stage 1.2: Loading data successfully")
# # # dataAll=dataAll[(dataAll["t1"]>0)&(dataAll["t1"]<=100)&(dataAll["mx2"]>2)&(dataAll["tbx"]>0)]
# # # print(functions.nowtime()+str(dataRunTime)+" Stage 1.3: Filting data")
# # # totalFormationCount=int(subprocess.getoutput("grep "+dataRunTime+" "+dataFolderLocation+"rdc.num | awk -F '[,:]' '{print $2}'"))
# # # if totalFormationCount > 0:
# # #     htmlFolderLocation=dataFolderLocation+dataRunTime+"_"+str(totalFormationCount)+"/"
# # # else:
# # #     htmlFolderLocation=dataFolderLocation+dataRunTime+"/"
# # # effectiveFormationCount=int(subprocess.getoutput("grep "+dataRunTime+" "+dataFolderLocation+"rdc.num | awk -F '[,:]' '{print $2-$4}'"))
# # # htmlFileLocation=htmlFolderLocation+str(totalFormationCount)+"-"+dataRunTime+"-Analysis.html"
# # # dataParas=subprocess.getoutput("grep "+dataRunTime+" "+dataFolderLocation+"rdc.num | awk -F '[,:]' '{print $2,$4,$6,$8,$10,$12,$14,$16,$18,$20,$22,$24,$26,$28,$30,$32,$34,$36,$38,$40,$42,$44,$46,$48,$50,$52}'").split()
# # # print(functions.nowtime()+str(dataRunTime)+" Stage 1 running successfully: Initialization completed.")


# # import sys


# # def main():
# #     print('参数个数为:', len(sys.argv), '个参数。')
# #     print('参数列表:', str(sys.argv))
# #     print('脚本名为：', sys.argv[0])
# #     for i in range(1, len(sys.argv)):
# #         print('参数 %s 为：%s' % (i, sys.argv[i]))

# # if __name__ == "__main__":
# #     main()


# # if not sys.argv[1]:
# #     print("1")





# # dataReturn = 3 if 1+1==2 else 4
# # print(dataReturn)
# # import subprocess
# # import functions
# # import sys
# # import os
# # import re

# # def alterContent(file):
# #     file_data = ""
# #     tempfile=file+".tmp"
# #     totalnum=int(subprocess.getoutput("wc -l %s | awk '{print $1}'" % file))
# #     otnum=functions.onetwentieth(totalnum)
# #     i=0
# #     with open(file, "r", encoding="utf-8") as f:
# #         for line in f:
# #             i+=1
# #             line = line.replace(" ","")
# #             # line = line.replace("0.000000","0.0")
# #             # print(line)
# #             # line = re.sub(",0.0*,",",0.0,",line)
# #             line = re.sub(r'\*+','-1',line)
# #             line = re.sub(',$','',line)
# #             # line = re.sub("\.0*,",".0,",line)
# #             file_data += line
# #             if i%otnum==0 or i%totalnum==0:
# #                 print(functions.nowtime()+"Trim blank of file: "+file+": "+str(i)+"/"+str(totalnum)+", "+"percent: {:.2%}".format(i/totalnum))
# #                 if len(file_data) > 0:
# #                     with open(tempfile,"a",encoding="utf-8") as f:
# #                         f.write(file_data)
# #                 else:
# #                     print(functions.nowtime()+"ERROR: Empty Data")
# #                     sys.exit(0)
# #                 file_data = ""
# #     if os.path.exists(tempfile):
# #         os.rename(tempfile,file)
# # alterContent("/Files/git/data/N20230405_151828_10000000s.csv3")


# # import numpy as np
# # import matplotlib.pyplot as plt
# # import matplotlib.colors as mcolors
# # from matplotlib.gridspec import GridSpec
# # x = np.linspace(0, 2 * np.pi, 100)
# # y1 = np.sin(x)
# # y2 = np.cos(x)
# # fig = plt.figure(figsize=(12, 8))

# # # 使用GridSpec创建2行2列的子图网格
# # gs = GridSpec(2, 3, width_ratios=[1, 1], height_ratios=[1, 0.1], hspace=0.3, wspace=0)

# # # 第一个子图：Sine Function
# # ax1 = fig.add_subplot(gs[0, 0])
# # ax1.tick_params(axis='both', which='both', direction='in', top=True, right=True)
# # cmap = plt.cm.get_cmap('viridis')
# # norm = mcolors.Normalize(vmin=min(y1), vmax=max(y1))
# # sc1 = ax1.scatter(x, y1, c=y1, cmap=cmap, norm=norm)
# # ax1.set_xlabel('X')
# # ax1.set_ylabel('Y')
# # ax1.set_title('Sine Function')
# # # 第二个子图：Cosine Function
# # ax2 = fig.add_subplot(gs[0, 1])
# # sc2 = ax2.scatter(x, y2, c=y2, cmap=cmap, norm=norm)
# # ax2.set_xlabel('X')
# # ax2.set_title('Cosine Function')
# # # ax.tick_params()
# # ax3 = fig.add_subplot(gs[0, 2])
# # sc3 = ax3.scatter(x, y2, c=y2, cmap=cmap, norm=norm)
# # # ax3.set_xlabel('X')
# # # ax2.set_ylabel('Y')
# # ax3.set_title('Cosine Function')
# # ax2.set_yticks([])
# # cbar_ax = fig.add_subplot(gs[1, :])
# # cbar = fig.colorbar(sc1, cax=cbar_ax, orientation='horizontal')
# # cbar.set_label('Colorbar Label')
# # # plt.tight_layout()
# # plt.show()

# # import numpy as np
# # import matplotlib.pyplot as plt
# # x = np.linspace(0, 2 * np.pi, 100)
# # y1 = np.sin(x)
# # y2 = np.cos(x)
# # y3 = np.tan(x)
# # fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

# # # 绘制第一个子图
# # axes[0].plot(x, y1)
# # axes[0].set_xlabel('X')
# # axes[0].set_ylabel('Y')
# # axes[0].set_title('Sine Function')
# # axes[0].tick_params(axis='both', which='both', direction='in', top=True, right=True)

# # # 绘制第二个子图
# # axes[1].plot(x, y2)
# # axes[1].set_xlabel('X')
# # axes[1].set_title('Cosine Function')
# # axes[1].tick_params(axis='both', which='both', direction='in', top=True, right=True)

# # # 绘制第三个子图
# # axes[2].plot(x, y3)
# # axes[2].set_xlabel('X')
# # axes[2].set_title('Tangent Function')
# # axes[2].tick_params(axis='both', which='both', direction='in', top=True, right=True)

# # # 调整子图之间的间距
# # plt.subplots_adjust(wspace=0.3)

# # # 显示图形
# # plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
# from matplotlib.gridspec import GridSpec

# x = np.linspace(0, 2 * np.pi, 100)
# y1 = np.sin(x)
# y2 = np.cos(x)
# fig = plt.figure(figsize=(16, 5))
# gs = GridSpec(1, 3, width_ratios=[1, 1, 1], hspace=0, wspace=0)  #, height_ratios=[0.1, 1, 1, 1]

# # 第一个子图：Sine Function

# # fig, ax = plt.subplots()
# plt.subplots_adjust(top=0.92, bottom=0.08, left=0.05, right=0.95, hspace=0.3)
# # cmap = plt.cm.get_cmap('viridis')
# # cmap.set_under(color='white')
# # # hist = ax.hist2d(data["t1"],data["mx2"],bins=40,weights=data["ndt"], range=[[0,60], [0,50]], norm=LogNorm(), cmap=cmap)
# # if np.max(hist[0])>0.001:
# #     hist[3].set_clim(0.001, np.max(hist[0]))
# #     cb = fig.colorbar(hist[3], ax=ax)
# #     cb.ax.set_ylabel('N', fontsize=16)
# #     cb.ax.tick_params(labelsize=13)
# #     ax.set_xlim(0,)
# #     ax.set_ylim(0,50)
# #     plt.text(28,45,r"$α_{CE}=$"+str(AlphaCE),fontsize=16)
# #     ax.fill_between([0,10],[17,17],[35,35], color='gray', alpha=0.3)
# #     ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
# #     plt.xlabel(r"$Age(Myr)$", fontsize=15)
# #     plt.ylabel(r"$M_{WR}({M_{\odot}}$)", fontsize=15)
# #     plt.xticks(fontsize=13)
# #     plt.yticks(fontsize=13)
# #     plt.savefig(htmlFolderLocation+fname+"-a"+str(int(AlphaCE)))
# # plt.close()


# ax1 = fig.add_subplot(gs[0, 0])
# cmap = plt.cm.get_cmap('viridis')
# norm = mcolors.Normalize(vmin=min(y1), vmax=max(y1))
# sc1 = ax1.scatter(x, y1, c=y1, cmap=cmap, norm=norm)
# ax1.set_ylabel('Y')
# ax1.tick_params(axis='both', which='both', direction='in', top=True, right=True)

# ax2 = fig.add_subplot(gs[0, 1])
# sc2 = ax2.scatter(x, y2, c=y2, cmap=cmap, norm=norm)
# ax2.tick_params(axis='both', which='both', direction='in', top=True, right=True)
# ax2.set_yticklabels([])

# ax3 = fig.add_subplot(gs[0, 2])
# sc3 = ax3.scatter(x, y1, c=y1, cmap=cmap, norm=norm)
# ax3.set_yticklabels([])
# ax3.tick_params(axis='both', which='both', direction='in', top=True, right=True)

# # ax4 = fig.add_subplot(gs[2, 0])
# # sc4 = ax4.scatter(x, y1, c=y1, cmap=cmap, norm=norm)
# # ax4.set_ylabel('Y')
# # ax4.set_xlabel('X')
# # ax4.tick_params(axis='both', which='both', direction='in', top=True, right=True)

# # ax5 = fig.add_subplot(gs[2, 1])
# # sc5 = ax5.scatter(x, y2, c=y2, cmap=cmap, norm=norm)
# # ax5.tick_params(axis='both', which='both', direction='in', top=True, right=True)
# # ax5.set_yticklabels([])
# # ax5.set_xlabel('X')

# # ax6 = fig.add_subplot(gs[2, 2])
# # sc6 = ax6.scatter(x, y1, c=y1, cmap=cmap, norm=norm)
# # ax6.set_yticklabels([])
# # ax6.set_xlabel('X')
# # ax6.tick_params(axis='both', which='both', direction='in', top=True, right=True)



# # ax4 = fig.add_subplot(gs[3, 0])
# # sc4 = ax4.scatter(x, y1, c=y1, cmap=cmap, norm=norm)
# # ax4.set_ylabel('Y')
# # ax4.set_xlabel('X')
# # ax4.tick_params(axis='both', which='both', direction='in', top=True, right=True)

# # ax5 = fig.add_subplot(gs[3, 1])
# # sc5 = ax5.scatter(x, y2, c=y2, cmap=cmap, norm=norm)
# # ax5.tick_params(axis='both', which='both', direction='in', top=True, right=True)
# # ax5.set_yticklabels([])
# # ax5.set_xlabel('X')

# # ax6 = fig.add_subplot(gs[3, 2])
# # sc6 = ax6.scatter(x, y1, c=y1, cmap=cmap, norm=norm)
# # ax6.set_yticklabels([])
# # ax6.set_xlabel('X')
# # ax6.tick_params(axis='both', which='both', direction='in', top=True, right=True)



# # \begin{figure}[htbp]
# #   \centering
# #   \includegraphics[width=\textwidth]{0}
# #   \caption{Figure 1: The evolutionary analysis was conducted for two types of compact stars: Neutron Stars (NS) and Black Holes (BH). It was found that within 10 million years, it is not possible to form massive X-ray binary systems with Neutron Stars. Although there are differences in the overall evolutionary quantities at different values of alpha, they still do not cover the observed range of binary star data. The subsequent discussion will focus solely on the scenario where compact stars are Black Holes.}
# # \end{figure}


# 202308 - 备份：

# APJ 836,50,2017 Feb 10 Laycock

# The X-Ray Binary Population of the Nearby Dwarf Starburst Galaxy IC 10: Variable and Transient X-Ray Sources


# Time: IC 10 hosts a young (6 × 106 years) 
#    Massey, P., & Holmes, S. 2007, ApJL, 580, L35

# SFR：is reported to be as high as 0.5 Me yr−1 (Leroy, A., Bolatto, A., Walter, F., & Blitz, L. 2006, ApJ, 643, 825 Massey & Holmes 2007),which when normalized by the
# mass of the galaxy (2× 107 Me;Petitpas, G. R., & Wilson, C. D., 1998, ApJ, 496, 226)  yields 2.5 × 10−8 Me yr−1 Me−1

# Z: Z ; Ze/5  Garnett, D. R. 1990, ApJ, 363, 142



# Mass: BH：23-34Msun WR:17-35
# period:
# Silverman, J. M., & Filippenko, A. V. 2008, ApJL, 678, L17

# silverman spectra of the WR star, spanning 1 month, obtained with the Keck I 10 m telescope.The spectra show a periodic shift in the He ii l4686 emission line as compared with IC 10 nebular lines such as [O iii] . 

# From this, we calculate a period of   34.93 +- 0.04 hr
# (consistent with the X-ray period of hr reported by Prestwich) 34.40+-0.83


# radial velocity semiamplitude of 370+-20km/s . 

# The resulting mass function is 7.64 +- 1.26 M , consistent 
# with that of Prestwich (7.8 M,).

# WR~35 M,BH~32.7+-2.6 M
# WR~17 M,, the minimum primary mass is 23.1+-2.1 M,.

#  X-ray luminosity of 10^38ergs/s (Brandt et al. 1997; Bauer & Brandt 2004)

# Be certified as WNE star: Clark & Crowther 2004


# Prestwich, A. H., et al. 2007, ApJ, 669, L21

