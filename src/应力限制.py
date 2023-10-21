import pint
import numpy as np
from pint import UnitRegistry

ureg: UnitRegistry = pint.UnitRegistry()
Q_ = ureg.Quantity

Eg = 0.0002 * (1 / ureg.ft)
fc = 70 * ureg.MPa
Smax = min(0.0948 * np.sqrt(fc.to(ureg.ksi).m), 0.3) * ureg.ksi

print(Smax, Smax.to(ureg.MPa))
print((0.24 * np.sqrt(fc.to(ureg.ksi).m) * ureg.ksi).to(ureg.MPa))
print((70 * ureg.MPa).to(ureg.ksi))
