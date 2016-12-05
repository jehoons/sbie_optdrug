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
---- | ---- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- |
FHIT | Tumor suppressor gene | True | True
HSPA4 | UNKNOWN | False | False
REM1 | UNKNOWN | False | False
HIST1H4I | UNKNOWN | False | False
LIFR | UNKNOWN | False | False

* (d) TABLE.S1D.NUM_DRUG.csv
Number of data in therapy data. By each drug, count the number of total cell line data and the number of large intestine data. Then, find the target of each drug and compare the target with network.

* (e) TABLE.S1E.LOF_GOF_INDV.csv


* (f) LOF and GOF of complex node.xlsx