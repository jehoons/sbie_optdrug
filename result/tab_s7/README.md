### Table S7. Scanning of fumia network

#### Table S7A. Fumina network model (preprocessed)

#### Table S7B. Basin of attraction in test mode
주의 - 어트랙터를 계산하기에 앞서, 적절한 입력조건이 설정되어야 함

예를 들어, `Mutagenic`, `GFs`, `Nutrients`, `TNF-alpha`, `Hypoxia` 노드들에 대해서 다음과 같이 설정을 하게 되면,

`Mutagenic` | `GFs` | `Nutrients` | `TNF-alpha` | `Hypoxia` |
---|---|---|---|---|
True|True|True|True|False|

dominent한 크기를 가지는 *basin of attractor*를 얻을 수 있었다. 아래 그래프에서는 (모든 입력조건을 0으로 두었을때) basin of attraction 분포를 도시하였다. 특별히 큰 크기를 가지는 basin of attraction이 없다는 것을 알 수 있다.

![draft_v1][draft_v1]

#### Table S7C,D Input combinations and simulation results
[download](http://gofile.me/3gpVt/QgRA45O0V)

### Methods
여기서의 분석은 새로 개발한 attr_cy 모듈을 이용하며, 사용하는 방법은 아래와 같다. 테스트에 이용된 모델은 `fA = A or C`, `fB = A and C`, `fC = not A or B`를 이용하였다. 이모델의 상태천이 다이어그램은 아래 같다.

![image1][image1]

아래의 코드를 실행보고 그 결과가 위의 그림에서 보인 상태천이 다이어그램과 같은 결과를 보이는지 확인해 보자.
```python
from boolean3_addon import attr_cy
import json

def test_hello(with_small, force):
    text='''
    A=Random
    B=Random
    C=Random
    A*= A or C
    B*= A and C
    C*= not A or B
    '''
    attr_cy.build(text)
    res = attr_cy.run(samples=100, steps=30, debug=False)
    json.dump(res, open('output.json', 'w'), indent=4)
```

프로그램의 실행결과는 아래와 같다. 얻어진 어트렉터의 베이신에 관한 정보가 위의 그림과 같다는 것을 알 수 있다.

```json
{
    "trajectory": {},
    "labels": [
        "A",
        "B",
        "C"
    ],
    "attractors": {
        "7eaed65c90": {
            "value": [
                "4ae1123067",
                "ce58123727"
            ],
            "ratio": 0.75,
            "count": 75,
            "type": "cyclic"
        },
        "86f1027545": {
            "value": "86f1027545",
            "ratio": 0.13,
            "count": 13,
            "type": "point"
        },
        "904154d19e": {
            "value": "904154d19e",
            "ratio": 0.12,
            "count": 12,
            "type": "point"
        }
    },
    "state_key": {
        "4ae1123067": "101",
        "ce58123727": "110",
        "86f1027545": "111",
        "904154d19e": "100"
    }
}
```

[image1]: https://www.dropbox.com/s/9yeovfo31ftfxz0/2016-10-15%2017_12_43-%EC%82%AC%EC%A7%84.png?dl=1

[draft_v1]: https://github.com/jehoons/sbie_optdrug/blob/master/result/tab_s7/TABLE_S7B_ATTRACTORS.png
