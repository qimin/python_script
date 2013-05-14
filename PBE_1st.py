__author__ = 'Qimin'

import json

from pymatgen.matproj.rest import MPRester
# get structural and other data from the Materials Project database

from pymatgen.io.vaspio_set import MPVaspInputSet, DictVaspInputSet
# Load standard input set as template

from pymatgen.io.vaspio.vasp_input import Kpoints
# generate KPOINTS

from pymatgen.io.vaspio.vasp_output import Outcar, Vasprun
# from OUTCAR or vasp.xml, get nelect parameters

import os
# file operation

if __name__ == '__main__':
    mpr = MPRester(api_key="UhlZvcEux2kmJSQx")

potcar_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'POTCARs')
# set up POTCAR directory path
os.environ['VASP_PSP_DIR'] = potcar_dir
# print os.environ['VASP_PSP_DIR']

id_expgap = open("ids.txt", "r")
for line in id_expgap:
    words=line.split()
    print words
    id_line=words[0]
    os.mkdir(id_line)
    os.chdir(id_line)
    s = mpr.get_structure_by_material_id(id_line)
    # obtain structural information from Materials Project database
    #print json.dumps(s.to_dict)
    # convert structural infomation into a dictionary and then dump to a json file

    user_incar_settings={"ALGO":'Normal',"EDIFF":1E-8,"ENCUT":500,"NSW":0,"LWAVE":True}
    mpvis = MPVaspInputSet(user_incar_settings=user_incar_settings)

    mpvis.get_incar(s).write_file('INCAR')
    # from the GW input set, get the incar parameters, generate INCAR
    print mpvis.get_incar(s)
    #
    kp_density = mpvis.get_kpoints(s).kpts[0]
    # from the GW input set, get the k-point density
    kpoints = Kpoints.gamma_automatic(kp_density)
    # generate Gamma centered k-point mesh
    kpoints.write_file('KPOINTS')
    # generate KPOINTS file
    mpvis.get_poscar(s).write_file('POSCAR')
    # generate POSCAR file
    mpvis.get_potcar(s).write_file('POTCAR')
    # generate POTCAR file
    os.chdir('..')
id_expgap.close()
