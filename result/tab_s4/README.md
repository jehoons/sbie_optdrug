### Table S4. Network-level functions of genetic alterations
뮤테이션이 반영된 네트워크를 시뮬레이션 하기 위해서는 어떤 뮤테이션이 유전자를 기능적으로 어떻게 바꾸는지 알아야 합니다. 우리는 처음에 [ONCOKB사이트](http://oncokb.org)에서 뮤테이션의 기능을 참고하려고 하였습니다. 하지만 이 웹사이트의 정책상 데이터를 수집하는 것을 금지하고 있기 때문에 데이터를 수집할 수 없었습니다. [Giordano, 2006](http://www.nature.com/onc/journal/v25/n38/full/1209721a.html)에 따르면, 튜머서프레서들은 로스오브펑션 뮤테이션에 의해서 비활성화가 되고 프로토-온코진들은 게인오브펑션 뮤테이션에 의해서 활성화가 됩니다. 따라서 우리는 온코진 뮤테이션은 GOF로 튜머서프레서의 뮤테이션은 LOF로 가정할 수 있습니다.

Gene | Type
--- | ---
APC | T
CTNNB1 | O
... | ...

여기서 T과 O는 각각 튜머서프레서진과 온코진입니다. 온코진과 튜머서프레서 유전자에 관한 정보는 LOF, GOF에 비해 정보량이 풍부한 편으로 보입니다. 우리는 [binfo](binfo.ncku.edu.tw)로부터 oncogene, Tumor suppressors에 대한 정보를 추출하였습니다.

[code](https://github.com/jehoons/sbie_optdrug/blob/master/scratch/binfo/test_binfo.py).

binfo 데이터베이스를 이용하는 방법은 아래와 같습니다.

```
http://www.binfo.ncku.edu.tw/cgi-bin/gf.pl?genename=APC
```

CCLE 데이터셋 중에서 유전자변이 데이터들을 동역학네트워크모델에 반영하기 위해서는 각 유전자변이들이 어떤 기능적변화를 야기하는지 알아야 한다. 우리는 유전자가 Oncogene인지 또는 Tumor Suppressor인지 여부를 공공데이터베이스(binfo)로부터 수집하였다 (**Table S4**). 예를 들어 APC유전자의 경우에는 아래와 같은 Web API 명령을 웹브라우저에 넣어줍으로써 해당 유전자에 대한 특징적인 정보들을 불러들일 수 있다.
```
http://www.binfo.ncku.edu.tw/cgi-bin/gf.pl?genename=APC
 ```

#### (**A**) List of gene names found in CCLE dataset

(Example rows)

ID |
---- |
FHIT |
HSPA4 |
REM1 |
HIST1H4I |
LIFR |

#### (**B**) List of raw HTML files collected from the database

(Not shown)

#### (**C**) List of Oncogenes and Tumor Suppressors

(Example rows)

ID | CATEGORY | GENE_FOUND | CONTENT_FOUND
---- | ---- | ---- | ----
FHIT | Tumor suppressor gene | True | True
HSPA4 | UNKNOWN | False | False
REM1 | UNKNOWN | False | False
HIST1H4I | UNKNOWN | False | False
LIFR | UNKNOWN | False | False

#### (**D**) Statistics of (**C**)

CATEGORY | CATEGORY
---- | ----
Oncogene | 140
Other | 51
Tumor suppressor gene | 67
UNKNOWN | 1380

![BarChart](https://github.com/jehoons/sbie_optdrug/blob/master/result/tab_s4/Table-S4D-Statistics.png)
