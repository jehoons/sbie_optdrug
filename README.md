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
