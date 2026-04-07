import matplotlib
import matplotlib.pyplot as plt

from pywaterinfo import Waterinfo

matplotlib.rcParams.update(
    {
        "font.family": "monospace",  # or 'serif', 'monospace', etc.
        "font.size": 12,  # set the default font size
        "figure.figsize": (15, 8),
        "figure.dpi": 300,
    }
)


hic = Waterinfo("hic")

# Get data from start of time series up to next two days
df_ensemble_data = hic.get_ensemble_timeseries_values(
    ts_id=84015010,
    start="2021-01-28",
    end="2021-01-29",
)


fig, ax = plt.subplots()

for name, group in df_ensemble_data.groupby("ensembledate"):
    _ = ax.plot(group["Timestamp"], group["0"], label=str(name), alpha=1)

_ = ax.set_xlabel("Timestamp")
_ = ax.set_ylabel("Value")
_ = ax.set_title("Available TOFs with their timeseries")
_ = ax.legend(title="Ensemble Date")
_ = ax.grid(True)
plt.tight_layout()
