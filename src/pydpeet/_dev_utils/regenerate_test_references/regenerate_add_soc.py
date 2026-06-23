import sys
from pathlib import Path

import pandas as pd

_SRC_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_SRC_DIR))

from pydpeet.process.analyze.configs.battery_config import BatteryConfig  # noqa: E402
from pydpeet.process.analyze.soc import SocMethod, add_soc  # noqa: E402

_RES_DIR = Path(__file__).resolve().parent.parent.parent / "res" / "res_for_unittests"

df = pd.read_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted.parquet")
df_primitives = pd.read_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted-primitives.parquet")

result = add_soc(
    df=df,
    df_primitives=df_primitives,
    neware_bool=True,
    standard_method=SocMethod.WITHOUT_RESET,
    methods=[SocMethod.WITHOUT_RESET, SocMethod.WITH_RESET_WHEN_FULL],
    config=BatteryConfig.DEFAULT,
    lower_soc_for_voltage=0.0,
    upper_soc_for_voltage=1.0,
    lower_voltage_for_soc=0.0,
    upper_voltage_for_soc=0.0,
    verbose=True,
    restart_for_testindex=True,
)

result.to_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted-add_soc.parquet")
print("Regenerated: add_soc reference data")
