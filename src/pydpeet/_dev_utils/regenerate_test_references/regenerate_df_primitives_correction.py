import sys
from pathlib import Path

import pandas as pd

_SRC_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_SRC_DIR))

from pydpeet.process.sequence.utils.postprocessing.df_primitives_correction import (  # noqa: E402
    df_primitives_correction,
)

_RES_DIR = Path(__file__).resolve().parent.parent.parent / "res" / "res_for_unittests"

df_primitives = pd.read_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted-primitives.parquet")

correction_config = {
    "replace_ID": {5: "V"},
    "replace_time": {(100.0, 200.0): "I"},
    "replace_time_and_merge": {(500.0, 600.0): "P"},
    "merge_left": [10],
    "merge_right": [15],
    "merge_range": [(20, 25)],
}

data_columns = {"I": "Current[A]", "P": "Power[W]", "V": "Voltage[V]"}

thresholds = {"V": 0.1, "I": 0.1, "P": 0.1}

result = df_primitives_correction(
    df_primitives=df_primitives,
    correction_config=correction_config,
    data_columns=data_columns,
    thresholds=thresholds,
    reindex=True,
    reannotate=True,
)

result.to_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted-primitives-corrected.parquet")
print("Regenerated: df_primitives_correction reference data")
