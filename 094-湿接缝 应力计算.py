import pandas as pd

from src import Superstructure
from src.sections import DXFSection

if __name__ == "__main__":
    Bridge = Superstructure([45, ] * 5, 60.0, 50.0, pr_detail=True)

    S3 = DXFSection(1, "S45", './src/NU2000B.dxf', 2000, 300, 3100, 0.1)

    S3.addTendon(1340, 1323, 1 * 12 * 140, 1)
    S3.addTendon(1460, 1323, 1 * 12 * 140, 1)
    S3.addTendon(1780, 1323, 1 * 12 * 140, 2)
    S3.addTendon(1900, 1323, 1 * 12 * 140, 2)

    fpe_T1, apc_T1, epc_T1, _no = S3.pos(1).data
    s_fcpg_T1 = S3.ncp().pre_stress(-fpe_T1 * apc_T1, epc_T1, epc_T1)
    fb = S3.ncp().pre_stress(-fpe_T1 * apc_T1, epc_T1, -S3.ncp().yb)
    ft = S3.ncp().pre_stress(-fpe_T1 * apc_T1, epc_T1, S3.ncp().yt)
    print(fb)
    fpe_T1, apc_T1, epc_T1, _no = S3.pos(2).data
    s_fcpg_T1 = S3.cp().pre_stress(-fpe_T1 * apc_T1, epc_T1, epc_T1)
    fb = S3.cp().pre_stress(-fpe_T1 * apc_T1, epc_T1, -S3.cp().yb)
    ft = S3.cp().pre_stress(-fpe_T1 * apc_T1, epc_T1, S3.cp().yt)
    print(fb, ft)
