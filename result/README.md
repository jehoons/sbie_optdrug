## Results

### Table S1
* ... 

### Table S2
* ... 

### Table S3
* ... 

### Table S4
Among the list of gene oncogene and tumor suppressor gene are identified. 

### Table S5
Patient-specific profiles (such as mutation and CNV) and drug effect information are converted as JSON format as following: 

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
	    	"function": "DEL", "intensity": 2
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

### Ref. 
* TEX writing - http://www.hostmath.com/


