"""
Fleet Performance Analysis
Reads vehicle telematics CSV, outputs fuel efficiency, driver safety scores,
and flags anomalies. Single-file, pandas only.
"""
import pandas as pd

INPUT_FILE = "fleet_data.csv"

# Safety score weights (lower = better driver)
WEIGHTS = {
    "harsh_braking_events": 3,
    "speeding_events": 4,
    "idle_minutes": 0.1,
}

def load_data(path):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df["fuel_efficiency_km_per_l"] = df["distance_km"] / df["fuel_litres"]
    return df

def vehicle_summary(df):
    return (
        df.groupby("vehicle_id")
        .agg(
            total_distance_km=("distance_km", "sum"),
            total_fuel_l=("fuel_litres", "sum"),
            avg_idle_min=("idle_minutes", "mean"),
        )
        .assign(
            avg_fuel_efficiency=lambda x: x["total_distance_km"] / x["total_fuel_l"]
        )
        .round(2)
    )

def driver_safety_scores(df):
    df = df.copy()
    df["safety_penalty"] = (
        df["harsh_braking_events"] * WEIGHTS["harsh_braking_events"]
        + df["speeding_events"] * WEIGHTS["speeding_events"]
        + df["idle_minutes"] * WEIGHTS["idle_minutes"]
    )
    scores = (
        df.groupby("driver_id")["safety_penalty"]
        .sum()
        .reset_index()
        .assign(safety_score=lambda x: (100 - x["safety_penalty"]).clip(lower=0).round(1))
        .sort_values("safety_score", ascending=False)
    )
    return scores[["driver_id", "safety_score"]]

def flag_anomalies(df):
    flags = []
    # Anomaly 1: fuel efficiency far below fleet mean (possible siphoning)
    mean_eff = df["fuel_efficiency_km_per_l"].mean()
    for _, row in df.iterrows():
        if row["fuel_efficiency_km_per_l"] < mean_eff * 0.75:
            flags.append(
                f"LOW FUEL EFFICIENCY: {row['vehicle_id']} on {row['date'].date()} "
                f"({row['fuel_efficiency_km_per_l']:.2f} km/L vs fleet avg {mean_eff:.2f})"
            )
    # Anomaly 2: excessive idle
    for _, row in df.iterrows():
        if row["idle_minutes"] > 90:
            flags.append(
                f"EXCESS IDLE: {row['vehicle_id']} on {row['date'].date()} "
                f"({row['idle_minutes']} min)"
            )
    # Anomaly 3: high harsh braking
    for _, row in df.iterrows():
        if row["harsh_braking_events"] >= 5:
            flags.append(
                f"HARSH BRAKING: {row['vehicle_id']} on {row['date'].date()} "
                f"({row['harsh_braking_events']} events)"
            )
    return flags

def main():
    print("=" * 60)
    print("FLEET PERFORMANCE ANALYSIS")
    print("=" * 60)

    df = load_data(INPUT_FILE)
    print(f"\nLoaded {len(df)} records across {df['vehicle_id'].nunique()} vehicles "
          f"and {df['driver_id'].nunique()} drivers.\n")

    print("-" * 60)
    print("VEHICLE SUMMARY")
    print("-" * 60)
    print(vehicle_summary(df).to_string())

    print("\n" + "-" * 60)
    print("DRIVER SAFETY SCORES (100 = perfect)")
    print("-" * 60)
    print(driver_safety_scores(df).to_string(index=False))

    print("\n" + "-" * 60)
    print("ANOMALIES FLAGGED")
    print("-" * 60)
    flags = flag_anomalies(df)
    if flags:
        for f in flags:
            print(f"  ! {f}")
    else:
        print("  None detected.")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
