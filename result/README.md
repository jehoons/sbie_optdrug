## Results

### Table S1. Extracted data from therapy data and MUTCNA 

### Table S2. Extracted node names from logical network data

### Table S3. Translated model into logical functional form

`boolean2` 시뮬레이터 (또는 다른 일반적인 boolean network simulator)에서 네트워크를 시뮬레이션 하기 위해서는 logical function의 형태로 네트워크가 표현되어 있을 필요가 있다. 우리는 logic minimization등의 테크닉을 이용하여 weighted sum function형태로 주어진 네트워크모델을 logical function의 형태로 전환하였다.

### Table S4. Oncogene and Tumor suppressors

뮤테이션이 반영된 네트워크를 시뮬레이션 하기 위해서는 어떤 뮤테이션이 유전자를 기능적으로 어떻게 바꾸는지 알아야 한다. 우리는 처음에 [ONCOKB사이트](http://oncokb.org)에서 뮤테이션의 기능을 참고하려고 하였다. 하지만 이 웹사이트의 정책상 데이터를 수집하는 것을 금지하고 있기 때문에 데이터를 수집할 수 없었다.

[Giordano, 2006](http://www.nature.com/onc/journal/v25/n38/full/1209721a.html)에 따르면, tumor suppressors들은 loss-of-function 뮤테이션에 의해서 비활성화가 되고 proto-oncogenes들은 gain-of-function 뮤테이션에 의해서 활성화가 된다. 그러므로 우리는 oncogene 뮤테이션은 GOF로 tumor suppressors 뮤테이션은 LOF로 가정한다. Among the list of gene oncogene and tumor suppressor gene are identified. 

Gene | Type
--- | --- 
APC | T
CTNNB1 | O
... | ... 

where T and O are tumor suppressor gene and oncogene, respectively.

oncogene, tumor suppressors에 관한 정보는 LOF, GOF에 비해서 상대적으로 정보의 량은 매우 풍부한 편이다. 우리는 [binfo](binfo.ncku.edu.tw)로부터 oncogene, Tumor suppressors에 대한 정보를 추출하였다[code](https://github.com/jehoons/sbie_optdrug/blob/master/scratch/binfo/test_binfo.py).

`binfo` 데이터베이스를 이용하는 방법
http://www.binfo.ncku.edu.tw/cgi-bin/gf.pl?genename=APC

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

[BooleanNet Simulator](https://scfbm.biomedcentral.com/articles/10.1186/1751-0473-3-16) is used as simulation engine used in this research. 

Fumia Network is used as backbone network for this research. 

We used drug-dose response from CCLE and GDSC database. 



