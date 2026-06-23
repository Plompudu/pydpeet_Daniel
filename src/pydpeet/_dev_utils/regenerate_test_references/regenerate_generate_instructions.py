import sys
from pathlib import Path

import pandas as pd

_SRC_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_SRC_DIR))

from pydpeet.process.sequence.utils.postprocessing.generate_instructions import extract_instructions  # noqa: E402

_RES_DIR = Path(__file__).resolve().parent.parent.parent / "res" / "res_for_unittests"

df_primitives = pd.read_parquet(_RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted-primitives.parquet")

end_condition_map = {"CC": "voltage", "CV": "current", "CP": "voltage", "Pause": "time"}

result = extract_instructions(
    df_primitives=df_primitives,
    end_condition_map=end_condition_map,
    threshold_warnings=5,
)

output_path = _RES_DIR / "basytec_6_3_1_0-TC23LFP09_CU_25deg-converted-generate_instructions.txt"
with open(output_path, "w", encoding="utf-8") as f:
    for line in result:
        f.write(line + "\n")

print(f"Regenerated: generate_instructions reference data ({len(result)} lines)")
