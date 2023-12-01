import pint
import numpy as np
from pint import UnitRegistry

ureg: UnitRegistry = pint.UnitRegistry()
Q_ = ureg.Quantity

fc = 45.0 * ureg.MPa
fci = fc * 0.8
gc = (2250 + 2.29 * fc.m) * (ureg.kg / ureg.m ** 3)
Ec = 0.041 * 1 * gc.m ** 1.5 * np.sqrt(fc.m) * ureg.MPa
Eci = 0.041 * 1 * gc.m ** 1.5 * np.sqrt(fci.m) * ureg.MPa

print(gc)
print(Ec)
