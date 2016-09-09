from os.path import exists
from sbie_optdrug.result.tab_s2 import program


def test():
    
    config = program.getconfig()

    if not exists(config['output']):        
        program.run(config)


