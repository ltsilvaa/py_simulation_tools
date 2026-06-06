"""

"""

def siesta():
    import siesta.utils.replace as r
    import siesta.utils.change as c
    c.chage_input_cell_optmization_type()
    r.replace_input_vectors()    

def qe():
    import qe.utils.replace as r
    import qe.utils.change as c
    c.chage_input_cell_optmization_type()
    r.replace_input_vectors()  

def onetep():
    ...

def castep():
    ...

def build_deformation_input(R: list, run_type: str, run_path: str):
    """
    """
    if run_type == 'siesta':
        siesta()
    elif run_type == 'qe':
        qe()
    elif run_type == 'onetep':
        onetep()
    elif run_type == 'castep':
        castep()



