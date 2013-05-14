__author__ = 'Qimin'

from pymatgen.matproj.rest import MPRester
from pymatgen.io.vaspio.vasp_input import Kpoints,Incar
from pymatgen.io.vaspio.vasp_output import Outcar, Vasprun
from pymatgen.io.vaspio_set import MPNonSCFVaspInputSet, MPStaticVaspInputSet
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
    nband = int(vasp_run['input']['parameters']['NBANDS'])
    

    os.chdir(id_line)

    user_incar_settings={"EDIFF":1E-4,"NBANDS":nband,"NSW":0}
    mpvis = MPNonSCFVaspInputSet(user_incar_settings=user_incar_settings)
    s = mpr.get_structure_by_material_id(id_line)
    mpvis.get_kpoints(s).write_file('KPOINTS')
    mpvis.get_incar(s).write_file('INCAR')
    
    os.chdir('..')
id_expgap.close()
