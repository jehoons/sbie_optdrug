# Finding optimal combination of cancer drugs

## Research purpose

* Map patient (or cell line) profile into network 
* Simulate personalized network 
* Calculate attractor's landscape 

## Update history

### 2016. 9. 28
* binfo로 부터 Oncogene, Tumor Suppressors 추출(**Table S4**)

### 2016. 9. 3
* OncoKB에서 LOF, GOF에 관한 자료를 추출가능함. 특히, 다음과 같이 웹에서 뮤테이션기능에 관한 데이터를 얻어올수 있다는 것을 확인하였음 
```
http://oncokb.org/#/gene/PTEN
```

* python bs4 를 활용하여 데이터를 추출할 계획 

### 2016. 8. 29
* LOF, GOF를 대량으로 처리하는 방법을 찾지 못함 
* CCLE MUTCNA 테이블을 분석 후 이를 정리한 테이블 생성 (컬럼 - cell-line, gene, mutation type, function, 등)

### 2016. 8. 26
* intersection ratio of network nodes to CCLE 
* intersection ratio of network nodes to drug 
* intersection ratio - 뮤테이션의 경우는 평균 20% 수준, CNV는 5%수준 임 - 너무 낮음
* 약물의 경우는 24개중에서 5개만이 타겟팅이 가능한 수준 - 너무 낮음
* 예상방법 - PPI(STRING)네트워크를 이용해서, CCLE노드와 Fumia노드 간의 거리정보를 이용해서 근사적으로 약물 또는 뮤테이션의 영향이 얼마일지를 추정하는 것이 가능할 것으로 생각됨
* LOF, GOF 식별 후 뮤테이션과 함께 네트워크에 반영하는 코드 작성
* cBioPortal에서 CCLE 데이터를 보시면 OncoKB랑 연동되어 LOF와 GOF정보를 셀라인별로 알 수 있음

### 2016. 8. 15
* CCLE에서 대장암관련 데이터를 추출하고 유전자프로화일을 반영하는 자동화 코드를 작성
* 약물타겟을 입력으로 주어서 시뮬레이션을 실행하는 방법
* Attractor analysis code 보완 
