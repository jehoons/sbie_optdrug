## Results

### Table S1

* Data is extracted from therapy data and mutation-copy number variation data

### Table S2

* Node names are extracted from logical network data

### Table S3

* change the weighted sum function to logical function

### Table S4

뮤테이션이 반영된 네트워크를 시뮬레이션 하기 위해서는 어떤 뮤테이션이 유전자를 기능적으로 어떻게 바꾸는지 알아야 한다. 우리는 처음에 [oncokb](oncokb.org) 뮤테이션의 기능을 참고하려고 하였지만, 해당 웹사이트의 정책상 데이터를 수집하는 것을 금지하고 있기 때문에 데이터를 수집할 수 없었다. 

[Giordano, 2006](http://www.nature.com/onc/journal/v25/n38/full/1209721a.html)에 따르면, tumor suppressors들은 loss-of-function 뮤테이션에 의해서 비활성화가 되고 proto-oncogenes들은 gain-of-function 뮤테이션에 의해서 활성화가 된다. 그러므로 우리는 oncogene 뮤테이션은 GOF로 tumor suppressors 뮤테이션은 LOF로 가정한다. Among the list of gene oncogene and tumor suppressor gene are identified. 

Gene | Type
--- | --- 
APC | T
CTNNB1 | O
... | ... 

where T and O are tumor suppressor gene and oncogene, respectively.

### Table S5

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


