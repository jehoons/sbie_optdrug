목표: 유전자뮤테이션을 네트워크모델에 반영하기

방법 1. 유전자 뮤테이션이 네트워크 모델에 포함되는 경우에만 반영하기 

방법 2. 유전자 뮤테이션이 네트워크 모델에 포함되는 경우, 이를 근사하여 반영하기 
* string 데이터셋 확보하기 (N0)
* 유전자발현정도를 이용하여 N0로부터 네트워크의 부분집합 N1을 추출하기

참고사항: 
* Kumar, R.D., Searleman, A.C., Swamidass, S.J., Griffith, O.L., and Bose, R. (2015). Statistically identifying tumor suppressors and oncogenes from pan-cancer genome-sequencing data. Bioinformatics 31, 3561–3568.
* 아노바 - http://annovar.openbioinformatics.org/en/latest/

아노바는 MAF, VCF 포맷을 입력으로 받는다. filter-by-annotation? 도구를 사용.
출력으로는 5가지 알고리즘을 이용하여 FIS를 계산한다. FIS는 어떤 변이를 선택할지에 대한 기준을 준다. 
하지만, 여전히 그 유전자가 1로 고정되는지, 0으로 고정될지는 알지 못한다. 적절한가정을 하여 이를 해소하거나  Kumar의 방법을 이용할수 있을 것 같다. 