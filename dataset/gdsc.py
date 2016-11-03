# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import pickle
from sbie_optdrug.dataset import filelist
import json
import pandas as pd
from ipdb import set_trace
import termutil

rawfiles = filelist.gdsc_v50['raw']


def cell_lines():
#   CELL_LINE_NAME  COSMIC_ID
# 0             SR   905965.0
# 1          STC-1  1299060.0
# 2       STS-0421  1299061.0
# 3         SU8686  1240218.0
# 4        CAL-120   906826.0

    data = pd.read_csv( rawfiles['gdsc_cell_lines_w5'] )

    return data


def manova_output():
# ipdb> data.head()
#         drug   gene  no_mut  mut  amp  del    pvalue  anova_effect  Mean_WT  \
# 0  Erlotinib   AKT2       1    0    1    0  0.933253      1.049500  4.35367
# 1  Erlotinib    ALK       2    1    1    0  0.932308      0.915901  4.35259
# 2  Erlotinib    APC      12   11    1    0  0.174994     -0.173367  4.37252
# 3  Erlotinib   BRAF      22   22    0    0  0.175359      0.297798  4.31634
# 4  Erlotinib  BRCA1       2    0    2    0  0.009620     -1.772750  4.37218
#
#    Mean_MT   ...     Semi-Interquartile Range_WT  Average Deviation_WT  \
# 0  4.61067   ...                         2.07448               414.506
# 1  4.65621   ...                         2.06765               412.574
# 2  3.88649   ...                         2.07891               399.960
# 3  4.87614   ...                         2.13987               399.233
# 4  1.51184   ...                         2.03576               407.785
#
#    Sum Of Squares_WT  Variation Ratio_WT  drug_effect  drug_id  slope effect  \
# 0            932.807            0.996894     0.455792        1      0.088685
# 1            930.126            0.996885     0.397771        1      0.093822
# 2            899.694            0.996785    -0.075292        1     -0.050727
# 3            909.652            0.996678     0.129332        1      0.054409
# 4            908.513            0.996885    -0.769896        1     -0.153800
#
#    Volcano Plot value  Analysis Date  Version
# 0            8.158006      10-Sep-13     w5.0
# 1            6.245137      10-Sep-13     w5.0
# 2            0.706994      10-Sep-13     w5.0
# 3            1.814112      10-Sep-13     w5.0
# 4            0.028854      10-Sep-13     w5.0
#
# [5 rows x 50 columns]
    data = pd.read_csv( rawfiles['gdsc_manova_output_w5'] )

    return data


def manova_input():
#   Cell Line  Cosmic_ID Cancer Type Tissue  MS-HL AKT2  ALK  APC BRAF BRCA1  \
# 0       NaN        NaN         NaN    NaN    NaN  NaN  NaN  NaN  NaN   NaN
# 1       NaN        NaN         NaN    NaN    NaN  NaN  NaN  NaN  NaN   NaN
# 2       NaN        NaN         NaN    NaN    NaN  NaN  NaN  NaN  NaN   NaN
# 3       NaN        NaN         NaN    NaN    NaN  NaN  NaN  NaN  NaN   NaN
# 4       NaN        NaN         NaN    NaN    NaN  NaN  NaN  NaN  NaN   NaN
#
#              ...              JNJ-26854165_IC_50_HIGH  \
# 0            ...                      1133_IC_50_HIGH
# 1            ...                      MDM2_IC_50_HIGH
# 2            ...             None required_IC_50_HIGH
# 3            ...                         Y_IC_50_HIGH
# 4            ...                 0.0390625_IC_50_HIGH
#
#              TW 37_IC_50_LOW          TW 37_IC_50.2  \
# 0             1149_IC_50_LOW             1149_IC_50
# 1  BCL-2 :  BCL-XL_IC_50_LOW  BCL-2 :  BCL-XL_IC_50
# 2    None required_IC_50_LOW    None required_IC_50
# 3                Y_IC_50_LOW                Y_IC_50
# 4       0.01953125_IC_50_LOW       0.01953125_IC_50
#
#              TW 37_IC_50_HIGH      CCT018159_IC_50_LOW    CCT018159_IC_50.2  \
# 0             1149_IC_50_HIGH           1170_IC_50_LOW           1170_IC_50
# 1  BCL-2 :  BCL-XL_IC_50_HIGH          HSP90_IC_50_LOW          HSP90_IC_50
# 2    None required_IC_50_HIGH  None required_IC_50_LOW  None required_IC_50
# 3                Y_IC_50_HIGH              Y_IC_50_LOW              Y_IC_50
# 4       0.01953125_IC_50_HIGH      0.0390625_IC_50_LOW      0.0390625_IC_50
#
#        CCT018159_IC_50_HIGH      AG-014699_IC_50_LOW    AG-014699_IC_50.2  \
# 0           1170_IC_50_HIGH           1175_IC_50_LOW           1175_IC_50
# 1          HSP90_IC_50_HIGH        PARP1/2_IC_50_LOW        PARP1/2_IC_50
# 2  None required_IC_50_HIGH  None required_IC_50_LOW  None required_IC_50
# 3              Y_IC_50_HIGH              Y_IC_50_LOW              Y_IC_50
# 4      0.0390625_IC_50_HIGH     0.01953125_IC_50_LOW     0.01953125_IC_50
#
#        AG-014699_IC_50_HIGH
# 0           1175_IC_50_HIGH
# 1        PARP1/2_IC_50_HIGH
# 2  None required_IC_50_HIGH
# 3              Y_IC_50_HIGH
# 4     0.01953125_IC_50_HIGH
#
# [5 rows x 2035 columns]
    data = pd.read_csv( rawfiles['gdsc_manova_input_w5'] )

    return data


def en_input():
# ipdb> data.head()
#                          23132-87         5637        639-V        647-V  \
# SCN3A                    1.516744     0.575197     0.269205     1.866920
# SCN3B                   21.372280     3.851475     5.909434     2.700979
# TMPRSS11E /// LOC653     0.767084     0.902683     7.339373     6.191828
# RPLP2                 4829.649000  3828.280000  2954.398000  2498.298000
# GFER                   182.283100    23.761410    62.224810    24.094620
#
#                               697        786-0      8-MG-BA        8505C  \
# SCN3A                    6.276263     7.408377    15.526160    11.376377
# SCN3B                   14.524920     2.620499     7.939816     6.063322
# TMPRSS11E /// LOC653     1.744238    18.408735     2.562830     0.961180
# RPLP2                 6175.425000  2963.744400  4677.987000  5299.149400
# GFER                    13.595590    18.124320   101.673100    61.479424
#
#                             A101D         A172     ...          VM-CUB-1  \
# SCN3A                    0.443228    11.199420     ...          0.879553
# SCN3B                    2.519536     3.705718     ...          6.402947
# TMPRSS11E /// LOC653     4.479781     0.411633     ...          5.874473
# RPLP2                 4666.832000  3422.029000     ...       3899.956000
# GFER                    53.482300    57.221960     ...         29.656750
#
#                          VMRC-RCZ       WM-115      WSU-NHL         YAPC  \
# SCN3A                    2.037591     6.782218    39.773170     0.470770
# SCN3B                    3.034943     9.784748     1.754601     2.470088
# TMPRSS11E /// LOC653     0.890203     0.177250     2.118926     2.360048
# RPLP2                 5521.773000  3209.311800  7610.129000  3532.778000
# GFER                    88.686130    43.228840    86.426000    85.486180
#
#                             YH-13        YKG-1     ZR-75-30        no-10  \
# SCN3A                    2.227729     0.544502     0.233714     0.491345
# SCN3B                    9.274123     1.235115     3.137976     0.750512
# TMPRSS11E /// LOC653     4.511205     0.397292     4.054890     0.539431
# RPLP2                 2892.355000  2116.524000  5440.562000  3241.198000
# GFER                    51.902210    87.498520    49.901310    63.910220
#
#                             no-11
# SCN3A                    6.598717
# SCN3B                   19.764830
# TMPRSS11E /// LOC653     3.856848
# RPLP2                 4967.683000
# GFER                   100.428700
# [13831 rows x 624 columns]
    data = pd.read_csv( rawfiles['gdsc_en_input_w5'] )

    return data


def en_output():
# This is a result for ElasticNet
# ipdb> data.head()
#                 FEATURE  DRUG ID  DRUG NAME TARGET  FREQ    WEIGHT     EFFECT
# 0               GPR172B        1  Erlotinib   EGFR   1.0 -0.585600  -8.474797
# 1                 HOXA1        1  Erlotinib   EGFR   1.0 -0.078676  -5.043885
# 2  UGT1A10 /// UGT1A8 /        1  Erlotinib   EGFR   1.0 -0.010312  -3.994034
# 3               OLFML2A        1  Erlotinib   EGFR   1.0 -0.059402 -10.704910
# 4                 ITM2B        1  Erlotinib   EGFR   1.0 -0.010735  -7.755489
    data =  pd.read_csv( rawfiles['gdsc_en_output_w5'] )

    return data


def drug_sensitivity_raw_data():
# ipdb> data.columns.values
# array(['IC_RESULTS_ID', 'BARCODE', ' PLATE_DATE', 'SCAN_ID', 'DRUG_SET',
#        'DRUG_SET_VERSION', 'FORMAT', 'ASSAY', 'COSMIC_ID',
#        'CELL_LINE_NAME', 'DRUG_ID', 'MAX_CONC', 'FOLD_DILUTION', 'raw_max',
#        'raw2', 'raw3', 'raw4', 'raw5', 'raw6', 'raw7', 'raw8', 'raw9',
#        'control1', 'control2', 'control3', 'control4', 'control5', ...
#        'control46', 'control47', 'control48', 'blank1', 'blank2', 'blank3', 
#        'blank28', 'blank29', 'blank30', 'blank31', 'blank32'], dtype=object)
    data = pd.read_csv( rawfiles['gdsc_drug_sensitivity_raw_data_w5'] )
    set_trace()
    return data


def drug_sensitivity_fitted_data():
#   cell_line_name  cosmic_id  format  drug_id  max_conc  ic_results_id  \
# 0         MC-CAR     683665       9        1       2.0        1018163
# 1         MC-CAR     683665       9        3       0.1         871771
# 2         MC-CAR     683665       9        5       8.0         887667
# 3         MC-CAR     683665       9        6       2.0         876856
# 4         MC-CAR     683665       9        9       1.0         868342
#
#    ic_50_est  ic_50_high  ic_50_low       d   ...     p_neg23  p_neg24  \
# 0   3.827969    7.131264   2.102452  0.0004   ...        null     null
# 1   1.490631    4.725280  -0.473336  0.0008   ...        null     null
# 2   2.120559    2.247206   2.025252  0.0005   ...        null     null
# 3   5.552208    9.652475   2.992057  0.0008   ...        null     null
# 4   0.801777    4.451681   0.240776  0.0033   ...        null     null
#
#    p_neg25  p_neg26  p_neg27  p_neg28  p_neg29  p_neg30  p_neg31  p_neg32
# 0     null     null     null     null     null     null     null     null
# 1     null     null     null     null     null     null     null     null
# 2     null     null     null     null     null     null     null     null
# 3     null     null     null     null     null     null     null     null
# 4     null     null     null     null     null     null     null     null
#
# [5 rows x 437 columns]
    data = pd.read_csv( rawfiles['gdsc_drug_sensitivity_fitted_data_w5'] )

    return data


def tissue_output():
#          drug name       tissue name  drug id  ttest p value  \
# 0  Erlotinib_ALPHA   B_cell_leukemia        1       0.004749
# 1  Erlotinib_ALPHA   B_cell_lymphoma        1       0.769064
# 2  Erlotinib_ALPHA           Bladder        1       0.519933
# 3  Erlotinib_ALPHA  Burkitt_lymphoma        1       0.313054
# 4  Erlotinib_ALPHA  Hodgkin_lymphoma        1       0.824143
#
#    ttest effect size  group mean  muts  ttest q value  sign diff subgroups  \
# 0           2.408670     6.73330     4       0.076057                    3
# 1           0.147351     4.49634    12       0.939026                    1
# 2          -0.778402     3.58088     2       0.843586                    0
# 3           0.527594     4.86409    11       0.720664                    2
# 4           0.156228     4.50779     6       0.953035                    0
#
#    B_cell_leukemia   ...       testis  sign_testis   thyroid  sign_thyroid  \
# 0              NaN   ...     2.106240          0.0  1.830140           0.0
# 1          2.23696   ...    -0.130718          0.0 -0.406824           0.0
# 2          3.15242   ...    -1.046180          0.0 -1.322280           0.0
# 3          1.86921   ...     0.237032          0.0 -0.039074           0.0
# 4          2.22551   ...    -0.119268          0.0 -0.395374           0.0
#
#    urogenital_system_other  sign_urogenital_system_other  uterus  sign_uterus  \
# 0                 3.344220                           0.0     NaN          NaN
# 1                 1.107260                           0.0     NaN          NaN
# 2                 0.191804                           0.0     NaN          NaN
# 3                 1.475010                           0.0     NaN          NaN
# 4                 1.118710                           0.0     NaN          NaN
#
#    Analysis Date  Version
# 0      10-Sep-13     w5.0
# 1      10-Sep-13     w5.0
# 2      10-Sep-13     w5.0
# 3      10-Sep-13     w5.0
# 4      10-Sep-13     w5.0
    data = pd.read_csv( rawfiles['gdsc_tissue_output_w5'] )

    return data


def compounds_conc():
#   Compound Name  Min Concentration(micromolar)  Max Concentration(micromolar)
# 0        17-AAG                       0.003906                          1.000
# 1        681640                       0.007812                          2.000
# 2      A-443654                       0.004000                          1.024
# 3      A-770041                       0.020000                          5.120
# 4       ABT-263                       0.007812                          2.000
    data = pd.read_csv( rawfiles['gdsc_compounds_conc_w5'] )

    return data


def mutation():
#   Cell Line  Cosmic_ID     Cancer Type                         Tissue  MS-HL  \
# 0    MC-CAR     683665           blood  haematopoietic_neoplasm_other      0
# 1    PFSK-1     683667  nervous_system                medulloblastoma      0
# 2      A673     684052     soft_tissue               rhabdomyosarcoma      0
# 3       ES3     684055            bone                 ewings_sarcoma      0
# 4       ES5     684057            bone                 ewings_sarcoma      0
#
#          AKT2         ALK         APC             BRAF       BRCA1   ...     \
# 0  na::0<cn<8  wt::0<cn<8  wt::0<cn<8       wt::0<cn<8  wt::0<cn<8   ...
# 1  na::0<cn<8  wt::0<cn<8  wt::0<cn<8       wt::0<cn<8  wt::0<cn<8   ...
# 2  na::0<cn<8  wt::0<cn<8  wt::0<cn<8  p.V600E::0<cn<8  wt::0<cn<8   ...
# 3  na::0<cn<8  wt::0<cn<8  wt::0<cn<8       wt::0<cn<8  wt::0<cn<8   ...
# 4  na::0<cn<8  wt::0<cn<8  wt::0<cn<8       wt::0<cn<8  wt::0<cn<8   ...
    data = pd.read_csv( rawfiles['gdsc_mutation_w5'] )

    return data


def expU133A():
# ipdb> data.head()
#        PROBE      BxPC-3      KMOE-2     MFM-223      NUGC-3      OC-314  \
# 0  1007_s_at  639.944183   16.373449  318.155778  450.998247  239.469002
# 1    1053_at   51.349139  135.185672   68.408031   65.130261  126.891209
# 2     117_at    5.900338   53.393754    3.679530    0.835631    0.624551
# 3     121_at   29.984657   18.760248   22.707359   37.108880  347.899885
# 4  1255_g_at    0.329891    1.891916    0.371882    1.384804    0.516666
#
#      COLO-741   KARPAS-45         JAR     DU-4475    ...          SF268  \
# 0  154.087362   46.001733  203.582799  171.863044    ...      84.766663
# 1  146.355079  163.087330  103.647606  204.069724    ...      78.853615
# 2    3.906931   28.396109   10.808254  165.628891    ...       0.769494
# 3   21.480952   40.950497   31.545490   31.226368    ...      22.735391
# 4    0.461409    0.503592    0.550652    1.156150    ...       0.667385
#
#          TK10      A2780   OVCAR-4.1        A375   KP-N-S19s        BC-3  \
# 0  235.219129  46.343851  263.266154  230.686727  101.217233   17.466248
# 1   55.688551  76.178632   23.357161   35.835890   75.858236  199.226068
# 2    2.808876   3.210985    0.670012   13.643147    7.977687    2.249444
# 3  553.756598  16.793050  638.726055   38.407900   32.861390   53.520014
# 4    1.072061   0.372600    6.173136    1.860528   18.326121    3.964986
#
#    PANC-08-13.1      EKVX.1  DMS-114.1
# 0    506.256421  305.627689  89.021586
# 1     63.581571   63.613736  91.283199
# 2      1.784688    2.224977   3.879441
# 3     46.280554   21.681985  23.478692
# 4      0.492764    0.611497  13.048996
    data = pd.read_csv( rawfiles['expU133A'], sep='\t')

    return data
