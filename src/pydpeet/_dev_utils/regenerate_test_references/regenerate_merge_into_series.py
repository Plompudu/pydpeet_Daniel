import sys
from pathlib import Path

import pandas as pd

_SRC_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_SRC_DIR))

from pydpeet.process.merge.series import merge_into_series  # noqa: E402

_RES_DIR = Path(__file__).resolve().parent.parent.parent / "res" / "res_for_unittests"

df = pd.read_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted.parquet")

df1 = df.iloc[:1000].reset_index(drop=True)
df2 = df.iloc[1000:2000].reset_index(drop=True)

result = merge_into_series(
    dfs=[df1, df2],
    time_between_tests_seconds=60.0,
    verbose=True,
    sort_dfs=True,
)

result.to_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted-merge_into_series.parquet")
print("Regenerated: merge_into_series reference data")
