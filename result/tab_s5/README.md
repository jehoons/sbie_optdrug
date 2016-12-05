### Table.S5A.COPYNUMVAR_data 
Patient-specific profiles (such as mutation and CNV) and drug effect information 
are converted as JSON format as following: 

```json
mutations = {
    "list": {
        "APC": {
            "function": "LOF", "intensity": 1.0
        }, 
        "CTNNB1": {
            "function": "GOF", "intensity": 1.0
        }
    }, 
    "default_function": "LOF"
}

copynumbers = {
    "list": {
        "APC": {
            "function": "AMP", "copy_number": 10
        }, 
        "CTNNB1": {
            "function": "DEL", "copy_number": 2
        }
    }, 
    "default_function": "LOF"
}

drugs = {
    "list": {
        "MEKi": {
            "type": "inhibitor", "dose": 1.0, "tau": 10, "target": "MEK"
        }, 
    },
}
```

### Table S5
Patient-specific profiles (such as mutation and CNV) and drug effect information are converted as JSON format

* (a) make json file of Copy number variation data

* (b) make json file of Mutation data

* (c) make json file of Drug data
