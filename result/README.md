## Results

### Table S1
* Data is extracted from therapy data and mutation-copy number variation data

### Table S2
* Node names are extracted from logical network data

### Table S3
* change the weighted sum function to logical function

### Table S4
Among the list of gene oncogene and tumor suppressor gene are identified. 

Gene | Type
--- | --- 
APC | T
CTNNB1 | O
... | ... 

where T and O are tumor suppressor gene and oncogene, respectively. 

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

### Ref. 
* TEX writing - http://www.hostmath.com/


