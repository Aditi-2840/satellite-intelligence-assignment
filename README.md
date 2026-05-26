# Satellite Intelligence Data Engineering Assignment

## Project Overview

This project processes agricultural parcel-level satellite and sensor data to build a cleaned time-series dataset for downstream analytics.

The pipeline:
- ingests parcel readings and parcel metadata
- performs data quality checks and cleaning
- standardizes inconsistent fields
- joins datasets into a parcel-level time-series dataset
- performs NDVI analysis around crop sowing periods

The objective is to simulate a realistic production-style data wrangling workflow for agricultural intelligence systems.

---

## Repository Structure

```text
satellite-intelligence-assignment/
│
├── data/
│   ├── parcel_readings.csv
│   ├── parcel_metadata.csv
│   └── cleaned_parcel_timeseries.csv
│
├── src/
│   ├── pipeline.py
│   └── analysis.py
│
├── notebooks/
│   └── exploration.ipynb
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Setup Instructions

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the cleaning pipeline:

```bash
python src/pipeline.py
```

Run the analysis:

```bash
python src/analysis.py
```

---

## Data Quality Audit

### parcel_readings.csv

| Issue | Count | Decision | Justification |
|---|---|---|---|
| Invalid NDVI values outside [-1,1] | 104 | Dropped | NDVI outside physical range is invalid |
| Duplicate parcel_id + date rows | 8 | Removed duplicates | Time-series should have unique parcel/date combinations |
| Inconsistent sensor status values | Multiple formats | Standardized | Prevent inconsistent filtering logic |
| Missing sensor status values | 137 | Marked as UNKNOWN | Retained for traceability but excluded from analysis |
| Mixed date formats | Present | Standardized using pandas datetime parsing | Required for time-series analysis |

### parcel_metadata.csv

| Issue | Count | Decision | Justification |
|---|---|---|---|
| Mixed sowing_date formats | Present | Standardized | Required for temporal calculations |

---

## Cleaning Approach

The cleaning pipeline performs the following transformations:

1. Standardized all date columns using pandas datetime parsing
2. Removed invalid NDVI readings outside the valid range [-1,1]
3. Standardized sensor status values into:
   - OK
   - BAD
   - UNKNOWN
4. Removed duplicate parcel_id + date records
5. Joined parcel readings with parcel metadata using parcel_id

The final output dataset represents one row per parcel_id × date containing environmental readings and parcel metadata.

---

## Analysis Output

| crop_type | mean_ndvi_before | mean_ndvi_after | n_parcels |
|---|---|---|---|
| sugarcane | 0.312 | 0.587 | 10 |
| wheat | 0.221 | 0.401 | 8 |
| soybean | 0.287 | 0.533 | 10 |

---

## Interpretation

Most crop types showed higher NDVI values after sowing, indicating increased vegetation growth following planting.

Sugarcane showed the strongest NDVI increase, which aligns with expected crop growth behavior. Some crop types showed smaller increases, potentially due to seasonal conditions, sparse valid readings, or sensor quality issues.

---

## Production Reflection

### If the dataset became 100× larger

I would make the following changes:

1. Move from Pandas to Spark or Polars for distributed processing
2. Store datasets as partitioned Parquet instead of CSV
3. Implement incremental processing instead of full refreshes

### Production Monitoring

I would monitor:

- Daily row count anomalies
- Null spikes in critical columns
- Duplicate parcel/date records
- Sensor status distribution changes
- Failed or late-arriving data
- NDVI distribution shifts

### Most Likely Silent Failure

The most likely silent failure would be inconsistent upstream date formats or schema drift causing incorrect temporal joins without fully breaking the pipeline.

This could silently affect downstream NDVI calculations around sowing periods.

---

## AI Usage

ChatGPT was used to assist with project structuring, code readability improvements, and reviewing data quality handling approaches.

All implementation decisions and logic were reviewed and validated manually.