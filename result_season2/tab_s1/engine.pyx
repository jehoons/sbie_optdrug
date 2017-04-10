
from numpy.random import random
import os, sys
import time
from ipdb import set_trace
from itertools import combinations, combinations_with_replacement
from cython.parallel import parallel, prange
from libc.stdlib cimport abort, malloc, free
import hashlib
import json


__start_time = 0

FP_LENGTH = 10

cdef detect_cycles( data ):
    fsize   = len(data)
    for msize in range(1, int(fsize/2) + 1):
        for index in range(fsize):
            left  = data[index:index+msize]
            right = data[index+msize:index+2*msize]
            if left == right:
                return index, msize

    return 0, 0

sign = lambda x: True if x > 0 else False
DEF num_nodes = 96
ctypedef int (*cfptr)(int*)
cdef cfptr eqlist[num_nodes]

cdef int __bool_fcn_72(int state[]):
    # [LexToken(ID,'State_TGFbeta',1,0), LexToken(ASSIGN,'*=',1,14), LexToken(SIGN,'sign',1,17), LexToken(LPAREN,'(',1,21), LexToken(+,'+',1,22), LexToken(ID,'State_HIF1',1,23), LexToken(RPAREN,')',1,33)]
    state_72=sign(+state[37])
    return state_72

cdef int __bool_fcn_22(int state[]):
    # [LexToken(ID,'State_DnaDamage',1,0), LexToken(ASSIGN,'*=',1,16), LexToken(SIGN,'sign',1,19), LexToken(LPAREN,'(',1,23), LexToken(+,'+',1,24), LexToken(ID,'State_Mutagen',1,25), LexToken(+,'+',1,38), LexToken(ID,'State_ROS',1,39), LexToken(RPAREN,')',1,48)]
    state_22=sign(+state[46]+state[61])
    return state_22

cdef int __bool_fcn_92(int state[]):
    # [LexToken(ID,'State_p53_Mdm2',1,0), LexToken(ASSIGN,'*=',1,15), LexToken(SIGN,'sign',1,18), LexToken(LPAREN,'(',1,22), LexToken(+,'+',1,23), LexToken(ID,'State_p53',1,24), LexToken(+,'+',1,33), LexToken(ID,'State_Mdm2',1,34), LexToken(NUMBER,-1.0,1,44), LexToken(RPAREN,')',1,46)]
    state_92=sign(+state[91]+state[44]-1.000000)
    return state_92

cdef int __bool_fcn_2(int state[]):
    # [LexToken(ID,'State_AMP_ATP',1,0), LexToken(ASSIGN,'*=',1,14), LexToken(SIGN,'sign',1,17), LexToken(LPAREN,'(',1,21), LexToken(-,'-',1,22), LexToken(ID,'State_Nutrients',1,23), LexToken(NUMBER,1.0,1,38), LexToken(RPAREN,')',1,40)]
    state_2=sign(-state[51]+1.000000)
    return state_2

cdef int __bool_fcn_49(int state[]):
    # [LexToken(ID,'State_NF1',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(-,'-',1,18), LexToken(ID,'State_PKC',1,19), LexToken(NUMBER,1.0,1,28), LexToken(RPAREN,')',1,30)]
    state_49=sign(-state[56]+1.000000)
    return state_49

cdef int __bool_fcn_56(int state[]):
    # [LexToken(ID,'State_PKC',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_RTK',1,19), LexToken(+,'+',1,28), LexToken(ID,'State_WNT',1,29), LexToken(RPAREN,')',1,38)]
    state_56=sign(+state[62]+state[78])
    return state_56

cdef int __bool_fcn_62(int state[]):
    # [LexToken(ID,'State_RTK',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_GFs',1,19), LexToken(RPAREN,')',1,28)]
    state_62=sign(+state[31])
    return state_62

cdef int __bool_fcn_59(int state[]):
    # [LexToken(ID,'State_RAGS',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_Nutrients',1,20), LexToken(-,'-',1,35), LexToken(ID,'State_Hypoxia',1,36), LexToken(RPAREN,')',1,49)]
    state_59=sign(+state[51]-state[38])
    return state_59

cdef int __bool_fcn_63(int state[]):
    # [LexToken(ID,'State_Ras',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(-,'-',1,18), LexToken(ID,'State_NF1',1,19), LexToken(+,'+',1,28), LexToken(ID,'State_RTK',1,29), LexToken(NUMBER,1.0,1,38), LexToken(RPAREN,')',1,40)]
    state_63=sign(-state[49]+state[62]+1.000000)
    return state_63

cdef int __bool_fcn_54(int state[]):
    # [LexToken(ID,'State_PI3K',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_Ras',1,20), LexToken(+,'+',1,29), LexToken(ID,'State_hTERT',1,30), LexToken(RPAREN,')',1,41)]
    state_54=sign(+state[63]+state[85])
    return state_54

cdef int __bool_fcn_57(int state[]):
    # [LexToken(ID,'State_PTEN',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(NUMBER,1.0,1,14)]
    state_57=+1.000000
    return sign(state_57)

cdef int __bool_fcn_55(int state[]):
    # [LexToken(ID,'State_PIP3',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_PI3K',1,20), LexToken(-,'-',1,30), LexToken(ID,'State_PTEN',1,31), LexToken(-,'-',1,41), LexToken(ID,'State_p53_PTEN',1,42), LexToken(NUMBER,1.0,1,56), LexToken(RPAREN,')',1,58)]
    state_55=sign(+state[54]-state[57]-state[93]+1.000000)
    return state_55

cdef int __bool_fcn_52(int state[]):
    # [LexToken(ID,'State_PDK1',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_PIP3',1,20), LexToken(+,'+',1,30), LexToken(ID,'State_HIF1',1,31), LexToken(+,'+',1,41), LexToken(ID,'State_Myc_Max',1,42), LexToken(RPAREN,')',1,55)]
    state_52=sign(+state[55]+state[37]+state[48])
    return state_52

cdef int __bool_fcn_39(int state[]):
    # [LexToken(ID,'State_IKK',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_PKC',1,19), LexToken(+,'+',1,28), LexToken(ID,'State_AKT',1,29), LexToken(+,'+',1,38), LexToken(ID,'State_mTOR',1,39), LexToken(-,'-',1,49), LexToken(ID,'State_PHDs',1,50), LexToken(-,'-',1,60), LexToken(ID,'State_p53',1,61), LexToken(+,'+',1,70), LexToken(ID,'State_TAK1',1,71), LexToken(RPAREN,')',1,81)]
    state_39=sign(+state[56]+state[0]+state[86]-state[53]-state[91]+state[70])
    return state_39

cdef int __bool_fcn_50(int state[]):
    # [LexToken(ID,'State_NFkappaB',1,0), LexToken(ASSIGN,'*=',1,15), LexToken(SIGN,'sign',1,18), LexToken(LPAREN,'(',1,22), LexToken(+,'+',1,23), LexToken(ID,'State_PIP3',1,24), LexToken(NUMBER,2.0,1,34), LexToken(*,'*',1,36), LexToken(ID,'State_IKK',1,37), LexToken(-,'-',1,46), LexToken(ID,'State_E_cadh',1,47), LexToken(+,'+',1,59), LexToken(ID,'State_Snail',1,60), LexToken(NUMBER,-1.0,1,71), LexToken(RPAREN,')',1,73)]
    state_50=sign(+state[55]+2.000000*state[39]-state[27]+state[69]-1.000000)
    return state_50

cdef int __bool_fcn_58(int state[]):
    # [LexToken(ID,'State_RAF',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_PKC',1,19), LexToken(+,'+',1,28), LexToken(ID,'State_Ras',1,29), LexToken(RPAREN,')',1,38)]
    state_58=sign(+state[56]+state[63])
    return state_58

cdef int __bool_fcn_26(int state[]):
    # [LexToken(ID,'State_ERK',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_RAF',1,19), LexToken(RPAREN,')',1,28)]
    state_26=sign(+state[58])
    return state_26

cdef int __bool_fcn_95(int state[]):
    # [LexToken(ID,'State_p90',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_PDK1',1,19), LexToken(+,'+',1,29), LexToken(ID,'State_ERK',1,30), LexToken(RPAREN,')',1,39)]
    state_95=sign(+state[52]+state[26])
    return state_95

cdef int __bool_fcn_0(int state[]):
    # [LexToken(ID,'State_AKT',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_PIP3',1,19), LexToken(+,'+',1,29), LexToken(ID,'State_PDK1',1,30), LexToken(NUMBER,-1.0,1,40), LexToken(RPAREN,')',1,42)]
    state_0=sign(+state[55]+state[52]-1.000000)
    return state_0

cdef int __bool_fcn_78(int state[]):
    # [LexToken(ID,'State_WNT',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(-,'-',1,18), LexToken(ID,'State_p53',1,19), LexToken(+,'+',1,28), LexToken(ID,'State_Gli',1,29), LexToken(RPAREN,')',1,38)]
    state_78=sign(-state[91]+state[35])
    return state_78

cdef int __bool_fcn_23(int state[]):
    # [LexToken(ID,'State_Dsh',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_WNT',1,19), LexToken(RPAREN,')',1,28)]
    state_23=sign(+state[78])
    return state_23

cdef int __bool_fcn_3(int state[]):
    # [LexToken(ID,'State_APC',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_PTEN',1,19), LexToken(NUMBER,1.0,1,29), LexToken(RPAREN,')',1,31)]
    state_3=sign(+state[57]+1.000000)
    return state_3

cdef int __bool_fcn_33(int state[]):
    # [LexToken(ID,'State_GSK_3',1,0), LexToken(ASSIGN,'*=',1,12), LexToken(SIGN,'sign',1,15), LexToken(LPAREN,'(',1,19), LexToken(-,'-',1,20), LexToken(ID,'State_p90',1,21), LexToken(-,'-',1,30), LexToken(ID,'State_AKT',1,31), LexToken(-,'-',1,40), LexToken(ID,'State_Dsh',1,41), LexToken(-,'-',1,50), LexToken(ID,'State_mTOR',1,51), LexToken(NUMBER,3.0,1,61), LexToken(RPAREN,')',1,63)]
    state_33=sign(-state[95]-state[0]-state[23]-state[86]+3.000000)
    return state_33

cdef int __bool_fcn_34(int state[]):
    # [LexToken(ID,'State_GSK_3_APC',1,0), LexToken(ASSIGN,'*=',1,16), LexToken(SIGN,'sign',1,19), LexToken(LPAREN,'(',1,23), LexToken(+,'+',1,24), LexToken(ID,'State_APC',1,25), LexToken(+,'+',1,34), LexToken(ID,'State_GSK_3',1,35), LexToken(NUMBER,-1.0,1,46), LexToken(RPAREN,')',1,48)]
    state_34=sign(+state[3]+state[33]-1.000000)
    return state_34

cdef int __bool_fcn_79(int state[]):
    # [LexToken(ID,'State_beta_cat',1,0), LexToken(ASSIGN,'*=',1,15), LexToken(SIGN,'sign',1,18), LexToken(LPAREN,'(',1,22), LexToken(-,'-',1,23), LexToken(ID,'State_GSK_3_APC',1,24), LexToken(-,'-',1,39), LexToken(ID,'State_p53',1,40), LexToken(NUMBER,1.0,1,49), LexToken(RPAREN,')',1,51)]
    state_79=sign(-state[34]-state[91]+1.000000)
    return state_79

cdef int __bool_fcn_65(int state[]):
    # [LexToken(ID,'State_Slug',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(-,'-',1,19), LexToken(ID,'State_p53_Mdm2',1,20), LexToken(+,'+',1,34), LexToken(ID,'State_NFkappaB',1,35), LexToken(+,'+',1,49), LexToken(ID,'State_TCF',1,50), LexToken(RPAREN,')',1,59)]
    state_65=sign(-state[92]+state[50]+state[71])
    return state_65

cdef int __bool_fcn_86(int state[]):
    # [LexToken(ID,'State_mTOR',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_RAGS',1,20), LexToken(+,'+',1,30), LexToken(ID,'State_AKT',1,31), LexToken(+,'+',1,40), LexToken(ID,'State_RHEB',1,41), LexToken(-,'-',1,51), LexToken(ID,'State_AMPK',1,52), LexToken(NUMBER,-1.0,1,62), LexToken(RPAREN,')',1,64)]
    state_86=sign(+state[59]+state[0]+state[60]-state[1]-1.000000)
    return state_86

cdef int __bool_fcn_37(int state[]):
    # [LexToken(ID,'State_HIF1',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_Hypoxia',1,20), LexToken(+,'+',1,33), LexToken(ID,'State_mTOR',1,34), LexToken(NUMBER,-2.0,1,44), LexToken(*,'*',1,46), LexToken(ID,'State_VHL',1,47), LexToken(-,'-',1,56), LexToken(ID,'State_PHDs',1,57), LexToken(+,'+',1,67), LexToken(ID,'State_Myc_Max',1,68), LexToken(-,'-',1,81), LexToken(ID,'State_p53',1,82), LexToken(-,'-',1,91), LexToken(ID,'State_FOXO',1,92), LexToken(NUMBER,2.0,1,102), LexToken(RPAREN,')',1,104)]
    state_37=sign(+state[38]+state[86]-2.000000*state[77]-state[53]+state[48]-state[91]-state[29]+2.000000)
    return state_37

cdef int __bool_fcn_13(int state[]):
    # [LexToken(ID,'State_COX412',1,0), LexToken(ASSIGN,'*=',1,13), LexToken(SIGN,'sign',1,16), LexToken(LPAREN,'(',1,20), LexToken(+,'+',1,21), LexToken(ID,'State_HIF1',1,22), LexToken(RPAREN,')',1,32)]
    state_13=sign(+state[37])
    return state_13

cdef int __bool_fcn_77(int state[]):
    # [LexToken(ID,'State_VHL',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(-,'-',1,18), LexToken(ID,'State_Hypoxia',1,19), LexToken(-,'-',1,32), LexToken(ID,'State_ROS',1,33), LexToken(NUMBER,1.0,1,42), LexToken(RPAREN,')',1,44)]
    state_77=sign(-state[38]-state[61]+1.000000)
    return state_77

cdef int __bool_fcn_53(int state[]):
    # [LexToken(ID,'State_PHDs',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(-,'-',1,19), LexToken(ID,'State_Hypoxia',1,20), LexToken(+,'+',1,33), LexToken(ID,'State_ROS',1,34), LexToken(NUMBER,1.0,1,43), LexToken(RPAREN,')',1,45)]
    state_53=sign(-state[38]+state[61]+1.000000)
    return state_53

cdef int __bool_fcn_48(int state[]):
    # [LexToken(ID,'State_Myc_Max',1,0), LexToken(ASSIGN,'*=',1,14), LexToken(SIGN,'sign',1,17), LexToken(LPAREN,'(',1,21), LexToken(-,'-',1,22), LexToken(ID,'State_TGFbeta',1,23), LexToken(+,'+',1,36), LexToken(ID,'State_Myc',1,37), LexToken(+,'+',1,46), LexToken(ID,'State_Max',1,47), LexToken(-,'-',1,56), LexToken(ID,'State_MXI1',1,57), LexToken(-,'-',1,67), LexToken(ID,'State_SmadE2F',1,68), LexToken(NUMBER,-1.0,1,81), LexToken(RPAREN,')',1,83)]
    state_48=sign(-state[72]+state[47]+state[43]-state[42]-state[67]-1.000000)
    return state_48

cdef int __bool_fcn_47(int state[]):
    # [LexToken(ID,'State_Myc',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_NFkappaB',1,19), LexToken(+,'+',1,33), LexToken(ID,'State_ERK',1,34), LexToken(-,'-',1,43), LexToken(ID,'State_HIF1',1,44), LexToken(+,'+',1,54), LexToken(ID,'State_E2F',1,55), LexToken(+,'+',1,64), LexToken(ID,'State_FosJun',1,65), LexToken(+,'+',1,77), LexToken(ID,'State_TCF',1,78), LexToken(+,'+',1,87), LexToken(ID,'State_Gli',1,88), LexToken(NUMBER,-1.0,1,97), LexToken(RPAREN,')',1,99)]
    state_47=sign(+state[50]+state[26]-state[37]+state[24]+state[30]+state[71]+state[35]-1.000000)
    return state_47

cdef int __bool_fcn_43(int state[]):
    # [LexToken(ID,'State_Max',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(NUMBER,1.0,1,13)]
    state_43=+1.000000
    return sign(state_43)

cdef int __bool_fcn_42(int state[]):
    # [LexToken(ID,'State_MXI1',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_HIF1',1,20), LexToken(RPAREN,')',1,30)]
    state_42=sign(+state[37])
    return state_42

cdef int __bool_fcn_74(int state[]):
    # [LexToken(ID,'State_TSC1_TSC2',1,0), LexToken(ASSIGN,'*=',1,16), LexToken(SIGN,'sign',1,19), LexToken(LPAREN,'(',1,23), LexToken(-,'-',1,24), LexToken(ID,'State_RAF',1,25), LexToken(-,'-',1,34), LexToken(ID,'State_ERK',1,35), LexToken(-,'-',1,44), LexToken(ID,'State_p90',1,45), LexToken(-,'-',1,54), LexToken(ID,'State_AKT',1,55), LexToken(+,'+',1,64), LexToken(ID,'State_HIF1',1,65), LexToken(+,'+',1,75), LexToken(ID,'State_p53',1,76), LexToken(+,'+',1,85), LexToken(ID,'State_AMPK',1,86), LexToken(NUMBER,1.0,1,96), LexToken(RPAREN,')',1,98)]
    state_74=sign(-state[58]-state[26]-state[95]-state[0]+state[37]+state[91]+state[1]+1.000000)
    return state_74

cdef int __bool_fcn_60(int state[]):
    # [LexToken(ID,'State_RHEB',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(-,'-',1,19), LexToken(ID,'State_TSC1_TSC2',1,20), LexToken(NUMBER,1.0,1,35), LexToken(RPAREN,')',1,37)]
    state_60=sign(-state[74]+1.000000)
    return state_60

cdef int __bool_fcn_91(int state[]):
    # [LexToken(ID,'State_p53',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_HIF1',1,19), LexToken(-,'-',1,29), LexToken(ID,'State_Bcl_2',1,30), LexToken(-,'-',1,41), LexToken(ID,'State_Mdm2',1,42), LexToken(+,'+',1,52), LexToken(ID,'State_CHK1_2',1,53), LexToken(NUMBER,1.0,1,65), LexToken(RPAREN,')',1,67)]
    state_91=sign(+state[37]-state[10]-state[44]+state[12]+1.000000)
    return state_91

cdef int __bool_fcn_10(int state[]):
    # [LexToken(ID,'State_Bcl_2',1,0), LexToken(ASSIGN,'*=',1,12), LexToken(SIGN,'sign',1,15), LexToken(LPAREN,'(',1,19), LexToken(NUMBER,2.0,1,20), LexToken(*,'*',1,22), LexToken(ID,'State_NFkappaB',1,23), LexToken(-,'-',1,37), LexToken(ID,'State_p53',1,38), LexToken(-,'-',1,47), LexToken(ID,'State_BAX',1,48), LexToken(-,'-',1,57), LexToken(ID,'State_BAD',1,58), LexToken(RPAREN,')',1,67)]
    state_10=sign(+2.000000*state[50]-state[91]-state[8]-state[7])
    return state_10

cdef int __bool_fcn_8(int state[]):
    # [LexToken(ID,'State_BAX',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(-,'-',1,18), LexToken(ID,'State_HIF1',1,19), LexToken(+,'+',1,29), LexToken(ID,'State_p53',1,30), LexToken(-,'-',1,39), LexToken(ID,'State_Bcl_2',1,40), LexToken(+,'+',1,51), LexToken(ID,'State_JNK',1,52), LexToken(RPAREN,')',1,61)]
    state_8=sign(-state[37]+state[91]-state[10]+state[40])
    return state_8

cdef int __bool_fcn_7(int state[]):
    # [LexToken(ID,'State_BAD',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(-,'-',1,18), LexToken(ID,'State_RAF',1,19), LexToken(-,'-',1,28), LexToken(ID,'State_p90',1,29), LexToken(-,'-',1,38), LexToken(ID,'State_AKT',1,39), LexToken(-,'-',1,48), LexToken(ID,'State_HIF1',1,49), LexToken(NUMBER,1.0,1,59), LexToken(RPAREN,')',1,61)]
    state_7=sign(-state[58]-state[95]-state[0]-state[37]+1.000000)
    return state_7

cdef int __bool_fcn_11(int state[]):
    # [LexToken(ID,'State_Bcl_XL',1,0), LexToken(ASSIGN,'*=',1,13), LexToken(SIGN,'sign',1,16), LexToken(LPAREN,'(',1,20), LexToken(-,'-',1,21), LexToken(ID,'State_p53',1,22), LexToken(-,'-',1,31), LexToken(ID,'State_BAD',1,32), LexToken(NUMBER,1.0,1,41), LexToken(RPAREN,')',1,43)]
    state_11=sign(-state[91]-state[7]+1.000000)
    return state_11

cdef int __bool_fcn_64(int state[]):
    # [LexToken(ID,'State_Rb',1,0), LexToken(ASSIGN,'*=',1,9), LexToken(SIGN,'sign',1,12), LexToken(LPAREN,'(',1,16), LexToken(-,'-',1,17), LexToken(ID,'State_CycA',1,18), LexToken(-,'-',1,28), LexToken(ID,'State_CycB',1,29), LexToken(-,'-',1,39), LexToken(ID,'State_CycD',1,40), LexToken(-,'-',1,50), LexToken(ID,'State_CycE',1,51), LexToken(-,'-',1,61), LexToken(ID,'State_Mdm2',1,62), LexToken(NUMBER,2.0,1,72), LexToken(RPAREN,')',1,74)]
    state_64=sign(-state[16]-state[17]-state[18]-state[19]-state[44]+2.000000)
    return state_64

cdef int __bool_fcn_24(int state[]):
    # [LexToken(ID,'State_E2F',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(NUMBER,-2.0,1,18), LexToken(*,'*',1,20), LexToken(ID,'State_Rb',1,21), LexToken(-,'-',1,29), LexToken(ID,'State_CycA',1,30), LexToken(-,'-',1,40), LexToken(ID,'State_CycB',1,41), LexToken(+,'+',1,51), LexToken(ID,'State_E2F',1,52), LexToken(NUMBER,1.0,1,61), LexToken(RPAREN,')',1,63)]
    state_24=sign(-2.000000*state[64]-state[16]-state[17]+state[24]+1.000000)
    return state_24

cdef int __bool_fcn_87(int state[]):
    # [LexToken(ID,'State_p14',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_Ras',1,19), LexToken(+,'+',1,28), LexToken(ID,'State_Myc_Max',1,29), LexToken(+,'+',1,42), LexToken(ID,'State_E2F',1,43), LexToken(NUMBER,-3.0,1,52), LexToken(RPAREN,')',1,54)]
    state_87=sign(+state[63]+state[48]+state[24]-3.000000)
    return state_87

cdef int __bool_fcn_16(int state[]):
    # [LexToken(ID,'State_CycA',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_CycA',1,20), LexToken(-,'-',1,30), LexToken(ID,'State_Rb',1,31), LexToken(-,'-',1,39), LexToken(ID,'State_cdc20',1,40), LexToken(-,'-',1,51), LexToken(ID,'State_p27',1,52), LexToken(-,'-',1,61), LexToken(ID,'State_p21',1,62), LexToken(+,'+',1,71), LexToken(ID,'State_E2F_CyclinE',1,72), LexToken(+,'+',1,89), LexToken(ID,'State_cdh1_UbcH10',1,90), LexToken(RPAREN,')',1,107)]
    state_16=sign(+state[16]-state[64]-state[80]-state[90]-state[89]+state[25]+state[82])
    return state_16

cdef int __bool_fcn_17(int state[]):
    # [LexToken(ID,'State_CycB',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(-,'-',1,19), LexToken(ID,'State_p53',1,20), LexToken(-,'-',1,29), LexToken(ID,'State_cdh1',1,30), LexToken(-,'-',1,40), LexToken(ID,'State_cdc20',1,41), LexToken(-,'-',1,52), LexToken(ID,'State_p27',1,53), LexToken(-,'-',1,62), LexToken(ID,'State_p21',1,63), LexToken(NUMBER,1.0,1,72), LexToken(RPAREN,')',1,74)]
    state_17=sign(-state[91]-state[81]-state[80]-state[90]-state[89]+1.000000)
    return state_17

cdef int __bool_fcn_18(int state[]):
    # [LexToken(ID,'State_CycD',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_NFkappaB',1,20), LexToken(NUMBER,-2.0,1,34), LexToken(*,'*',1,36), LexToken(ID,'State_GSK_3',1,37), LexToken(+,'+',1,48), LexToken(ID,'State_Myc_Max',1,49), LexToken(-,'-',1,62), LexToken(ID,'State_p27',1,63), LexToken(-,'-',1,72), LexToken(ID,'State_p21',1,73), LexToken(-,'-',1,82), LexToken(ID,'State_p15',1,83), LexToken(-,'-',1,92), LexToken(ID,'State_FOXO',1,93), LexToken(+,'+',1,103), LexToken(ID,'State_FosJun',1,104), LexToken(+,'+',1,116), LexToken(ID,'State_TCF',1,117), LexToken(+,'+',1,126), LexToken(ID,'State_Gli',1,127), LexToken(RPAREN,')',1,136)]
    state_18=sign(+state[50]-2.000000*state[33]+state[48]-state[90]-state[89]-state[88]-state[29]+state[30]+state[71]+state[35])
    return state_18

cdef int __bool_fcn_19(int state[]):
    # [LexToken(ID,'State_CycE',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(-,'-',1,19), LexToken(ID,'State_Rb',1,20), LexToken(+,'+',1,28), LexToken(ID,'State_E2F',1,29), LexToken(-,'-',1,38), LexToken(ID,'State_CycA',1,39), LexToken(-,'-',1,49), LexToken(ID,'State_p27',1,50), LexToken(-,'-',1,59), LexToken(ID,'State_p21',1,60), LexToken(RPAREN,')',1,69)]
    state_19=sign(-state[64]+state[24]-state[16]-state[90]-state[89])
    return state_19

cdef int __bool_fcn_81(int state[]):
    # [LexToken(ID,'State_cdh1',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(-,'-',1,19), LexToken(ID,'State_CycA',1,20), LexToken(-,'-',1,30), LexToken(ID,'State_CycB',1,31), LexToken(+,'+',1,41), LexToken(ID,'State_cdc20',1,42), LexToken(NUMBER,1.0,1,53), LexToken(RPAREN,')',1,55)]
    state_81=sign(-state[16]-state[17]+state[80]+1.000000)
    return state_81

cdef int __bool_fcn_80(int state[]):
    # [LexToken(ID,'State_cdc20',1,0), LexToken(ASSIGN,'*=',1,12), LexToken(SIGN,'sign',1,15), LexToken(LPAREN,'(',1,19), LexToken(+,'+',1,20), LexToken(ID,'State_CycB',1,21), LexToken(-,'-',1,31), LexToken(ID,'State_cdh1',1,32), LexToken(RPAREN,')',1,42)]
    state_80=sign(+state[17]-state[81])
    return state_80

cdef int __bool_fcn_75(int state[]):
    # [LexToken(ID,'State_UbcH10',1,0), LexToken(ASSIGN,'*=',1,13), LexToken(SIGN,'sign',1,16), LexToken(LPAREN,'(',1,20), LexToken(+,'+',1,21), LexToken(ID,'State_CycA',1,22), LexToken(+,'+',1,32), LexToken(ID,'State_CycB',1,33), LexToken(-,'-',1,43), LexToken(ID,'State_cdh1',1,44), LexToken(+,'+',1,54), LexToken(ID,'State_cdc20',1,55), LexToken(+,'+',1,66), LexToken(ID,'State_UbcH10',1,67), LexToken(RPAREN,')',1,79)]
    state_75=sign(+state[16]+state[17]-state[81]+state[80]+state[75])
    return state_75

cdef int __bool_fcn_90(int state[]):
    # [LexToken(ID,'State_p27',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(-,'-',1,18), LexToken(ID,'State_AKT',1,19), LexToken(+,'+',1,28), LexToken(ID,'State_HIF1',1,29), LexToken(-,'-',1,39), LexToken(ID,'State_Myc_Max',1,40), LexToken(-,'-',1,53), LexToken(ID,'State_CycA',1,54), LexToken(-,'-',1,64), LexToken(ID,'State_CycB',1,65), LexToken(-,'-',1,75), LexToken(ID,'State_CycD',1,76), LexToken(+,'+',1,86), LexToken(ID,'State_SmadMiz_1',1,87), LexToken(NUMBER,1.0,1,102), LexToken(RPAREN,')',1,104)]
    state_90=sign(-state[0]+state[37]-state[48]-state[16]-state[17]-state[18]+state[68]+1.000000)
    return state_90

cdef int __bool_fcn_89(int state[]):
    # [LexToken(ID,'State_p21',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(-,'-',1,18), LexToken(ID,'State_AKT',1,19), LexToken(+,'+',1,28), LexToken(ID,'State_HIF1',1,29), LexToken(-,'-',1,39), LexToken(ID,'State_Myc_Max',1,40), LexToken(+,'+',1,53), LexToken(ID,'State_p53',1,54), LexToken(+,'+',1,63), LexToken(ID,'State_SmadMiz_1',1,64), LexToken(-,'-',1,79), LexToken(ID,'State_hTERT',1,80), LexToken(NUMBER,1.0,1,91), LexToken(RPAREN,')',1,93)]
    state_89=sign(-state[0]+state[37]-state[48]+state[91]+state[68]-state[85]+1.000000)
    return state_89

cdef int __bool_fcn_44(int state[]):
    # [LexToken(ID,'State_Mdm2',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_AKT',1,20), LexToken(+,'+',1,29), LexToken(ID,'State_p53',1,30), LexToken(-,'-',1,39), LexToken(ID,'State_p14',1,40), LexToken(-,'-',1,49), LexToken(ID,'State_ATM_ATR',1,50), LexToken(NUMBER,1.0,1,63), LexToken(RPAREN,')',1,65)]
    state_44=sign(+state[0]+state[91]-state[87]-state[4]+1.000000)
    return state_44

cdef int __bool_fcn_66(int state[]):
    # [LexToken(ID,'State_Smad',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_TNFalpha',1,20), LexToken(+,'+',1,34), LexToken(ID,'State_TGFbeta',1,35), LexToken(RPAREN,')',1,48)]
    state_66=sign(+state[73]+state[72])
    return state_66

cdef int __bool_fcn_68(int state[]):
    # [LexToken(ID,'State_SmadMiz_1',1,0), LexToken(ASSIGN,'*=',1,16), LexToken(SIGN,'sign',1,19), LexToken(LPAREN,'(',1,23), LexToken(+,'+',1,24), LexToken(ID,'State_Smad',1,25), LexToken(+,'+',1,35), LexToken(ID,'State_Miz_1',1,36), LexToken(NUMBER,-1.0,1,47), LexToken(RPAREN,')',1,49)]
    state_68=sign(+state[66]+state[45]-1.000000)
    return state_68

cdef int __bool_fcn_67(int state[]):
    # [LexToken(ID,'State_SmadE2F',1,0), LexToken(ASSIGN,'*=',1,14), LexToken(SIGN,'sign',1,17), LexToken(LPAREN,'(',1,21), LexToken(+,'+',1,22), LexToken(ID,'State_Smad',1,23), LexToken(RPAREN,')',1,33)]
    state_67=sign(+state[66])
    return state_67

cdef int __bool_fcn_88(int state[]):
    # [LexToken(ID,'State_p15',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_SmadMiz_1',1,19), LexToken(+,'+',1,34), LexToken(ID,'State_Miz_1',1,35), LexToken(RPAREN,')',1,46)]
    state_88=sign(+state[68]+state[45])
    return state_88

cdef int __bool_fcn_28(int state[]):
    # [LexToken(ID,'State_FADD',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_TNFalpha',1,20), LexToken(RPAREN,')',1,34)]
    state_28=sign(+state[73])
    return state_28

cdef int __bool_fcn_14(int state[]):
    # [LexToken(ID,'State_Caspase8',1,0), LexToken(ASSIGN,'*=',1,15), LexToken(SIGN,'sign',1,18), LexToken(LPAREN,'(',1,22), LexToken(+,'+',1,23), LexToken(ID,'State_FADD',1,24), LexToken(RPAREN,')',1,34)]
    state_14=sign(+state[28])
    return state_14

cdef int __bool_fcn_9(int state[]):
    # [LexToken(ID,'State_Bak',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_Caspase8',1,19), LexToken(RPAREN,')',1,33)]
    state_9=sign(+state[14])
    return state_9

cdef int __bool_fcn_40(int state[]):
    # [LexToken(ID,'State_JNK',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_TGFbeta',1,19), LexToken(RPAREN,')',1,32)]
    state_40=sign(+state[72])
    return state_40

cdef int __bool_fcn_29(int state[]):
    # [LexToken(ID,'State_FOXO',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(-,'-',1,19), LexToken(ID,'State_AKT',1,20), LexToken(NUMBER,2.0,1,29), LexToken(RPAREN,')',1,31)]
    state_29=sign(-state[0]+2.000000)
    return state_29

cdef int __bool_fcn_30(int state[]):
    # [LexToken(ID,'State_FosJun',1,0), LexToken(ASSIGN,'*=',1,13), LexToken(SIGN,'sign',1,16), LexToken(LPAREN,'(',1,20), LexToken(+,'+',1,21), LexToken(ID,'State_ERK',1,22), LexToken(+,'+',1,31), LexToken(ID,'State_JNK',1,32), LexToken(RPAREN,')',1,41)]
    state_30=sign(+state[26]+state[40])
    return state_30

cdef int __bool_fcn_61(int state[]):
    # [LexToken(ID,'State_ROS',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(-,'-',1,18), LexToken(ID,'State_COX412',1,19), LexToken(-,'-',1,31), LexToken(ID,'State_GSH',1,32), LexToken(RPAREN,')',1,41)]
    state_61=sign(-state[13]-state[32])
    return state_61

cdef int __bool_fcn_1(int state[]):
    # [LexToken(ID,'State_AMPK',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(-,'-',1,19), LexToken(ID,'State_GFs',1,20), LexToken(+,'+',1,29), LexToken(ID,'State_AMP_ATP',1,30), LexToken(+,'+',1,43), LexToken(ID,'State_HIF1',1,44), LexToken(+,'+',1,54), LexToken(ID,'State_ATM_ATR',1,55), LexToken(NUMBER,1.0,1,68), LexToken(RPAREN,')',1,70)]
    state_1=sign(-state[31]+state[2]+state[37]+state[4]+1.000000)
    return state_1

cdef int __bool_fcn_20(int state[]):
    # [LexToken(ID,'State_Cytoc_APAF1',1,0), LexToken(ASSIGN,'*=',1,18), LexToken(SIGN,'sign',1,21), LexToken(LPAREN,'(',1,25), LexToken(-,'-',1,26), LexToken(ID,'State_AKT',1,27), LexToken(+,'+',1,36), LexToken(ID,'State_p53',1,37), LexToken(-,'-',1,46), LexToken(ID,'State_Bcl_2',1,47), LexToken(+,'+',1,58), LexToken(ID,'State_BAX',1,59), LexToken(-,'-',1,68), LexToken(ID,'State_Bcl_XL',1,69), LexToken(+,'+',1,81), LexToken(ID,'State_Caspase8',1,82), LexToken(+,'+',1,96), LexToken(ID,'State_Bak',1,97), LexToken(RPAREN,')',1,106)]
    state_20=sign(-state[0]+state[91]-state[10]+state[8]-state[11]+state[14]+state[9])
    return state_20

cdef int __bool_fcn_15(int state[]):
    # [LexToken(ID,'State_Caspase9',1,0), LexToken(ASSIGN,'*=',1,15), LexToken(SIGN,'sign',1,18), LexToken(LPAREN,'(',1,22), LexToken(+,'+',1,23), LexToken(ID,'State_Cytoc_APAF1',1,24), LexToken(RPAREN,')',1,41)]
    state_15=sign(+state[20])
    return state_15

cdef int __bool_fcn_6(int state[]):
    # [LexToken(ID,'State_Apoptosis',1,0), LexToken(ASSIGN,'*=',1,16), LexToken(SIGN,'sign',1,19), LexToken(LPAREN,'(',1,23), LexToken(+,'+',1,24), LexToken(ID,'State_Caspase8',1,25), LexToken(+,'+',1,39), LexToken(ID,'State_Caspase9',1,40), LexToken(RPAREN,')',1,54)]
    state_6=sign(+state[14]+state[15])
    return state_6

cdef int __bool_fcn_27(int state[]):
    # [LexToken(ID,'State_E_cadh',1,0), LexToken(ASSIGN,'*=',1,13), LexToken(SIGN,'sign',1,16), LexToken(LPAREN,'(',1,20), LexToken(-,'-',1,21), LexToken(ID,'State_NFkappaB',1,22), LexToken(-,'-',1,36), LexToken(ID,'State_Slug',1,37), LexToken(-,'-',1,47), LexToken(ID,'State_Snail',1,48), LexToken(NUMBER,3.0,1,59), LexToken(RPAREN,')',1,61)]
    state_27=sign(-state[50]-state[65]-state[69]+3.000000)
    return state_27

cdef int __bool_fcn_36(int state[]):
    # [LexToken(ID,'State_Glut_1',1,0), LexToken(ASSIGN,'*=',1,13), LexToken(SIGN,'sign',1,16), LexToken(LPAREN,'(',1,20), LexToken(+,'+',1,21), LexToken(ID,'State_AKT',1,22), LexToken(+,'+',1,31), LexToken(ID,'State_HIF1',1,32), LexToken(+,'+',1,42), LexToken(ID,'State_Myc_Max',1,43), LexToken(NUMBER,-1.0,1,56), LexToken(RPAREN,')',1,58)]
    state_36=sign(+state[0]+state[37]+state[48]-1.000000)
    return state_36

cdef int __bool_fcn_85(int state[]):
    # [LexToken(ID,'State_hTERT',1,0), LexToken(ASSIGN,'*=',1,12), LexToken(SIGN,'sign',1,15), LexToken(LPAREN,'(',1,19), LexToken(+,'+',1,20), LexToken(ID,'State_NF1',1,21), LexToken(+,'+',1,30), LexToken(ID,'State_NFkappaB',1,31), LexToken(+,'+',1,45), LexToken(ID,'State_AKT',1,46), LexToken(+,'+',1,55), LexToken(ID,'State_HIF1',1,56), LexToken(+,'+',1,66), LexToken(ID,'State_Myc_Max',1,67), LexToken(-,'-',1,80), LexToken(ID,'State_p53',1,81), LexToken(-,'-',1,90), LexToken(ID,'State_SmadMiz_1',1,91), LexToken(-,'-',1,106), LexToken(ID,'State_eEF2',1,107), LexToken(NUMBER,-4.0,1,117), LexToken(RPAREN,')',1,119)]
    state_85=sign(+state[49]+state[50]+state[0]+state[37]+state[48]-state[91]-state[68]-state[83]-4.000000)
    return state_85

cdef int __bool_fcn_76(int state[]):
    # [LexToken(ID,'State_VEGF',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_HIF1',1,20), LexToken(+,'+',1,30), LexToken(ID,'State_Myc_Max',1,31), LexToken(RPAREN,')',1,44)]
    state_76=sign(+state[37]+state[48])
    return state_76

cdef int __bool_fcn_25(int state[]):
    # [LexToken(ID,'State_E2F_CyclinE',1,0), LexToken(ASSIGN,'*=',1,18), LexToken(SIGN,'sign',1,21), LexToken(LPAREN,'(',1,25), LexToken(+,'+',1,26), LexToken(ID,'State_E2F',1,27), LexToken(+,'+',1,36), LexToken(ID,'State_CycE',1,37), LexToken(NUMBER,-1.0,1,47), LexToken(RPAREN,')',1,49)]
    state_25=sign(+state[24]+state[19]-1.000000)
    return state_25

cdef int __bool_fcn_82(int state[]):
    # [LexToken(ID,'State_cdh1_UbcH10',1,0), LexToken(ASSIGN,'*=',1,18), LexToken(SIGN,'sign',1,21), LexToken(LPAREN,'(',1,25), LexToken(+,'+',1,26), LexToken(ID,'State_cdh1',1,27), LexToken(+,'+',1,37), LexToken(ID,'State_UbcH10',1,38), LexToken(NUMBER,-1.0,1,50), LexToken(RPAREN,')',1,52)]
    state_82=sign(+state[81]+state[75]-1.000000)
    return state_82

cdef int __bool_fcn_70(int state[]):
    # [LexToken(ID,'State_TAK1',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_TNFalpha',1,20), LexToken(RPAREN,')',1,34)]
    state_70=sign(+state[73])
    return state_70

cdef int __bool_fcn_32(int state[]):
    # [LexToken(ID,'State_GSH',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_NFkappaB',1,19), LexToken(+,'+',1,33), LexToken(ID,'State_Myc_Max',1,34), LexToken(+,'+',1,47), LexToken(ID,'State_p21',1,48), LexToken(RPAREN,')',1,57)]
    state_32=sign(+state[50]+state[48]+state[89])
    return state_32

cdef int __bool_fcn_71(int state[]):
    # [LexToken(ID,'State_TCF',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_beta_cat',1,19), LexToken(-,'-',1,33), LexToken(ID,'State_TAK1',1,34), LexToken(RPAREN,')',1,44)]
    state_71=sign(+state[79]-state[70])
    return state_71

cdef int __bool_fcn_45(int state[]):
    # [LexToken(ID,'State_Miz_1',1,0), LexToken(ASSIGN,'*=',1,12), LexToken(SIGN,'sign',1,15), LexToken(LPAREN,'(',1,19), LexToken(-,'-',1,20), LexToken(ID,'State_Myc_Max',1,21), LexToken(NUMBER,1.0,1,34), LexToken(RPAREN,')',1,36)]
    state_45=sign(-state[48]+1.000000)
    return state_45

cdef int __bool_fcn_94(int state[]):
    # [LexToken(ID,'State_p70',1,0), LexToken(ASSIGN,'*=',1,10), LexToken(SIGN,'sign',1,13), LexToken(LPAREN,'(',1,17), LexToken(+,'+',1,18), LexToken(ID,'State_PDK1',1,19), LexToken(+,'+',1,29), LexToken(ID,'State_mTOR',1,30), LexToken(RPAREN,')',1,40)]
    state_94=sign(+state[52]+state[86])
    return state_94

cdef int __bool_fcn_4(int state[]):
    # [LexToken(ID,'State_ATM_ATR',1,0), LexToken(ASSIGN,'*=',1,14), LexToken(SIGN,'sign',1,17), LexToken(LPAREN,'(',1,21), LexToken(+,'+',1,22), LexToken(ID,'State_DnaDamage',1,23), LexToken(RPAREN,')',1,38)]
    state_4=sign(+state[22])
    return state_4

cdef int __bool_fcn_12(int state[]):
    # [LexToken(ID,'State_CHK1_2',1,0), LexToken(ASSIGN,'*=',1,13), LexToken(SIGN,'sign',1,16), LexToken(LPAREN,'(',1,20), LexToken(+,'+',1,21), LexToken(ID,'State_ATM_ATR',1,22), LexToken(RPAREN,')',1,35)]
    state_12=sign(+state[4])
    return state_12

cdef int __bool_fcn_21(int state[]):
    # [LexToken(ID,'State_DNARepair',1,0), LexToken(ASSIGN,'*=',1,16), LexToken(SIGN,'sign',1,19), LexToken(LPAREN,'(',1,23), LexToken(+,'+',1,24), LexToken(ID,'State_ATM_ATR',1,25), LexToken(RPAREN,')',1,38)]
    state_21=sign(+state[4])
    return state_21

cdef int __bool_fcn_84(int state[]):
    # [LexToken(ID,'State_eEF2K',1,0), LexToken(ASSIGN,'*=',1,12), LexToken(SIGN,'sign',1,15), LexToken(LPAREN,'(',1,19), LexToken(+,'+',1,20), LexToken(ID,'State_p90',1,21), LexToken(+,'+',1,30), LexToken(ID,'State_p70',1,31), LexToken(RPAREN,')',1,40)]
    state_84=sign(+state[95]+state[94])
    return state_84

cdef int __bool_fcn_83(int state[]):
    # [LexToken(ID,'State_eEF2',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(-,'-',1,19), LexToken(ID,'State_eEF2K',1,20), LexToken(NUMBER,1.0,1,31), LexToken(RPAREN,')',1,33)]
    state_83=sign(-state[84]+1.000000)
    return state_83

cdef int __bool_fcn_93(int state[]):
    # [LexToken(ID,'State_p53_PTEN',1,0), LexToken(ASSIGN,'*=',1,15), LexToken(SIGN,'sign',1,18), LexToken(LPAREN,'(',1,22), LexToken(+,'+',1,23), LexToken(ID,'State_PTEN',1,24), LexToken(+,'+',1,34), LexToken(ID,'State_p53',1,35), LexToken(NUMBER,-1.0,1,44), LexToken(RPAREN,')',1,46)]
    state_93=sign(+state[57]+state[91]-1.000000)
    return state_93

cdef int __bool_fcn_41(int state[]):
    # [LexToken(ID,'State_LDHA',1,0), LexToken(ASSIGN,'*=',1,11), LexToken(SIGN,'sign',1,14), LexToken(LPAREN,'(',1,18), LexToken(+,'+',1,19), LexToken(ID,'State_HIF1',1,20), LexToken(+,'+',1,30), LexToken(ID,'State_Myc_Max',1,31), LexToken(NUMBER,-1.0,1,44), LexToken(RPAREN,')',1,46)]
    state_41=sign(+state[37]+state[48]-1.000000)
    return state_41

cdef int __bool_fcn_5(int state[]):
    # [LexToken(ID,'State_AcidLactic',1,0), LexToken(ASSIGN,'*=',1,17), LexToken(SIGN,'sign',1,20), LexToken(LPAREN,'(',1,24), LexToken(+,'+',1,25), LexToken(ID,'State_LDHA',1,26), LexToken(RPAREN,')',1,36)]
    state_5=sign(+state[41])
    return state_5

cdef int __bool_fcn_69(int state[]):
    # [LexToken(ID,'State_Snail',1,0), LexToken(ASSIGN,'*=',1,12), LexToken(SIGN,'sign',1,15), LexToken(LPAREN,'(',1,19), LexToken(+,'+',1,20), LexToken(ID,'State_NFkappaB',1,21), LexToken(-,'-',1,35), LexToken(ID,'State_GSK_3',1,36), LexToken(-,'-',1,47), LexToken(ID,'State_p53',1,48), LexToken(+,'+',1,57), LexToken(ID,'State_Smad',1,58), LexToken(NUMBER,-1.0,1,68), LexToken(RPAREN,')',1,70)]
    state_69=sign(+state[50]-state[33]-state[91]+state[66]-1.000000)
    return state_69

cdef int __bool_fcn_31(int state[]):
    state_31 = sign(state[31])
    return state_31

cdef int __bool_fcn_35(int state[]):
    state_35 = sign(state[35])
    return state_35

cdef int __bool_fcn_38(int state[]):
    state_38 = sign(state[38])
    return state_38

cdef int __bool_fcn_46(int state[]):
    state_46 = sign(state[46])
    return state_46

cdef int __bool_fcn_51(int state[]):
    state_51 = sign(state[51])
    return state_51

cdef int __bool_fcn_73(int state[]):
    state_73 = sign(state[73])
    return state_73

eqlist[0] = &__bool_fcn_0
eqlist[1] = &__bool_fcn_1
eqlist[2] = &__bool_fcn_2
eqlist[3] = &__bool_fcn_3
eqlist[4] = &__bool_fcn_4
eqlist[5] = &__bool_fcn_5
eqlist[6] = &__bool_fcn_6
eqlist[7] = &__bool_fcn_7
eqlist[8] = &__bool_fcn_8
eqlist[9] = &__bool_fcn_9
eqlist[10] = &__bool_fcn_10
eqlist[11] = &__bool_fcn_11
eqlist[12] = &__bool_fcn_12
eqlist[13] = &__bool_fcn_13
eqlist[14] = &__bool_fcn_14
eqlist[15] = &__bool_fcn_15
eqlist[16] = &__bool_fcn_16
eqlist[17] = &__bool_fcn_17
eqlist[18] = &__bool_fcn_18
eqlist[19] = &__bool_fcn_19
eqlist[20] = &__bool_fcn_20
eqlist[21] = &__bool_fcn_21
eqlist[22] = &__bool_fcn_22
eqlist[23] = &__bool_fcn_23
eqlist[24] = &__bool_fcn_24
eqlist[25] = &__bool_fcn_25
eqlist[26] = &__bool_fcn_26
eqlist[27] = &__bool_fcn_27
eqlist[28] = &__bool_fcn_28
eqlist[29] = &__bool_fcn_29
eqlist[30] = &__bool_fcn_30
eqlist[31] = &__bool_fcn_31
eqlist[32] = &__bool_fcn_32
eqlist[33] = &__bool_fcn_33
eqlist[34] = &__bool_fcn_34
eqlist[35] = &__bool_fcn_35
eqlist[36] = &__bool_fcn_36
eqlist[37] = &__bool_fcn_37
eqlist[38] = &__bool_fcn_38
eqlist[39] = &__bool_fcn_39
eqlist[40] = &__bool_fcn_40
eqlist[41] = &__bool_fcn_41
eqlist[42] = &__bool_fcn_42
eqlist[43] = &__bool_fcn_43
eqlist[44] = &__bool_fcn_44
eqlist[45] = &__bool_fcn_45
eqlist[46] = &__bool_fcn_46
eqlist[47] = &__bool_fcn_47
eqlist[48] = &__bool_fcn_48
eqlist[49] = &__bool_fcn_49
eqlist[50] = &__bool_fcn_50
eqlist[51] = &__bool_fcn_51
eqlist[52] = &__bool_fcn_52
eqlist[53] = &__bool_fcn_53
eqlist[54] = &__bool_fcn_54
eqlist[55] = &__bool_fcn_55
eqlist[56] = &__bool_fcn_56
eqlist[57] = &__bool_fcn_57
eqlist[58] = &__bool_fcn_58
eqlist[59] = &__bool_fcn_59
eqlist[60] = &__bool_fcn_60
eqlist[61] = &__bool_fcn_61
eqlist[62] = &__bool_fcn_62
eqlist[63] = &__bool_fcn_63
eqlist[64] = &__bool_fcn_64
eqlist[65] = &__bool_fcn_65
eqlist[66] = &__bool_fcn_66
eqlist[67] = &__bool_fcn_67
eqlist[68] = &__bool_fcn_68
eqlist[69] = &__bool_fcn_69
eqlist[70] = &__bool_fcn_70
eqlist[71] = &__bool_fcn_71
eqlist[72] = &__bool_fcn_72
eqlist[73] = &__bool_fcn_73
eqlist[74] = &__bool_fcn_74
eqlist[75] = &__bool_fcn_75
eqlist[76] = &__bool_fcn_76
eqlist[77] = &__bool_fcn_77
eqlist[78] = &__bool_fcn_78
eqlist[79] = &__bool_fcn_79
eqlist[80] = &__bool_fcn_80
eqlist[81] = &__bool_fcn_81
eqlist[82] = &__bool_fcn_82
eqlist[83] = &__bool_fcn_83
eqlist[84] = &__bool_fcn_84
eqlist[85] = &__bool_fcn_85
eqlist[86] = &__bool_fcn_86
eqlist[87] = &__bool_fcn_87
eqlist[88] = &__bool_fcn_88
eqlist[89] = &__bool_fcn_89
eqlist[90] = &__bool_fcn_90
eqlist[91] = &__bool_fcn_91
eqlist[92] = &__bool_fcn_92
eqlist[93] = &__bool_fcn_93
eqlist[94] = &__bool_fcn_94
eqlist[95] = &__bool_fcn_95

cdef int state0[num_nodes]
cdef int state1[num_nodes]

def simulate(steps=10, on_states=[], off_states=[]):
    node_list = ['State_AKT', 'State_AMPK', 'State_AMP_ATP', 'State_APC', 'State_ATM_ATR', 'State_AcidLactic', 'State_Apoptosis', 'State_BAD', 'State_BAX', 'State_Bak', 'State_Bcl_2', 'State_Bcl_XL', 'State_CHK1_2', 'State_COX412', 'State_Caspase8', 'State_Caspase9', 'State_CycA', 'State_CycB', 'State_CycD', 'State_CycE', 'State_Cytoc_APAF1', 'State_DNARepair', 'State_DnaDamage', 'State_Dsh', 'State_E2F', 'State_E2F_CyclinE', 'State_ERK', 'State_E_cadh', 'State_FADD', 'State_FOXO', 'State_FosJun', 'State_GFs', 'State_GSH', 'State_GSK_3', 'State_GSK_3_APC', 'State_Gli', 'State_Glut_1', 'State_HIF1', 'State_Hypoxia', 'State_IKK', 'State_JNK', 'State_LDHA', 'State_MXI1', 'State_Max', 'State_Mdm2', 'State_Miz_1', 'State_Mutagen', 'State_Myc', 'State_Myc_Max', 'State_NF1', 'State_NFkappaB', 'State_Nutrients', 'State_PDK1', 'State_PHDs', 'State_PI3K', 'State_PIP3', 'State_PKC', 'State_PTEN', 'State_RAF', 'State_RAGS', 'State_RHEB', 'State_ROS', 'State_RTK', 'State_Ras', 'State_Rb', 'State_Slug', 'State_Smad', 'State_SmadE2F', 'State_SmadMiz_1', 'State_Snail', 'State_TAK1', 'State_TCF', 'State_TGFbeta', 'State_TNFalpha', 'State_TSC1_TSC2', 'State_UbcH10', 'State_VEGF', 'State_VHL', 'State_WNT', 'State_beta_cat', 'State_cdc20', 'State_cdh1', 'State_cdh1_UbcH10', 'State_eEF2', 'State_eEF2K', 'State_hTERT', 'State_mTOR', 'State_p14', 'State_p15', 'State_p21', 'State_p27', 'State_p53', 'State_p53_Mdm2', 'State_p53_PTEN', 'State_p70', 'State_p90']
    state0[46]=False
    state0[31]=False
    state0[51]=False
    state0[73]=False
    state0[38]=False
    state0[35]=False
    state0[72]=random()>0.5
    state0[22]=random()>0.5
    state0[92]=random()>0.5
    state0[2]=random()>0.5
    state0[49]=random()>0.5
    state0[56]=random()>0.5
    state0[62]=random()>0.5
    state0[59]=random()>0.5
    state0[63]=random()>0.5
    state0[54]=random()>0.5
    state0[57]=random()>0.5
    state0[55]=random()>0.5
    state0[52]=random()>0.5
    state0[39]=random()>0.5
    state0[50]=random()>0.5
    state0[58]=random()>0.5
    state0[26]=random()>0.5
    state0[95]=random()>0.5
    state0[0]=random()>0.5
    state0[78]=random()>0.5
    state0[23]=random()>0.5
    state0[3]=random()>0.5
    state0[33]=random()>0.5
    state0[34]=random()>0.5
    state0[79]=random()>0.5
    state0[65]=random()>0.5
    state0[86]=random()>0.5
    state0[37]=random()>0.5
    state0[13]=random()>0.5
    state0[77]=random()>0.5
    state0[53]=random()>0.5
    state0[48]=random()>0.5
    state0[47]=random()>0.5
    state0[43]=random()>0.5
    state0[42]=random()>0.5
    state0[74]=random()>0.5
    state0[60]=random()>0.5
    state0[91]=random()>0.5
    state0[10]=random()>0.5
    state0[8]=random()>0.5
    state0[7]=random()>0.5
    state0[11]=random()>0.5
    state0[64]=random()>0.5
    state0[24]=random()>0.5
    state0[87]=random()>0.5
    state0[16]=random()>0.5
    state0[17]=random()>0.5
    state0[18]=random()>0.5
    state0[19]=random()>0.5
    state0[81]=random()>0.5
    state0[80]=random()>0.5
    state0[75]=random()>0.5
    state0[90]=random()>0.5
    state0[89]=random()>0.5
    state0[44]=random()>0.5
    state0[66]=random()>0.5
    state0[68]=random()>0.5
    state0[67]=random()>0.5
    state0[88]=random()>0.5
    state0[28]=random()>0.5
    state0[14]=random()>0.5
    state0[9]=random()>0.5
    state0[40]=random()>0.5
    state0[29]=random()>0.5
    state0[30]=random()>0.5
    state0[61]=random()>0.5
    state0[1]=random()>0.5
    state0[20]=random()>0.5
    state0[15]=random()>0.5
    state0[6]=random()>0.5
    state0[27]=random()>0.5
    state0[36]=random()>0.5
    state0[85]=random()>0.5
    state0[76]=random()>0.5
    state0[25]=random()>0.5
    state0[82]=random()>0.5
    state0[70]=random()>0.5
    state0[32]=random()>0.5
    state0[71]=random()>0.5
    state0[45]=random()>0.5
    state0[94]=random()>0.5
    state0[4]=random()>0.5
    state0[12]=random()>0.5
    state0[21]=random()>0.5
    state0[84]=random()>0.5
    state0[83]=random()>0.5
    state0[93]=random()>0.5
    state0[41]=random()>0.5
    state0[5]=random()>0.5
    state0[69]=random()>0.5
    state0[46]=state0[46]
    state0[31]=state0[31]
    state0[51]=state0[51]
    state0[73]=state0[73]
    state0[38]=state0[38]
    state0[35]=state0[35]
    on_idxes = [ node_list.index(s) for s in on_states]
    off_idxes = [ node_list.index(s) for s in off_states]
    state_list = []
    state_list.append(state0)

    for i in range(steps):
        for k in range(num_nodes):
            state1[k] = eqlist[k](state0)
        for k in on_idxes:
            state1[k] = True
        for k in off_idxes:
            state1[k] = False
        for k in range(num_nodes):
            state0[k] = state1[k]
        state_list.append(state0)

    return state_list


def fp(s):
    res = hashlib.sha224(repr(s).encode('utf-8')).hexdigest()
    return res[0:FP_LENGTH]

def prettify(state_data, trajectory=False):
    if trajectory==False: 
        return "".join( ['%d'%s for s in state_data] )        
    else:
        traj_value = [] 
        for state in state_data: 
            state_str = []
            for st0 in state:
                state_str.append('%d' % st0)

            traj_value.append("".join(state_str))

        return "-".join(traj_value)

def main(steps, samples, debug, on_states, off_states):
    res = {}
    seen = {}
    traj = {}    
    for i in range(samples):
        values = simulate(steps=steps, on_states=on_states, off_states=off_states)
        idx, size = detect_cycles(values)

        if size == 1:
            attr_type = 'point'
        elif size > 1:
            attr_type = 'cyclic'
        elif size == 0:
            attr_type = 'unknown'
        else:        
            assert False        

        if attr_type == 'cyclic':
            cyc = values[idx : idx + size]
            head = sorted(cyc)[0]
            left = cyc[cyc.index(head) : len(cyc)]
            right = cyc[0 : cyc.index(head)]
            raw_attr = left + right 
            attr_id = fp(raw_attr)
            attr = [] 
        
            for state in raw_attr:
                fp_value = fp(state)
                attr.append(fp_value)
                seen[fp_value] = prettify(state, trajectory=False)
        else: # point
            raw_attr = values[-1]
            attr_id = fp(raw_attr)
            attr = attr_id
            seen[attr_id] = prettify(raw_attr, trajectory=False)
        
        if attr_id in res: 
            res[attr_id]['count'] += 1
        else: 
            res[attr_id] = {} 
            res[attr_id]['count'] = 1 
            res[attr_id]['type'] = attr_type
            res[attr_id]['value'] = attr
    
        res[attr_id]['ratio'] = float(res[attr_id]['count']) / float(samples)

        if debug: 
            if attr_type=='cyclic':
                has_trajectory=True
            else: 
                has_trajectory=False

            traj[i] = {
                'value': prettify(values, trajectory=True),
                'type': attr_type, 
                'attr': prettify(raw_attr, trajectory=has_trajectory)
                }

    result = {
        'attractors': res, 
        'state_key': seen, 
        'trajectory': traj, 
        'labels': ['State_AKT', 'State_AMPK', 'State_AMP_ATP', 'State_APC', 'State_ATM_ATR', 'State_AcidLactic', 'State_Apoptosis', 'State_BAD', 'State_BAX', 'State_Bak', 'State_Bcl_2', 'State_Bcl_XL', 'State_CHK1_2', 'State_COX412', 'State_Caspase8', 'State_Caspase9', 'State_CycA', 'State_CycB', 'State_CycD', 'State_CycE', 'State_Cytoc_APAF1', 'State_DNARepair', 'State_DnaDamage', 'State_Dsh', 'State_E2F', 'State_E2F_CyclinE', 'State_ERK', 'State_E_cadh', 'State_FADD', 'State_FOXO', 'State_FosJun', 'State_GFs', 'State_GSH', 'State_GSK_3', 'State_GSK_3_APC', 'State_Gli', 'State_Glut_1', 'State_HIF1', 'State_Hypoxia', 'State_IKK', 'State_JNK', 'State_LDHA', 'State_MXI1', 'State_Max', 'State_Mdm2', 'State_Miz_1', 'State_Mutagen', 'State_Myc', 'State_Myc_Max', 'State_NF1', 'State_NFkappaB', 'State_Nutrients', 'State_PDK1', 'State_PHDs', 'State_PI3K', 'State_PIP3', 'State_PKC', 'State_PTEN', 'State_RAF', 'State_RAGS', 'State_RHEB', 'State_ROS', 'State_RTK', 'State_Ras', 'State_Rb', 'State_Slug', 'State_Smad', 'State_SmadE2F', 'State_SmadMiz_1', 'State_Snail', 'State_TAK1', 'State_TCF', 'State_TGFbeta', 'State_TNFalpha', 'State_TSC1_TSC2', 'State_UbcH10', 'State_VEGF', 'State_VHL', 'State_WNT', 'State_beta_cat', 'State_cdc20', 'State_cdh1', 'State_cdh1_UbcH10', 'State_eEF2', 'State_eEF2K', 'State_hTERT', 'State_mTOR', 'State_p14', 'State_p15', 'State_p21', 'State_p27', 'State_p53', 'State_p53_Mdm2', 'State_p53_PTEN', 'State_p70', 'State_p90']
        }

    return result
