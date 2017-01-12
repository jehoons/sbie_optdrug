from os.path import dirname 

# dataset에는 .. 입력데이터 집합과, 출력데이터 집합을 불러들이도록 디자인하면 어떨지? 

dataset_dir = dirname(__file__)+'/dataset'

HALLMARK_APOPTOSIS = 'dataset/MSigDB/HALLMARK_APOPTOSIS.txt'
HALLMARK_E2F_TARGETS = 'dataset/MSigDB/HALLMARK_E2F_TARGETS.txt'
HALLMARK_G2M_CHECKPOINT = 'dataset/MSigDB/HALLMARK_G2M_CHECKPOINT.txt'
HALLMARK_MITOTIC_SPINDLE = 'dataset/MSigDB/HALLMARK_MITOTIC_SPINDLE.txt'
HALLMARK_MYC_TARGETS_V1 = 'dataset/MSigDB/HALLMARK_MYC_TARGETS_V1.txt'
HALLMARK_MYC_TARGETS_V2 = 'dataset/MSigDB/HALLMARK_MYC_TARGETS_V2.txt'
HALLMARK_P53_PATHWAY = 'dataset/MSigDB/HALLMARK_P53_PATHWAY.txt'

HALLMARK_APOPTOSIS = pd.read_csv(HALLMARK_APOPTOSIS, skiprows=[1])
HALLMARK_APOPTOSIS = HALLMARK_APOPTOSIS[['HALLMARK_APOPTOSIS']].values.tolist()

HALLMARK_E2F_TARGETS = pd.read_csv(HALLMARK_E2F_TARGETS, skiprows=[1])
HALLMARK_E2F_TARGETS = HALLMARK_E2F_TARGETS[['HALLMARK_E2F_TARGETS']].values.tolist()

HALLMARK_G2M_CHECKPOINT = pd.read_csv(HALLMARK_G2M_CHECKPOINT, skiprows=[1])
HALLMARK_G2M_CHECKPOINT = HALLMARK_G2M_CHECKPOINT[['HALLMARK_G2M_CHECKPOINT']].values.tolist()

HALLMARK_MITOTIC_SPINDLE = pd.read_csv(HALLMARK_MITOTIC_SPINDLE, skiprows=[1])
HALLMARK_MITOTIC_SPINDLE = HALLMARK_MITOTIC_SPINDLE[['HALLMARK_APOPTOSIS']].values.tolist()

HALLMARK_MYC_TARGETS_V1 = pd.read_csv(HALLMARK_MYC_TARGETS_V1, skiprows=[1])
HALLMARK_MYC_TARGETS_V1 = HALLMARK_MYC_TARGETS_V1[['HALLMARK_MYC_TARGETS_V1']].values.tolist()

HALLMARK_MYC_TARGETS_V2 = pd.read_csv(HALLMARK_MYC_TARGETS_V2, skiprows=[1])
HALLMARK_MYC_TARGETS_V2 = HALLMARK_MYC_TARGETS_V2[['HALLMARK_MYC_TARGETS_V2']].values.tolist()

HALLMARK_P53_PATHWAY = pd.read_csv(HALLMARK_P53_PATHWAY, skiprows=[1])
HALLMARK_P53_PATHWAY = HALLMARK_P53_PATHWAY[['HALLMARK_P53_PATHWAY']].values.tolist()

df_fumia = pd.read_csv(fumia_node_list, names=['fumia_node'])
HALLMARK_APOPTOSIS = HALLMARK_APOPTOSIS[['HALLMARK_APOPTOSIS']].values.tolist()
