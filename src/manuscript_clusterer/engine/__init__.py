"""Import the profile as a pandas DataFrame.
"""
from pathlib import Path
import pandas as pd


profile_readings = pd.read_csv(str(Path(__file__).absolute().parent) + "/data/profile_rules.csv", index_col=0)
