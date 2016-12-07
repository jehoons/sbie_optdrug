### Patient-specific profiles (such as mutation and CNV) and drug effect information are converted as JSON format

### TABLE.S5A.COPYNUMVAR_data_s1.json

* (a) copy number alteration 데이터를 cell line에 따라서 정리한 데이터를 json file로 정리했다. function 분류는 result/tab_s1에 (e)번 결과에 따라서 정리했다. 수정할 부분은 copy number alteration에 맞는 데이터를 채우는 것이다.

```json
{
   "C2BBE1_LARGE_INTESTINE": {
      "AMP": {
         "function": "GOFLOF", 
         "intensity": 0.5
      }, 
      "APC": {
         "function": "GOFLOF", 
         "intensity": 0.5
      }, 
      "ATM": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
      "ATP": {
         "function": "GOFLOF", 
         "intensity": 0.5
      }, 
      "BCL2": {
         "function": "GOFLOF", 
         "intensity": 0.5
      }, 
      "CDH1": {
         "function": "LOF", 
         "intensity": 0.5
      }, 
```

### TABLE.S5A.COPYNUMVAR_data_s4.json

* (a) copy number alteration 데이터를 cell line에 따라서 정리한 데이터를 json file로 정리했다. function 분류는 result/tab_s4의 결과에 따라서 정리했다. 수정할 부분은 copy number alteration에 맞는 데이터를 채우는 것이다.

```json
{
   "C2BBE1_LARGE_INTESTINE": {
      "AMP": {
         "function": "GOFLOF", 
         "intensity": 0.5
      }, 
      "APC": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
      "ATM": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
      "ATP": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
      "BCL2": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
```

### TABLE.S5B.MUTATION_data_s1.json

* (b) mutation 데이터를 cell line에 따라서 정리한 데이터를 json file로 정리했다. function 분류는 result/tab_s1에 (e)번 결과에 따라서 정리했다.

```json
{
   "C2BBE1_LARGE_INTESTINE": {
      "APC": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
      "P53": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
      "ROS": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
      "SMAD": {
         "function": "GOF", 
         "intensity": 0.5
      }
   }, 
   "CCK81_LARGE_INTESTINE": {
      "APC": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
      "MTOR": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
      "P53": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
```

### TABLE.S5B.MUTATION_data_s4.json

* (b) mutation 데이터를 cell line에 따라서 정리한 데이터를 json file로 정리했다. function 분류는 result/tab_s4의 결과에 따라서 정리했다.

```json
{
   "C2BBE1_LARGE_INTESTINE": {
      "APC": {
         "function": "LOF", 
         "intensity": 0.5
      }, 
      "P53": {
         "function": "LOF", 
         "intensity": 0.5
      }, 
      "ROS": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
      "SMAD": {
         "function": "LOF", 
         "intensity": 0.5
      }
   }, 
   "CCK81_LARGE_INTESTINE": {
      "APC": {
         "function": "LOF", 
         "intensity": 0.5
      }, 
      "MTOR": {
         "function": "GOF", 
         "intensity": 0.5
      }, 
```

### TABLE.S5C.DRUG_data.json

* (c) drug 데이터를 cell line에 따라서 정리한 데이터를 json file로 정리했다. 추가할 데이터는 '"dose": 1.0, "tau": 10' 이런 약물의 수치적인 데이터이다.

```json
{
   "C2BBE1_LARGE_INTESTINE": {
      "Nutlin-3": {
         "target": "MDM2", 
         "type": "inhibitor"
      }, 
      "PLX4720": {
         "target": "RAF", 
         "type": "inhibitor"
      }, 
      "RAF265": {
         "target": "RAF", 
         "type": "inhibitor"
      }, 
      "Sorafenib": {
         "target": "RTK", 
         "type": "inhibitor"
      }
   }, 
   "CCK81_LARGE_INTESTINE": {
      "Nutlin-3": {
         "target": "MDM2", 
         "type": "inhibitor"
      }, 
```

앞으로 데이터 추가해서 만들 json file 예시
```json
{
   "C2BBE1_LARGE_INTESTINE": {
        "mutations" : {
            "APC": {
                "function": "LOF", "intensity": 1.0
            }, 
            "CTNNB1": {
                "function": "GOF", "intensity": 1.0
            }
            "default_function" : "LOF"
        }, 
        
        "copynumbers" : {
            "APC": {
                "function": "AMP", "copy_number": 10
            }, 
            "CTNNB1": {
                "function": "DEL", "copy_number": 2
            }
            "default_function" : "LOF"
        }, 

        "drugs" : {
            "MEKi": {
                "type" : "inhibitor", "dose": 1.0, "tau": 10, "target": "MEK"
            }, 
        },
    }
   
```
