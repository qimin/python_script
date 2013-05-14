__author__ = 'Qimin'

from pymatgen.matproj.rest import MPRester
from pymatgen.io.vaspio_set import MPVaspInputSet, DictVaspInputSet
from pymatgen.io.vaspio.vasp_input import Kpoints,Incar
from pymatgen.io.vaspio.vasp_output import Outcar, Vasprun
import os

if __name__ == '__main__':
    mpr = MPRester(api_key="UhlZvcEux2kmJSQx")

id_expgap = open("ids.txt", "r")

for line in id_expgap:
    words=line.split()
    print words
    id_line=words[0]
    vasp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), str(id_line))
    vasp_run = Vasprun(os.path.join(vasp_dir,"vasprun.xml")).to_dict
    nelect = int(vasp_run['input']['parameters']['NELECT'])
    nband = nelect * 6 +96 - nelect % 96 

    os.chdir(id_line)
    #s = mpr.get_structure_by_material_id(id_line)
    user_incar_settings={"ALGO":'Exact',"NSW":0,"NELM":1,"NBANDS":nband,"LOPTICS":True,"LWAVE":True}
    mpvis = MPVaspInputSet(user_incar_settings=user_incar_settings)
    incar = Incar.from_file(os.path.join(vasp_dir,"INCAR"))
    incar.update(user_incar_settings)
    incar.write_file('INCAR')
    os.chdir('..')
id_expgap.close()
