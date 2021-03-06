### Table S1. CCLE data is processed to analyze fumia network
#### (**A**) Cell line, mutation, and CNV dataset are preprocessed.
CCLE데이터셋의 Mutation과 CNV로부터 대장암관련 세포주를 추출하였고, fumia 네트워크의 노드와 관련이 있는 유전자이름 선택하였습니다. 특히 유전자이름의 경우에는 노드이름과 겹친다고해서 반드시 그 노드를 의미하는 것은 아니었기 때문에, 검색결과를 또한 반영하였습니다. 유전자이름을 검색하는데 활용한 데이터베이스는 [genenames.org](http://www.genenames.org/)입니다.

#### (**B**) Drug dose response dataset is preprocessed.
CCLE데이터셋의 dose response (therapy dataset) 테이블에서 세포주가 large intestine이고 drug의 target이 network의 node와 겹치는 경우의 record들을 필터링하였습니다.

#### (**C**) Molecular profile coverage
Mutation, CNV 데이터에서 유전자이름이 네트워크의 노드와 이름이 겹치는 경우의 데이터의 수를 세포주에 따라서 카운트하였습니다. 단순히 유전자이름의 수는 아니지만, 해당 노드의 값이 1인 경우, 즉 켜져 있는 mutation 수를 data의 종류(mutation, copy number alteration of amplification, copy number alteration of delete)에 따라서 카운트 한 것입니다.

CCLE cell line | CCLE mutation의 수 | CCLE CNV AMP의 수 | CCLE CNV DEL의 수 | Network mutation | Network CNV AMP | Network CNV DEL | Ratio of Mut | Ratio of CNV AMP | Ratio of CNV DEL
---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
SW1116_Large_Intestine | 32 | 621 | 678 | 5 | 8 | 10 | 15.625 | 1.288245 | 1.474926
COLO205_Large_Intestine | 20 | 623 | 170 | 4 | 15 | 1 | 20 | 2.407705 | 0.588235
OUMS23_Large_Intestine | 36 | 455 | 927 | 8 | 11 | 12 | 22.22222 | 2.417582 | 1.294498

#### (**D**) Drug converage
Therapy 데이터셋에서 약물과 관련이 있는 샘플의 갯수와 fumia network에서 몇개나 관련이 있는지를 조사하였습니다.

Drug | Target | Total Cell line number | Number of Large intsetine | Target in Network
---- | ---- | ---- | ---- | ---- |
AEW541 | IGF1R | 503 | 23 | X
Nilotinib | ABL | 420 | 20 | X
Nutlin-3 | MDM2 | 504 | 23 | MDM2

#### (**E**) Table of LOF and GOF
(**A**)에서 검색한 유전자 이름들을 기준으로 유전자 이름이 노드를 gain(더 만들도록 하는 작용)하도록 하는지, loss(덜 만들도록 하는 작용)하도록 하는지 판단하여 loss나 gain으로 기록하였습니다.

Description | Loss or Gain
---- | ---- |
TGFB1_MUT | Gain
TGFB2_MUT | Gain
TGFB3_MUT | Gain

#### (**F**) Rule table for LOF and GOF
GSK/APC와 같이 두 node에 의해서 영향을 받는 node가 존재할수 있습니다. 이러한 모호한 경우에는 어떻게 LOF, GOF를 정해야 할까요? 이 테이블에서는 GOF, LOF를 결정할때 여러 경우들을 아래와 같이 분류하였습니다.

GSK3 | APC | GSK3/APC
---- | ---- | ---- |
LOF | X | LOF
GOF | X | GOF
X | LOF | LOF
