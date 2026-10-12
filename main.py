import pandas as pd
import numpy as np

df = pd.read_excel("medical_equipment_maintenance_dataset.xlsx")

print(df.head())
print(df.shape)
print(df.info())
print(df.isnull().sum())
print("Duplicate rows:", df.duplicated().sum())
print(df.describe())
print(df.describe().T)
print(df["maintenance_type"].value_counts())
print(df["equipment_type"].value_counts())
print(df["department"].value_counts())
downtime_by_equipment = df.groupby("equipment_type")["downtime_hours"].mean()

print(downtime_by_equipment)
downtime_by_department = df.groupby("department")["downtime_hours"].mean()
print(downtime_by_department.sort_values(ascending=False))
print("\nAverage downtime by department:")
downtime_by_department = df.groupby("department")["downtime_hours"].mean()
print(downtime_by_department.sort_values(ascending=False))
cost_by_equipment = df.groupby("equipment_type")["service_cost_ngn"].mean()

print("\nAverage service cost by equipment:")
print(cost_by_equipment.sort_values(ascending=False).round(2))
maintenance_counts = df["maintenance_type"].value_counts()

print("\nMaintenance workload:")
print(maintenance_counts)

print("\nMaintenance workload percentage:")
print((maintenance_counts / len(df) * 100).round(2))
print("\nPreventive maintenance status:")
print(df["pm_status"].value_counts())

print("\nPreventive maintenance status percentages:")
print((df["pm_status"].value_counts(normalize=True) * 100).round(2))
pm_records = df[df["maintenance_type"] == "Preventive"]

print("\nPreventive maintenance records:")
print(pm_records["pm_status"].value_counts())

print("\nPreventive maintenance status percentages:")
print(
    (pm_records["pm_status"].value_counts(normalize=True) * 100)
    .round(2)
)

# Late preventive maintenance by equipment type

pm_records = df[df["pm_status"].isin(["On Time", "Late"])]

late_pm = pm_records[pm_records["pm_status"] == "Late"]

late_by_equipment = (
    late_pm["equipment_type"]
    .value_counts()
)

print("\nLate preventive maintenance by equipment type:")
print(late_by_equipment)

# Late preventive maintenance rate by equipment type

pm_records = df[df["pm_status"].isin(["On Time", "Late"])].copy()

pm_summary = (
    pm_records.groupby("equipment_type")["pm_status"]
    .agg(
        total_pm_records="count",
        late_records=lambda x: (x == "Late").sum()
    )
)

pm_summary["late_rate_pct"] = (
    pm_summary["late_records"]
    / pm_summary["total_pm_records"] * 100
).round(2)

pm_summary = pm_summary.sort_values(
    "late_rate_pct", ascending=False
)

print("\nPreventive maintenance compliance by equipment:")
print(pm_summary)


import matplotlib.pyplot as plt

rates = pm_summary["late_rate_pct"].sort_values()

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(rates.index, rates.values)

ax.bar_label(
    bars,
    labels=[f"{value:.2f}%" for value in rates.values],
    padding=4,
    fontsize=9
)

ax.set_xlabel("Late Preventive Maintenance Rate (%)")
ax.set_ylabel("Equipment Type")
ax.set_title("Late Preventive Maintenance Rate by Equipment Type")

ax.set_xlim(0, max(rates.values) + 8)
ax.grid(axis="x", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("pm_late_rate_by_equipment.png", dpi=300, bbox_inches="tight")
plt.show()

# Chart 2: Average service cost by equipment type

avg_cost = (
    df.groupby("equipment_type")["service_cost_ngn"]
    .mean()
    .sort_values()
)

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(avg_cost.index, avg_cost.values)

ax.bar_label(
    bars,
    labels=[f"₦{value:,.0f}" for value in avg_cost.values],
    padding=4,
    fontsize=8
)

ax.set_xlabel("Average Service Cost (NGN)")
ax.set_ylabel("Equipment Type")
ax.set_title("Average Service Cost by Equipment Type")

ax.set_xlim(0, max(avg_cost.values) * 1.3)
ax.grid(axis="x", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("average_service_cost_by_equipment.png", dpi=300, bbox_inches="tight")
plt.show()




# Chart 3: Maintenance Workload Distribution

workload = df["maintenance_type"].value_counts()
percentages = workload / workload.sum() * 100

fig, ax = plt.subplots(figsize=(8, 6))

wedges, texts, autotexts = ax.pie(
    workload,
    labels=workload.index,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.7
)

ax.set_title("Maintenance Workload Distribution")

plt.tight_layout()
plt.savefig("maintenance_workload_distribution.png", dpi=300, bbox_inches="tight")
plt.show()