# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import re 
from sbie_optdrug.preproc import rule2logic

""" The original fumia_network curated version """

fumia_network_data = """
S_TGFbeta(t+1)=sgn_th(S_HIF1(t));
% S_TGFbeta(t+1)=0;   % tumor suppressor gene
S_DnaDamage(t+1)=sgn_th(S_Mutagen(t)+S_ROS(t));
S_p53_Mdm2(t+1)=sgn_th(S_p53(t)+S_Mdm2(t)-1);
S_AMP_ATP(t+1)=sgn_th(-S_Nutrients(t)+1);
S_NF1(t+1)=sgn_th(-S_PKC(t)+1);
S_PKC(t+1)=sgn_th(S_RTK(t)+S_WNT(t));
S_RTK(t+1)=sgn_th(S_GFs(t));
% S_RTK(t+1)=1;    % oncogene   % RTK:EGFR
S_RAGS(t+1)=sgn_th(S_Nutrients(t)-S_Hypoxia(t));
S_Ras(t+1)=sgn_th(-S_NF1(t)+S_RTK(t)+1);
% S_Ras(t+1)=1;   % oncogene
S_PI3K(t+1)=sgn_th(S_Ras(t)+S_hTERT(t));
% S_PI3K(t+1)=1;   % oncogene
S_PTEN(t+1)=1;
% S_PTEN(t+1)=0;     % tumor suppressor gene
S_PIP3(t+1)=sgn_th(S_PI3K(t)-S_PTEN(t)-S_p53_PTEN(t)+1);
S_PDK1(t+1)=sgn_th(S_PIP3(t)+S_HIF1(t)+S_Myc_Max(t));
S_IKK(t+1)=sgn_th(S_PKC(t)+S_AKT(t)+S_mTOR(t)-S_PHDs(t)-S_p53(t)+S_TAK1(t));
S_NF_kB(t+1)=sgn_th(S_PIP3(t)+2*S_IKK(t)-S_E_cadh(t)+S_Snail(t)-1);
S_RAF(t+1)=sgn_th(S_PKC(t)+S_Ras(t));
% S_RAF(t+1)=1;     % oncogene
S_ERK(t+1)=sgn_th(S_RAF(t));
% S_ERK(t+1)=1;    % proto-oncogene
S_p90(t+1)=sgn_th(S_PDK1(t)+S_ERK(t));
S_AKT(t+1)=sgn_th(S_PIP3(t)+S_PDK1(t)-1);
% S_AKT(t+1)=1;    % oncogene
S_WNT(t+1)=sgn_th(-S_p53(t)+S_Gli(t));
S_Dsh(t+1)=sgn_th(S_WNT(t));
S_APC(t+1)=sgn_th(S_PTEN(t)+1);
% S_APC(t+1)=0;     % tumor suppressor gene
S_GSK_3(t+1)=sgn_th(-S_p90(t)-S_AKT(t)-S_Dsh(t)-S_mTOR(t)+3);
S_GSK_3_APC(t+1)=sgn_th(S_APC(t)+S_GSK_3(t)-1);
S_beta_cat(t+1)=sgn_th(-S_GSK_3_APC(t)-S_p53(t)+1);
% S_beta_cat(t+1)=1;         % proto-oncogene
S_Slug(t+1)=sgn_th(-S_p53_Mdm2(t)+S_NF_kB(t)+S_TCF(t));
S_mTOR(t+1)=sgn_th(S_RAGS(t)+S_AKT(t)+S_RHEB(t)-S_AMPK(t)-1);
% S_mTOR(t+1)=1;       % proto-oncogene
S_HIF1(t+1)=sgn_th(S_Hypoxia(t)+S_mTOR(t)-2*S_VHL(t)-S_PHDs(t)+S_Myc_Max(t)-S_p53(t)-S_FOXO(t)+2);
S_COX412(t+1)=sgn_th(S_HIF1(t));
S_VHL(t+1)=sgn_th(-S_Hypoxia(t)-S_ROS(t)+1);
S_PHDs(t+1)=sgn_th(-S_Hypoxia(t)+S_ROS(t)+1);
S_Myc_Max(t+1)=sgn_th(-S_TGFbeta(t)+S_Myc(t)+S_Max(t)-S_MXI1(t)-S_SmadE2F(t)-1);
S_Myc(t+1)=sgn_th(S_NF_kB(t)+S_ERK(t)-S_HIF1(t)+S_E2F(t)+S_FosJun(t)+S_TCF(t)+S_Gli(t)-1);
% S_Myc(t+1)=1;    % proto-oncogene
S_Max(t+1)=1;
S_MXI1(t+1)=sgn_th(S_HIF1(t));
S_TSC1_TSC2(t+1)=sgn_th(-S_RAF(t)-S_ERK(t)-S_p90(t)-S_AKT(t)+S_HIF1(t)+S_p53(t)+S_AMPK(t)+1);
S_RHEB(t+1)=sgn_th(-S_TSC1_TSC2(t)+1);
S_p53(t+1)=sgn_th(S_HIF1(t)-S_Bcl_2(t)-S_Mdm2(t)+S_CHK1_2(t)+1);
% S_p53(t+1)=0;    % tumor suppressor gene
S_Bcl_2(t+1)=sgn_th(2*S_NF_kB(t)-S_p53(t)-S_BAX(t)-S_BAD(t));
% S_Bcl_2(t+1)=1;     % oncogene
S_BAX(t+1)=sgn_th(-S_HIF1(t)+S_p53(t)-S_Bcl_2(t)+S_JNK(t));
% S_BAX(t+1)=0;     % tumor suppressor gene
S_BAD(t+1)=sgn_th(-S_RAF(t)-S_p90(t)-S_AKT(t)-S_HIF1(t)+1);
% S_BAD(t+1)=0;     % pro-apoptotic protein (apoptosis¸¦ ÃËÁø½ÃÅ°´Â ´Ü¹éÁú)
S_Bcl_XL(t+1)=sgn_th(-S_p53(t)-S_BAD(t)+1);
S_Rb(t+1)=sgn_th(-S_CycA(t)-S_CycB(t)-S_CycD(t)-S_CycE(t)-S_Mdm2(t)+2);
% S_Rb(t+1)=0;        % tumor suppressor gene
S_E2F(t+1)=sgn_th((-2)*S_Rb(t)-S_CycA(t)-S_CycB(t)+S_E2F(t)+1);
S_p14(t+1)=sgn_th(S_Ras(t)+S_Myc_Max(t)+S_E2F(t)-3);
S_CycA(t+1)=sgn_th(S_CycA(t)-S_Rb(t)-S_cdc20(t)-S_p27(t)-S_p21(t)+S_E2F_CyclinE(t)+S_cdh1_UbcH10(t));
S_CycB(t+1)=sgn_th(-S_p53(t)-S_cdh1(t)-S_cdc20(t)-S_p27(t)-S_p21(t)+1);
S_CycD(t+1)=sgn_th(S_NF_kB(t)+(-2)*S_GSK_3(t)+S_Myc_Max(t)-S_p27(t)-S_p21(t)-S_p15(t)-S_FOXO(t)+S_FosJun(t)+S_TCF(t)+S_Gli(t));
% S_CycD(t+1)=1;   % oncogene
S_CycE(t+1)=sgn_th(-S_Rb(t)+S_E2F(t)-S_CycA(t)-S_p27(t)-S_p21(t));
S_cdh1(t+1)=sgn_th(-S_CycA(t)-S_CycB(t)+S_cdc20(t)+1); 
% S_cdh1(t+1)=0;     % tumor suppressor gene   --> mutation
S_cdc20(t+1)=sgn_th(S_CycB(t)-S_cdh1(t));
S_UbcH10(t+1)=sgn_th(S_CycA(t)+S_CycB(t)-S_cdh1(t)+S_cdc20(t)+S_UbcH10(t));
S_p27(t+1)=sgn_th(-S_AKT(t)+S_HIF1(t)-S_Myc_Max(t)-S_CycA(t)-S_CycB(t)-S_CycD(t)+S_SmadMiz_1(t)+1);
S_p21(t+1)=sgn_th(-S_AKT(t)+S_HIF1(t)-S_Myc_Max(t)+S_p53(t)+S_SmadMiz_1(t)-S_hTERT(t)+1);
S_Mdm2(t+1)=sgn_th(S_AKT(t)+S_p53(t)-S_p14(t)-S_ATM_ATR(t)+1);
% S_Mdm2(t+1)=1;     % oncogene
S_Smad(t+1)=sgn_th(S_TNFalpha(t)+S_TGFbeta(t));
% S_Smad(t+1)=0;    % tumor suppressor gene
S_SmadMiz_1(t+1)=sgn_th(S_Smad(t)+S_Miz_1(t)-1);
S_SmadE2F(t+1)=sgn_th(S_Smad(t));
S_p15(t+1)=sgn_th(S_SmadMiz_1(t)+S_Miz_1(t));
S_FADD(t+1)=sgn_th(S_TNFalpha(t));
S_Caspase8(t+1)=sgn_th(S_FADD(t));
% S_Caspase8(t+1)=0;    % pro-apoptotic protein (apoptosis¸¦ ÃËÁø½ÃÅ°´Â ´Ü¹éÁú)
S_Bak(t+1)=sgn_th(S_Caspase8(t));
S_JNK(t+1)=sgn_th(S_TGFbeta(t));
S_FOXO(t+1)=sgn_th(-S_AKT(t)+2);
S_FosJun(t+1)=sgn_th(S_ERK(t)+S_JNK(t));
S_ROS(t+1)=sgn_th(-S_COX412(t)-S_GSH(t));
S_AMPK(t+1)=sgn_th(-S_GFs(t)+S_AMP_ATP(t)+S_HIF1(t)+S_ATM_ATR(t)+1);
S_Cytoc_APAF1(t+1)=sgn_th(-S_AKT(t)+S_p53(t)-S_Bcl_2(t)+S_BAX(t)-S_Bcl_XL(t)+S_Caspase8(t)+S_Bak(t));
S_Caspase9(t+1)=sgn_th(S_Cytoc_APAF1(t));
% S_Caspase9(t+1)=0;    % pro-apoptotic protein (apoptosis¸¦ ÃËÁø½ÃÅ°´Â ´Ü¹éÁú)
S_Apoptosis(t+1)=sgn_th(S_Caspase8(t)+S_Caspase9(t));
S_E_cadh(t+1)=sgn_th(-S_NF_kB(t)-S_Slug(t)-S_Snail(t)+3);                    
% S_E_cadh(t+1)=0;      % tumor suppressor gene   --> mutation¿¡¼­ Á¦¿Ü½ÃÅ´
S_Glut_1(t+1)=sgn_th(S_AKT(t)+S_HIF1(t)+S_Myc_Max(t)-1);
S_hTERT(t+1)=sgn_th(S_NF1(t)+S_NF_kB(t)+S_AKT(t)+S_HIF1(t)+S_Myc_Max(t)-S_p53(t)-S_SmadMiz_1(t)-S_eEF2(t)-4);
S_VEGF(t+1)=sgn_th(S_HIF1(t)+S_Myc_Max(t));
S_E2F_CyclinE(t+1)=sgn_th(S_E2F(t)+S_CycE(t)-1);
S_cdh1_UbcH10(t+1)=sgn_th(S_cdh1(t)+S_UbcH10(t)-1);
S_TAK1(t+1)=sgn_th(S_TNFalpha(t));
S_GSH(t+1)=sgn_th(S_NF_kB(t)+S_Myc_Max(t)+S_p21(t));
S_TCF(t+1)=sgn_th(S_beta_cat(t)-S_TAK1(t));
% S_TCF(t+1)=0;    % tumor suppressor gene
S_Miz_1(t+1)=sgn_th(-S_Myc_Max(t)+1);
S_p70(t+1)=sgn_th(S_PDK1(t)+S_mTOR(t));
S_ATM_ATR(t+1)=sgn_th(S_DnaDamage(t));
S_CHK1_2(t+1)=sgn_th(S_ATM_ATR(t));
S_DNARepair(t+1)=sgn_th(S_ATM_ATR(t));
S_eEF2K(t+1)=sgn_th(S_p90(t)+S_p70(t));
S_eEF2(t+1)=sgn_th(-S_eEF2K(t)+1);
S_p53_PTEN(t+1)=sgn_th(S_PTEN(t)+S_p53(t)-1);
S_LDHA(t+1)=sgn_th(S_HIF1(t)+S_Myc_Max(t)-1);
S_AcidLactic(t+1)=sgn_th(S_LDHA(t));
S_Snail(t+1)=sgn_th(S_NF_kB(t)-S_GSK_3(t)-S_p53(t)+S_Smad(t)-1);
"""


def get_txtdata():
    
    return fumia_network_data


def to_logic(short=False):

    txtdata = re.sub('%.*\n', '\n', get_txtdata())
    txtdata = re.sub('[ ;]', '', txtdata)
    txtdata = txtdata.replace('(t)', '')
    txtdata = txtdata.replace('(t+1)', '')

    return rule2logic.run(txtdata, short=short)

