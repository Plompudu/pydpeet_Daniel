import sys
from pathlib import Path

import pandas as pd

_SRC_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_SRC_DIR))

from pydpeet.process.sequence.utils.postprocessing.filter_df import filter_and_split_df_by_blocks  # noqa: E402

_RES_DIR = Path(__file__).resolve().parent.parent.parent / "res" / "res_for_unittests"

df_segments_and_sequences = pd.read_parquet(
    _RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted-segments-and-sequences.parquet"
)
df_primitives = pd.read_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted-primitives.parquet")

dfs_per_block, df_filtered = filter_and_split_df_by_blocks(
    df_segments_and_sequences=df_segments_and_sequences,
    df_primitives=df_primitives,
    rules=["CC_Discharge", "Pause"],
    combine_op="or",
    print_blocks=False,
    also_return_filtered_df=True,
)

expected_dir = _RES_DIR / "filter_and_split_df_by_blocks_expected"
expected_dir.mkdir(parents=True, exist_ok=True)

df_filtered.to_parquet(expected_dir / "df_filtered.parquet")

for i, block_df in enumerate(dfs_per_block):
    block_df.to_parquet(expected_dir / f"block_{i}.parquet")

print(f"Regenerated: filter_and_split_df_by_blocks reference data ({len(dfs_per_block)} blocks)")
