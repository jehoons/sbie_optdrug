## Results

### Table S1. Extracted data from therapy data and MUTCNA 

### Table S2. Extracted node names from logical network data

### Table S3. Translated model into logical functional form
`boolean2` 시뮬레이터 (또는 다른 일반적인 불린네트워크시뮬레이터)에서 네트워크를 시뮬레이션 하기 위해서는 로지컬펑션의 형태로 네트워크가 표현되어 있을 필요가 있다. 우리는 웨이트썸펑션의 형태로 주어진 네트워크 모델을 로지컬펑션의 형태로 전환하였다.

### Table S4. Oncogene and Tumor suppressors
[Giordano, 2006][giordano06]에 따르면, 튜머서프레서들은 로스오브펑션 뮤테이션에 의해서 비활성화가 되고 프로토-온코진들은 게인오브펑션 뮤테이션에 의해서 활성화가 된다. 그러므로 우리는 온코진 뮤테이션은 GOF로 튜머서프레서의 뮤테이션은 LOF로 가정한다.

### Table S5. Collecting Patient-specific data and chemical treatment data
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

## Materials and Methods
[BooleanNet Simulator][boolean2-sim] is used as simulation engine used in this research. Fumia Network is used as backbone network for this research. We used drug-dose response from CCLE and GDSC database.


[giordano06]: (http://www.nature.com/onc/journal/v25/n38/full/1209721a.html)

[boolean2-sim]: https://scfbm.biomedcentral.com/articles/10.1186/1751-0473-3-16