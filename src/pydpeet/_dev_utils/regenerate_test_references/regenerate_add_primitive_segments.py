import sys
from pathlib import Path

import pandas as pd

_SRC_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_SRC_DIR))

from pydpeet.process.sequence.configs.config import PrimitiveConfig  # noqa: E402
from pydpeet.process.sequence.step_analyzer import add_primitive_segments  # noqa: E402

_RES_DIR = Path(__file__).resolve().parent.parent.parent / "res" / "res_for_unittests"

df = pd.read_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted.parquet")

result = add_primitive_segments(
    df=df,
    config=PrimitiveConfig.FALLBACK,
)

result.to_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted-add_primitive_segments.parquet")
print("Regenerated: add_primitive_segments reference data")
