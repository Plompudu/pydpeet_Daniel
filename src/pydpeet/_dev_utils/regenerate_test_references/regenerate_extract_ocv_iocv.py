import sys
from pathlib import Path

import pandas as pd

_SRC_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_SRC_DIR))

from pydpeet import battery_config_wrapper  # noqa: E402
from pydpeet.process.analyze.extract.ocv import extract_ocv_iocv  # noqa: E402

_RES_DIR = Path(__file__).resolve().parent.parent.parent / "res" / "res_for_unittests"

df_neware = pd.read_parquet(_RES_DIR / "neware_8_0_0_516-Cal_Ageing_Checkup3.parquet")
df_neware_primitives = pd.read_parquet(_RES_DIR / "neware_8_0_0_516-Cal_Ageing_Checkup3_primitives.parquet")

result = extract_ocv_iocv(
    min_pause_lenght=120.0,
    min_loops=70.0,
    visualize=False,
    df_primitives=df_neware_primitives,
    df=None,
    config=battery_config_wrapper(c_ref=4.75, max_voltage=4.2, min_voltage=2.5, voltage_intervall=0.01),
)

for i, block_df in enumerate(result):
    block_df.to_parquet(_RES_DIR / f"neware_8_0_0_516-Cal_Ageing_Checkup3_extract_ocv_iocv_block_{i}.parquet")
print(f"Regenerated: extract_ocv_iocv reference data ({len(result)} blocks)")
