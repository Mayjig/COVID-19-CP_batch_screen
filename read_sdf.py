import sys
import string
import rdkit
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.ML.Descriptors import MoleculeDescriptors

file_in  = sys.argv[1]
file_out = file_in.split('.')[0]+"_desc.sdf"
print(file_in)
print(file_out)

ms = [x for x in  Chem.SDMolSupplier(file_in) if x is not None]
ms_wr = Chem.SDWriter(file_out)

nms=[x[0] for x in Descriptors._descList]
#nms.remove('MolecularFormula')
print (len(Descriptors._descList))


calc = MoleculeDescriptors.MolecularDescriptorCalculator(nms)

for i in range(len(ms)):
  descrs = calc.CalcDescriptors(ms[i])
  for x in range(len(descrs)):
    ms[i].SetProp(str(nms[x]),str(descrs[x]))
  ms_wr.write(ms[i])
