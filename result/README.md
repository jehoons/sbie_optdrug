## Results

### [Table S1. Extracted data from therapy data and MUTCNA][tab_s1]

### [Table S2. Extracted node names from logical network data][tab_s2]

### [Table S3. Translated model into logical functional form][tab_s3]
`boolean2` 시뮬레이터 (또는 다른 일반적인 불린네트워크시뮬레이터)에서 네트워크를 시뮬레이션 하기 위해서는 로지컬펑션의 형태로 네트워크가 표현되어 있을 필요가 있다. 우리는 웨이트썸펑션의 형태로 주어진 네트워크 모델을 로지컬펑션의 형태로 전환하였다.

### [Table S4. Oncogene and Tumor suppressors][tab_s4]
[Giordano, 2006][giordano06]에 따르면, 튜머서프레서들은 로스오브펑션 뮤테이션에 의해서 비활성화가 되고 프로토-온코진들은 게인오브펑션 뮤테이션에 의해서 활성화가 된다. 그러므로 우리는 온코진 뮤테이션은 GOF로 튜머서프레서의 뮤테이션은 LOF로 가정한다.

### [Table S5. Collecting Patient-specific data and chemical treatment data][tab_s5]
뮤테이션 진익스프레션 등과 같은 환자특이적 프로화일들을 수집하고 시뮬레이션에 용이한 형태로 정리하였다.

### [Table S6. Regression analysis][tab_s6]

### [Table S7. Scanning of Fumia network][tab_s7]
Fumia네트워크의 모든 입력, 드럭타겟의 조합에 대해서 그 어트랙터베이신을 구한다.

## Materials and Methods
[BooleanNet Simulator][boolean2-sim] is used as simulation engine used in this research. Fumia Network is used as backbone network for this research. We used drug-dose response from CCLE and GDSC database.

[giordano06]: http://www.nature.com/onc/journal/v25/n38/full/1209721a.html
[boolean2-sim]: https://scfbm.biomedcentral.com/articles/10.1186/1751-0473-3-16
[tab_s1]: https://github.com/jehoons/sbie_optdrug/blob/master/result/tab_s1
[tab_s2]: https://github.com/jehoons/sbie_optdrug/blob/master/result/tab_s2
[tab_s3]: https://github.com/jehoons/sbie_optdrug/blob/master/result/tab_s3
[tab_s4]: https://github.com/jehoons/sbie_optdrug/blob/master/result/tab_s4
[tab_s5]: https://github.com/jehoons/sbie_optdrug/blob/master/result/tab_s5
[tab_s6]: https://github.com/jehoons/sbie_optdrug/blob/master/result/tab_s6
[tab_s7]: https://github.com/jehoons/sbie_optdrug/blob/master/result/tab_s7


