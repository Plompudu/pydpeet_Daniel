"""
Auto-generated __init__ file.
Created: 2026-03-06 15:11:49
"""

# Re-export selected names from source modules

from pydpeet.citations.citeme import print_references, write_to_bibtex
from pydpeet.io.configs.config import DataOutputFiletype, ReadConfig
from pydpeet.io.convert import convert
from pydpeet.io.map import mapping
from pydpeet.io.read import read
from pydpeet.io.utils import load_custom_module
from pydpeet.io.write import write
from pydpeet.process.analyze.capacity import add_capacity, add_charge_throughput
from pydpeet.process.analyze.configs.battery_config import BatteryConfig, battery_config_wrapper
from pydpeet.process.analyze.cycle import add_equivalent_full_cycles
from pydpeet.process.analyze.efficiency import add_efficiency_coulomb
from pydpeet.process.analyze.energy import add_cumulative_energy
from pydpeet.process.analyze.extract.dva_ica import compute_ocv_dva_ica
from pydpeet.process.analyze.extract.ocv import extract_ocv_iocv
from pydpeet.process.analyze.power import add_power
from pydpeet.process.analyze.resistance import add_resistance_internal
from pydpeet.process.analyze.soc import SocMethod, add_soc
from pydpeet.process.analyze.soh import add_soh
from pydpeet.process.merge.series import merge_into_campaign, merge_into_series
from pydpeet.process.sequence.configs.config import (
    DeviceConfig,
    PrimitiveConfig,
    SequenceOverviewConfig,
    VisualizationConfig,
    primitive_config_wrapper,
    sequence_overview_config_wrapper,
    visualization_config_wrapper,
)
from pydpeet.process.sequence.step_analyzer import add_primitive_segments, extract_sequence_overview
from pydpeet.process.sequence.utils.postprocessing.df_primitives_correction import df_primitives_correction
from pydpeet.process.sequence.utils.postprocessing.filter_df import (
    filter_and_split_df_by_blocks,
    filter_df,
    return_or_print_blocks,
    split_df_by_blocks,
)
from pydpeet.process.sequence.utils.postprocessing.generate_instructions import generate_instructions
from pydpeet.process.sequence.utils.preprocessing.calculate_thresholds import calculate_minimum_definitive_differences
from pydpeet.process.sequence.utils.visualize.visualize_data import visualize_phases
from pydpeet.utils.logging_style import set_logging_style

# Public API for this package
__all__ = [
    # Tutorial 01
    "set_logging_style",
    "ReadConfig",
    "read",
    "DataOutputFiletype",
    "load_custom_module",
    "mapping",  # TODO diskutieren ob private
    "merge_into_series",
    "write",
    "print_references",
    "write_to_bibtex",
    # Tutorial 02
    "DeviceConfig",
    "PrimitiveConfig",
    "primitive_config_wrapper",
    "add_primitive_segments",
    "calculate_minimum_definitive_differences",
    "VisualizationConfig",
    "visualization_config_wrapper",
    "visualize_phases",
    # Tutorial 03
    "SequenceOverviewConfig",
    "sequence_overview_config_wrapper",
    "df_primitives_correction",
    "extract_sequence_overview",
    # Tutorial 04
    "BatteryConfig",
    "battery_config_wrapper",
    # Tutorial 05
    "extract_ocv_iocv",
    "compute_ocv_dva_ica",
    # Tutorial 06
    "SocMethod",
    "add_capacity",
    "add_charge_throughput",
    "add_cumulative_energy",
    "add_efficiency_coulomb",
    "add_equivalent_full_cycles",
    "add_power",
    "add_resistance_internal",
    "add_soc",
    "add_soh",
    # Tutorial 07
    "filter_and_split_df_by_blocks",
    "filter_df",
    "generate_instructions",
    "return_or_print_blocks",
    "split_df_by_blocks",
    # TODO was ist das / wofür braucht man das?
    "merge_into_campaign",

    # TODO diskutieren ob wir es überhaupt brauchen, da read
    "convert",]
