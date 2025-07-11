import numpy as np
import scipy.ndimage as spn
import time

VolFra = 0.20
RandomSeed = 20221010
lens = [100, 100, 100]
RVESize_x = 100
elsize = RVESize_x/lens[0]
print("*********************************")
PoreLen = 3
PoreLen = PoreLen/elsize
PorFra = 0.20

Aggre_grade = [19.0, 12.5, 9.5, 4.75]
Aggre_grade = np.array(Aggre_grade)/elsize
Fuller_n = 0.5
print("Element Number:\t", lens)
print("Element Size:\t", elsize)
print("Volume Fraction:\t", VolFra)

start = time.time()
# Random seed locations
np.random.seed(RandomSeed)
## Paras initialization
lx = lens[0]
ly = lens[1]
lz = lens[2]
lxyz = lx*ly*lz
Aggre_Fra = np.zeros(len(Aggre_grade)-1)
Aggre_Len = np.zeros(len(Aggre_grade)-1)
for i in range(len(Aggre_Fra)):
    Aggre_Fra[i] = (Aggre_grade[i]**Fuller_n-Aggre_grade[i+1]**Fuller_n)/(max(Aggre_grade)**Fuller_n-min(Aggre_grade)**Fuller_n)
    Aggre_Len[i] = (Aggre_grade[i]+Aggre_grade[i+1])/2.0

Aggre_Vol = Aggre_Fra*VolFra*lxyz
Aggre_N = np.rint(Aggre_Vol/Aggre_Len/Aggre_Len/Aggre_Len).astype(int)
Aggre_RatExp = 3.0
Aggre_VolRat = np.rint((Aggre_Len/min(Aggre_Len))**Aggre_RatExp).astype(int)
Aggre_Totn = np.sum(Aggre_N)
Aggre_TotN = np.sum(Aggre_N*Aggre_VolRat)

loc_mat = np.arange(0, Aggre_Totn, dtype=int)
loc_mat = np.vstack((loc_mat, loc_mat, loc_mat, loc_mat))
loc_x_0 = np.random.randint(0, lx, size=(Aggre_TotN, 1))
loc_y_0 = np.random.randint(0, ly, size=(Aggre_TotN, 1))
loc_z_0 = np.random.randint(0, lz, size=(Aggre_TotN, 1))
loc_xyz = np.hstack((loc_x_0, loc_y_0, loc_z_0))
MergeSet = []
Aggre_i = 0
Number_List = np.arange(0, Aggre_TotN, dtype=int)
# Seeds merging except the smallest gradation
for i in range(len(Aggre_N)-1):
    Aggre_Gi_Set = np.zeros((Aggre_N[i], Aggre_VolRat[i]), dtype=int)
    for j in range(Aggre_N[i]):
        Pij, = np.random.choice(Number_List, size=1, replace=False)
        dis_arr = np.sum(np.asarray(loc_xyz[Pij] - loc_xyz[Number_List]) ** 2, axis=1)        # simplify the np.sqrt()
        dis_idx = Number_List[np.argpartition(dis_arr, Aggre_VolRat[i])[:Aggre_VolRat[i]]]
        Aggre_Gi_Set[j] = dis_idx
        loc_mat[1::, Aggre_i] = np.rint(np.average(loc_xyz[dis_idx], axis=0)).astype(int)
        Aggre_i = Aggre_i+1
        Number_List = np.setdiff1d(Number_List, dis_idx)
    MergeSet.append(Aggre_Gi_Set)
# Seeds of the smallest gradation
loc_mat[1::, Aggre_i::] = loc_xyz[Number_List].T
MergeSet.append(Number_List.reshape([Aggre_N[-1], 1]))

# Aggregate sub-regions
xx, yy, zz = np.mgrid[-loc_mat[1][0]:lx-loc_mat[1][0],
                      -loc_mat[2][0]:ly-loc_mat[2][0],
                      -loc_mat[3][0]:lz-loc_mat[3][0]]
dis_vals = xx**2+yy**2+zz**2             # simplify the np.sqrt()
AggIdx = np.zeros([lx, ly, lz], dtype=int)
for iAgg in range(1, Aggre_Totn):
    xx, yy, zz = np.mgrid[-loc_mat[1][iAgg]:lx-loc_mat[1][iAgg],
                          -loc_mat[2][iAgg]:ly-loc_mat[2][iAgg],
                          -loc_mat[3][iAgg]:lz-loc_mat[3][iAgg]]
    dis_iAgg = xx**2+yy**2+zz**2         # simplify the np.sqrt()
    AggIdx[dis_iAgg < dis_vals] = iAgg
    dis_vals[dis_iAgg < dis_vals] = dis_iAgg[dis_iAgg < dis_vals]
AggIdx = AggIdx
print("Aggregate sub-regions time:\t", time.time()-start)

# Aggregate shrinkage
AggSrkIdx = np.zeros([lx, ly, lz], dtype=int)-1
iAggList = np.unique(AggIdx)
AggreSize = np.array([])
for iAgg in iAggList:
    layer_tag = -1
    AggiIdx = AggIdx.copy()
    AggiIdx[AggiIdx != iAgg] = layer_tag
    AggiTarN = round(np.sum(AggiIdx == iAgg)*VolFra)
    AggiSrkTag = True
    while AggiSrkTag:
        xxi, yyi, zzi = np.where(AggiIdx == iAgg)
        layer_tag = layer_tag-1
        AggiIdx_pad = np.pad(AggiIdx, pad_width=1, mode='constant', constant_values=-1)
        i_out1 = np.where(AggiIdx_pad[xxi, yyi+1, zzi+1] != iAgg)[0]
        i_out2 = np.where(AggiIdx_pad[xxi+1, yyi, zzi+1] != iAgg)[0]
        i_out3 = np.where(AggiIdx_pad[xxi+1, yyi+1, zzi] != iAgg)[0]
        i_out4 = np.where(AggiIdx_pad[xxi+2, yyi+1, zzi+1] != iAgg)[0]
        i_out5 = np.where(AggiIdx_pad[xxi+1, yyi+2, zzi+1] != iAgg)[0]
        i_out6 = np.where(AggiIdx_pad[xxi+1, yyi+1, zzi+2] != iAgg)[0]
        i_out = np.unique(np.concatenate((i_out1, i_out2, i_out3, i_out4, i_out5, i_out6), axis=0))
        AggiIdx[xxi[i_out], yyi[i_out], zzi[i_out]] = layer_tag
        if AggiTarN < np.sum(AggiIdx == iAgg):
            AggiSrkTag = True
        elif AggiTarN == np.sum(AggiIdx == iAgg):
            AggiSrkTag = False
        else:
            AggiSrkTag = False
            AggiDis = (xxi[i_out]-loc_mat[1, iAgg])*(xxi[i_out]-loc_mat[1, iAgg])+\
                      (yyi[i_out]-loc_mat[2, iAgg])*(yyi[i_out]-loc_mat[2, iAgg])+\
                      (zzi[i_out]-loc_mat[3, iAgg])*(zzi[i_out]-loc_mat[3, iAgg])
            AggiReturnOrd = np.argsort(AggiDis)[0:int(AggiTarN-np.sum(AggiIdx == iAgg))]
            AggiIdx[xxi[i_out][AggiReturnOrd], yyi[i_out][AggiReturnOrd], zzi[i_out][AggiReturnOrd]] = iAgg
            # print(AggiSrkTag, AggiTarN, np.sum(AggiIdx == iAgg))
    AggSrkIdx[AggiIdx == iAgg] = iAgg
print("Aggregate shrinkage time:\t", time.time()-start)

# ITZ Generate
ITZIdx = AggSrkIdx.copy()
xxi, yyi, zzi = np.where(ITZIdx == -1)
ITZ_tag = -2
i_itz = np.where(ITZIdx[xxi[xxi > 0]-1, yyi[xxi > 0], zzi[xxi > 0]] != -1)[0]
ITZIdx[xxi[xxi > 0][i_itz], yyi[xxi > 0][i_itz], zzi[xxi > 0][i_itz]] = ITZ_tag
i_itz = np.where(ITZIdx[xxi[yyi > 0], yyi[yyi > 0]-1, zzi[yyi > 0]] != -1)[0]
ITZIdx[xxi[yyi > 0][i_itz], yyi[yyi > 0][i_itz], zzi[yyi > 0][i_itz]] = ITZ_tag
i_itz = np.where(ITZIdx[xxi[zzi > 0], yyi[zzi > 0], zzi[zzi > 0]-1] != -1)[0]
ITZIdx[xxi[zzi > 0][i_itz], yyi[zzi > 0][i_itz], zzi[zzi > 0][i_itz]] = ITZ_tag
i_itz = np.where(ITZIdx[xxi[xxi < lx-1]+1, yyi[xxi < lx-1], zzi[xxi < lx-1]] != -1)[0]
ITZIdx[xxi[xxi < lx-1][i_itz], yyi[xxi < lx-1][i_itz], zzi[xxi < lx-1][i_itz]] = ITZ_tag
i_itz = np.where(ITZIdx[xxi[yyi < ly-1], yyi[yyi < ly-1]+1, zzi[yyi < ly-1]] != -1)[0]
ITZIdx[xxi[yyi < ly-1][i_itz], yyi[yyi < ly-1][i_itz], zzi[yyi < ly-1][i_itz]] = ITZ_tag
i_itz = np.where(ITZIdx[xxi[zzi < lz-1], yyi[zzi < lz-1], zzi[zzi < lz-1]+1] != -1)[0]
ITZIdx[xxi[zzi < lz-1][i_itz], yyi[zzi < lz-1][i_itz], zzi[zzi < lz-1][i_itz]] = ITZ_tag
print("ITZ generation time:\t", time.time()-start)


# Pore Generation
PoreIdx = ITZIdx.copy()
RandomNum = np.random.standard_normal(lens)
SD = PoreLen/2
Processed_RF = spn.gaussian_filter(RandomNum, SD)
PerLimit = np.percentile(Processed_RF[AggSrkIdx < 0].flatten(), 100*PorFra/(1-VolFra))
PoreIdx[Processed_RF < PerLimit] = -3           # pore
PoreIdx[ITZIdx >= 0] = ITZIdx[ITZIdx >= 0]      # Aggregate phase
print("Pore generation time:\t", time.time()-start)

# Multi-phase counts
MatIdx = PoreIdx.copy()
MatIdx[PoreIdx >= 0] = 3
MatIdx[PoreIdx == -2] = 2
MatIdx[PoreIdx == -1] = 1
MatIdx[PoreIdx == -3] = 0
print("\t".join(["Aggregate phase:", str(np.sum(MatIdx == 3)/lxyz), str(np.sum(MatIdx == 3))]))
print("\t".join(["ITZ phase:", str(np.sum(MatIdx == 2)/lxyz), str(np.sum(MatIdx == 2))]))
print("\t".join(["Mortar phase:", str(np.sum(MatIdx == 1)/lxyz), str(np.sum(MatIdx == 1))]))
print("\t".join(["Pore phase:", str(np.sum(MatIdx == 0)/lxyz), str(np.sum(MatIdx == 0))]))

# RVE Plotting
try:
    from RVEPlot import *
    PlotTag = True
    if PlotTag:
        RVEPlt(MatIdx, "MatIdx")
        # RVEPlt(ITZIdx, "ITZIdx")
        # RVEPlt(PoreIdx, "PoreIdx")
        RVEPlt(MatIdx, "Agg&NonAgg")
        # RandomNum[MatIdx == 3] = 10000
        # RVEPlt(RandomNum, "RandMat")
        # Processed_RF[MatIdx == 3] = 10000
        # RVEPlt(Processed_RF, "RandMat")
        RVEPlt(MatIdx, "Pore@NonAgg")
except:
    print("********NO-PLOT-MODULE********")

# INP Writer
try:
    from InpWriter import *
    InpTag = True
    if InpTag:
        ModelName = "".join(["CRM_", str(RandomSeed), "_", str(lens[0]), "_", str(lens[1]),
                             "_", str(lens[2]), "_", str(Aggre_Totn), "_", str(PoreLen),
                             "_", str(round(PorFra*100)), "_", str(round(VolFra*100))])
        InpWrite(MatIdx, ModelName)
except:
    print("********NO-INP-MODULE********")
