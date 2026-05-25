import pandas as pd # type: ignore
import numpy as np # type: ignore


DATA_PATH = "data/cleaned_parcel_timeseries.csv"

def main():
    df = pd.read_csv(DATA_PATH)

    # Convert dates
    df["date"] = pd.to_datetime(df["date"])
    df["sowing_date"] = pd.to_datetime(df["sowing_date"])

    # Ignore bad sensors
    df = df[df["sensor_status"] == "OK"]

    # Days relative to sowing
    df["days_from_sowing"] = (
        df["date"] - df["sowing_date"]
    ).dt.days

    before_df = df[
        (df["days_from_sowing"] >= -30)
        & (df["days_from_sowing"] < 0)
    ]

    after_df = df[
        (df["days_from_sowing"] >= 0)
        & (df["days_from_sowing"] <= 30)
    ]

    before_summary = (
        before_df
        .groupby("crop_type")
        .agg(mean_ndvi_before=("ndvi_value", "mean"))
        .reset_index()
    )

    after_summary = (
        after_df
        .groupby("crop_type")
        .agg(
            mean_ndvi_after=("ndvi_value", "mean"),
            n_parcels=("parcel_id", "nunique")
        )
        .reset_index()
    )

    final_summary = before_summary.merge(
        after_summary,
        on="crop_type",
        how="outer"
    )

    final_summary = final_summary.round(3)

    print("\nAnalysis Output\n")
    print(final_summary)


if __name__ == "__main__":
    main()