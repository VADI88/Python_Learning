# Class : SKILLSHARE

import polars as pl
import matplotlib.pyplot as plt
from pathlib import Path

data_folder_path = Path("data")

chicago_crimes_data_path: Path = data_folder_path / "crimes-2022.csv"
japanese_customs_trade_path: Path = data_folder_path / "custom_1988_2020.csv"

chicago_crimes_data = pl.read_csv(chicago_crimes_data_path)
japanese_customs_trade_data = pl.read_csv(japanese_customs_trade_path)

# basic understanding of polar

print(chicago_crimes_data.shape)
chicago_crimes_data.head()

chicago_crimes_data.describe()
