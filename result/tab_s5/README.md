### Patient-specific profiles (such as mutation and CNV) and drug effect information are converted as JSON format

### TABLE.S5A.COPYNUMVAR_data_s1.json

* (a) make json file of Copy number variation data

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

* 

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

* (b) make json file of Mutation data

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

* (b) make json file of Mutation data

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

* (c) make json file of Drug data

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

앞으로 만들 json file
```json
{
   "C2BBE1_LARGE_INTESTINE": {
        "mutations" = {
            "APC": {
                "function": "LOF", "intensity": 1.0
            }, 
            "CTNNB1": {
                "function": "GOF", "intensity": 1.0
            }
            "default_function": "LOF"
        }, 
        
        "copynumbers" = {
            "APC": {
                "function": "AMP", "copy_number": 10
            }, 
            "CTNNB1": {
                "function": "DEL", "copy_number": 2
            }
            "default_function": "LOF"
        }, 

        drugs = {
            "MEKi": {
                "type": "inhibitor", "dose": 1.0, "tau": 10, "target": "MEK"
            }, 
        },
    }
```

Patient-specific profiles (such as mutation and CNV) and drug effect information 
are converted as JSON format as following: 


### Table S5

