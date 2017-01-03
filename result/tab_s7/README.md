### Table S7. Scanning result for fumia network

#### A. Fumina network model (preprocessed)

#### B. Basin of attraction in test mode
어트랙터를 계산하기에 앞서, 적절한 입력조건을 설정할 필요가 있다. 예를 들어, `Mutagenic`, `GFs`, `Nutrients`, `TNF-alpha`, `Hypoxia` 노드들에 대해서 다음과 같이 설정을 하게 되면,

`Mutagenic` | `GFs` | `Nutrients` | `TNF-alpha` | `Hypoxia` |
---|---|---|---|---|
True|True|True|True|False|

가장 큰 크기를 가지는 *basin of attractor*가 얻어 진다.

#### C and D. Input combinations and simulation results
[download](http://gofile.me/3gpVt/QgRA45O0V)

### Methods
시뮬레이션 방법은 아래와 같다:
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
프로그램의 실행결과는 아래와 같다:

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
![image1]

#### E. Fumia regulation network (SIF)

#### F. Input combinations - APC mutation

#### G. Scanning result - with Table S7F.

[image1]: https://www.dropbox.com/s/9hc801ibul8q14v/2016-10-15%2017_12_43-%EC%82%AC%EC%A7%84.png?dl=1
