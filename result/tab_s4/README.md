CCLE 데이터셋 중에서 유전자변이 데이터들을 동역학네트워크모델에 반영하기 위해서는 각 유전자변이들이 어떤 기능적변화를 야기하는지 알아야 한다. 우리는 유전자가 **Oncogene**인지 또는 **Tumor Suppressor**인지 여부를 공공데이터베이스(binfo)로부터 수집하였다 (**Table S4**). 예를 들어 APC유전자의 경우에는 아래와 같은 Web API 명령을 웹브라우저에 넣어줍으로써 해당 유전자에 대한 특징적인 정보들을 불러들일 수 있다. 
```
http://www.binfo.ncku.edu.tw/cgi-bin/gf.pl?genename=APC
 ```


### Table S4A. List of gene names found in CCLE dataset

(Example rows)

ID |
---- | 
FHIT |
HSPA4 |
REM1 |
HIST1H4I |
LIFR | 

### Table S4B. List of raw HTML files collected from the database

(Not shown)

### Table S4C. List of Oncogenes and Tumor Suppressors

(Example rows)

ID | CATEGORY | GENE_FOUND | CONTENT_FOUND
---- | ---- | ---- | ----
FHIT | Tumor suppressor gene | True | True
HSPA4 | UNKNOWN | False | False
REM1 | UNKNOWN | False | False
HIST1H4I | UNKNOWN | False | False
LIFR | UNKNOWN | False | False

### Table S4D. Statistics of Table S4C

CATEGORY | CATEGORY
---- | ----
Oncogene | 140
Other | 51
Tumor suppressor gene | 67
UNKNOWN | 1380

### Table S4D. Char for Table S4D 

![BarChart](https://github.com/jehoons/sbie_optdrug/blob/master/result/tab_s4/TABLE_S4D_STATISTICS.JPG)


