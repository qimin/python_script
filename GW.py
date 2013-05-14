__author__ = 'Qimin'

import json

from pymatgen.matproj.rest import MPRester
# get structural and other data from the Materials Project database

from pymatgen.io.vaspio_set import VaspInputSet, DictVaspInputSet
# Load standard input set as template

from pymatgen.io.vaspio.vasp_input import Kpoints
# generate KPOINTS

from pymatgen.io.vaspio.vasp_output import Outcar, Vasprun
# from OUTCAR or vasp.xml, get nelect parameters

import os
# file operation

class QiminGWVaspInputSet(VaspInputSet):
    """
    Typical implementation of input set for a GW run.
    """
    def __init__(self, user_incar_settings=None, constrain_total_magmom=False):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(module_dir, "QiminGWVaspInputSet.json")) as f:
            DictVaspInputSet.__init__(
                self, "Qimin GW", json.load(f),
                constrain_total_magmom=constrain_total_magmom)
        if user_incar_settings:
            self.incar_settings.update(user_incar_settings)

if __name__ == '__main__':
    mpr = MPRester(api_key="UhlZvcEux2kmJSQx")

id_expgap = open("ids.txt", "r")

for line in id_expgap:
    words=line.split()
    print words
    id_line=words[0]
    
    s = mpr.get_structure_by_material_id(id_line)
    vasp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), str(id_line))
    vasp_run = Vasprun(os.path.join(vasp_dir,"vasprun.xml")).to_dict
    nelect = int(vasp_run['input']['parameters']['NELECT'])
    nband = nelect * 6 +96 - nelect % 96 

    
    os.chdir(id_line)
    user_incar_settings={"ENCUTGW":150,"NBANDS":nband,"NOMEGA":96}
    mpvis = QiminGWVaspInputSet(user_incar_settings=user_incar_settings)
    mpvis.get_incar(s).write_file('INCAR')

    os.chdir('..')
id_expgap.close()
