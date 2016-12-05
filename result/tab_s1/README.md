### Table S1
Therapy data와 mutation-copy number variation data로부터 데이터를 추출함

* (a) TABLE.S1A.MUTCNA_CRC_NET.csv
mutation-copy number variation data에서 추출된 데이터로 cell line이 large intestine과 관련이 있고, network의 node와 gene name이 일치하는 경우의 데이터들만 모았다. 특히 gene name의 경우에는 단순히 node 이름과 겹친다고 그 node를 의미하지 않기 때문에 검색 결과를 이용해서 더 세세하게 분류를 했다.
gene name 검색한 site : (http://www.genenames.org/)

* (b) TABLE.S1B.THERAPY_CRC_NET.csv
Therapy data로부터 cell line이 large intestine과 일치하고, drug의 target이 network의 node와 겹치는 데이터를 분류했다.

* (c) TABLE.S1C.NUM_MUTCNA.csv
mutation-copy number variation data에서 gene name이 network의 node와 이름이 겹치는 경우의 데이터의 수를 cell line에 따라서 세었다. 단순 gene name 수는 아니고 값이 1인 즉, 켜져있는 mutation 수를 data의 종류(mutation, copy number alteration of amplification, copy number alteration of delete)에 따라서 세었다.

CCLE cell line | CCLE mutation의 수 | CCLE CNV AMP의 수 | CCLE CNV DEL의 수 | Network mutation | Network CNV AMP | Network CNV DEL | Ratio of Mut | Ratio of CNV AMP | Ratio of CNV DEL
---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
SW1116_Large_Intestine | 32 | 621 | 678 | 5 | 8 | 10 | 15.625 | 1.288245 | 1.474926
COLO205_Large_Intestine | 20 | 623 | 170 | 4 | 15 | 1 | 20 | 2.407705 | 0.588235
OUMS23_Large_Intestine | 36 | 455 | 927 | 8 | 11 | 12 | 22.22222 | 2.417582 | 1.294498

* (d) TABLE.S1D.NUM_DRUG.csv
Therapy data에서 약물에 따라서 cell line이 large intestine인 데이터의 개수를 세었다. 그리고 drug target이 node와 겹치면 Target in Network에 노드이름을 써주었다.

Drug | Target | Total Cell line number | Number of Large intsetine | Target in Network 
---- | ---- | ---- | ---- | ---- |
AEW541 | IGF1R | 503 | 23 | X 
Nilotinib | ABL | 420 | 20 | X 
Nutlin-3 | MDM2 | 504 | 23 | MDM2 

* (e) TABLE.S1E.LOF_GOF_INDV.csv
(a)에서 검색한 gene name들을 기준으로 gene name이 node를 gain(더 만들도록 하는 작용)하도록 하는지, loss(덜 만들도록 하는 작용)하도록 하는지 판단하여 loss나 gain으로 적어둔 파일이다.

Description | Loss or Gain 
---- | ---- |
TGFB1_MUT | Gain 
TGFB2_MUT | Gain 
TGFB3_MUT | Gain 

* (f) LOF and GOF of complex node.xlsx
GSK/APC와 같이 두 node에 의해서 영향을 받는 node의 Gain of function과 Loss of function을 결정할 때 여러 case들을 분류해 놓은 표이다.

GSK3 | APC | GSK3/APC 
---- | ---- | ---- |
LOF | X | LOF 
GOF | X | GOF 
X | LOF | LOF 