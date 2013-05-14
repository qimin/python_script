__author__ = 'Qimin'

import json
from pymatgen.matproj.rest import MPRester

if __name__ == '__main__':
    mpr = MPRester(api_key="UhlZvcEux2kmJSQx")

id_expgap = open("ids.txt", "r")
for line in id_expgap:
    words=line.split()
    print words
    id_line=words[0]
    bs = mpr.get_bandstructure_by_material_id(1)
    if bs != None:
        target = json.dumps(bs.to_dict)
        obj = json.loads(target)
        print obj["band_gap"]["energy"], obj["vbm"]["energy"], obj["cbm"]["energy"]
id_expgap.close()
