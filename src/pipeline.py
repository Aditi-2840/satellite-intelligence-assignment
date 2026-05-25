import pandas as pd  # type: ignore

READINGS_PATH = "data/parcel_readings.csv"
META_PATH = "data/parcel_metadata.csv"
OUTPUT_PATH = "data/cleaned_parcel_timeseries.csv"



def clean_sensor_status(value):
    if pd.isna(value):
        return "UNKNOWN"

    value = str(value).strip().upper()

    if value == "OK":
        return "OK"

    return "BAD"

def load_data():
    readings = pd.read_csv(READINGS_PATH)
    metadata = pd.read_csv(META_PATH)

    return readings, metadata



def clean_readings(df):
    print(f"Initial readings rows: {len(df)}")

    # Standardize dates
    df["date"] = pd.to_datetime(
        df["date"],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

    # Remove invalid NDVI
    invalid_ndvi = (~df["ndvi_value"].between(-1, 1)).sum()

    print(f"Dropping {invalid_ndvi} invalid NDVI rows")

    df = df[df["ndvi_value"].between(-1, 1)]

    # Standardize sensor status
    df["sensor_status"] = df["sensor_status"].apply(clean_sensor_status)

    # Remove duplicates
    before = len(df)

    df = df.drop_duplicates(subset=["parcel_id", "date"])

    print(f"Dropped {before - len(df)} duplicate rows")

    return df



def clean_metadata(df):
    df["sowing_date"] = pd.to_datetime(
        df["sowing_date"],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

    return df

def join_data(readings, metadata):
    final_df = readings.merge(
        metadata,
        on="parcel_id",
        how="left"
    )

    return final_df

def main():
    readings, metadata = load_data()

    readings = clean_readings(readings)
    metadata = clean_metadata(metadata)

    final_df = join_data(readings, metadata)

    final_df.to_csv(OUTPUT_PATH, index=False)

    print("\nPipeline completed successfully")
    print(f"Final row count: {len(final_df)}")


if __name__ == "__main__":
    main()