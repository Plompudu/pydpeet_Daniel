import sys
from pathlib import Path

_SRC_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_SRC_DIR))

from pydpeet import convert  # noqa: E402

_RES_DIR = Path(__file__).resolve().parent.parent.parent / "res" / "res_for_unittests"

input_txt = str(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg.txt")

df = convert(config="basytec_6_3_1_0", input_path=input_txt, keep_all_additional_data=False)
df.to_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted.parquet")
print("Regenerated: converted base data (without additional data)")

df_with_additional = convert(config="basytec_6_3_1_0", input_path=input_txt, keep_all_additional_data=True)
df_with_additional.to_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted-with-additional.parquet")
print("Regenerated: converted base data (with additional data)")
