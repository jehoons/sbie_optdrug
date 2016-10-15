여기서는 새로 개발한 attr_cy 모듈을 이용한다. 사용하는 방법은 아래와 같다. 여기서, 테스트에 이용하는 모델은 `fA = A or C`, `fB = A and C`, `fC = not A or B`를 이용하였다. 이모델의 상태천이 다이어그램은 아래 같다.

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

### Table S7. Scanning of fumia network
![draft_v1][draft_v1]
이것이 현재의 결과이다. 뚜렷한 결과가 보이지 않는 이유는 입력조건을 설정하지 않았기 때문일 것으로 생각된다. 

[draft_v1]: https://www.dropbox.com/s/bqk2zyshqpdjsn3/2016-10-15-1822-TABLE.S7B.ATTRACTORS.png?dl=1

[image1]: https://www.dropbox.com/s/9yeovfo31ftfxz0/2016-10-15%2017_12_43-%EC%82%AC%EC%A7%84.png?dl=1
