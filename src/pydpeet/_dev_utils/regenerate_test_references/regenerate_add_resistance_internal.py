import sys
from pathlib import Path

import pandas as pd

_SRC_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_SRC_DIR))

from pydpeet.process.analyze.configs.battery_config import BatteryConfig  # noqa: E402
from pydpeet.process.analyze.resistance import add_resistance_internal  # noqa: E402

_RES_DIR = Path(__file__).resolve().parent.parent.parent / "res" / "res_for_unittests"

df = pd.read_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted.parquet")

result = add_resistance_internal(
    df=df,
    config=BatteryConfig.DEFAULT,
    verbose=True,
)

result.to_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted-add_resistance_internal.parquet")
print("Regenerated: add_resistance_internal reference data")
