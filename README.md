## Finding optimal combination of cancer drugs

### Research goal
* Map patient (or cell line) profile into network
* Simulate personalized network
* Calculate attractor's landscape

### Requirements
프로젝트 코드를 실행하기 위해서는 다음과 같이 데이터셋 다운로드 및 패키지 설치를 하여야 합니다.

#### Dataset
프로젝트에서 필요한 데이터셋 [material.tar.gz](http://gofile.me/3gpVt/hE0oPs0Hv)를 다운로드합니다. 그 다음에는 다음 명령을 실행하여 데이터셋을 해당폴더에 위치시킵니다.
```
mv material.tar.gz sbie_optdrug/dataset
tar xvfz material.tar.gz
```

#### Package
프로젝트 코드를 실행하기 위해서는 `mytermutils`, `BooleanSim` 패키지를 설치하여야 합니다.
```
# install mytermutils
git clone git@github.com:jehoons/mytermutils.git
cd mytermutils
python setup.py install
cd ..
rm -rf mytermutils

# install BooleanSim
git clone git@github.com:jehoons/BooleanSim.git
cd BooleanSim
python setup.py install
cd ..
rm -rf BooleanSim

# install BooleanSim
pip install tqdm
```

### Update history

#### 2016. 9. 28
* LOF/GOF 추출 성공 - binfo로 부터 Oncogene, Tumor Suppressors 추출(**Table S4**)

#### 2016. 9. 3
* OncoKB에서 LOF, GOF에 관한 자료를 추출할수 있는 가능성 확인

#### 2016. 8. 29
* CCLE MUTCNA 테이블을 분석 후 이를 정리한 테이블 생성
* LOF/GOF 추출 1차시도 - 실패

#### 2016. 8. 26
* intersection ratio of network nodes to CCLE
* intersection ratio of network nodes to drug
* intersection ratio - 뮤테이션의 경우는 평균 20% 수준, CNV는 5%수준 임 - 너무 낮음
* 약물의 경우는 24개중에서 5개만이 타겟팅이 가능한 수준 - 너무 낮음
* LOF, GOF 식별 후 뮤테이션과 함께 네트워크에 반영하는 코드 작성
* cBioPortal에서 CCLE 데이터를 보면, OncoKB랑 연동되어 LOF와 GOF정보를 셀라인별로 확인가능

#### 2016. 8. 15
* CCLE에서 대장암관련 데이터를 추출하고 유전자프로화일을 반영하는 자동화 코드를 작성
* 약물타겟을 입력으로 주어서 시뮬레이션을 실행하는 방법
* Attractor analysis code 보완
