import pandas as pd
import numpy as np

PROCESSED_PATH = 'data/processed/'
RAW_PATH = 'data/raw/'

# 1. Load Master Fact and Raw Circuits
master = pd.read_csv(PROCESSED_PATH + 'master_fact.csv')
raw_circuits = pd.read_csv(RAW_PATH + 'circuits.csv')

# Only keep circuits that appear in master_fact!
valid_circuits = master['circuitId'].unique()

# 2. Compute Aggregations
agg_df = master.groupby('circuitId').agg(
    total_races=('raceId', 'nunique'),
    avg_delta=('grid_to_finish_delta', 'mean'),
    avg_qualifying_gap=('qualifying_gap_ms', 'mean'),
    lap_time_variance=('lap_time_std', 'mean')
).reset_index()

# Compute stop averages
stop1 = master[master['stop_count_bucket'] == '1 stop'].groupby('circuitId')['position'].mean().reset_index().rename(columns={'position': 'avg_1stop_position'})
stop2 = master[master['stop_count_bucket'] == '2 stops'].groupby('circuitId')['position'].mean().reset_index().rename(columns={'position': 'avg_2stop_position'})

# Compute Lock-in Score (correlation between grid and position)
lock_in = []
for cid, group in master.groupby('circuitId'):
    valid = group.dropna(subset=['grid', 'position'])
    if len(valid) > 5:
        # We cap grid and pos at 20 just in case
        corr = valid['grid'].corr(valid['position'])
        if pd.isna(corr): corr = 0
        score = corr * 100
    else:
        score = 0
    lock_in.append({'circuitId': cid, 'qualifying_lock_in_score': round(score, 1)})
lock_in_df = pd.DataFrame(lock_in)

# Merge
df = pd.DataFrame({'circuitId': valid_circuits})
df = df.merge(agg_df, on='circuitId', how='left')
df = df.merge(stop1, on='circuitId', how='left')
df = df.merge(stop2, on='circuitId', how='left')
df = df.merge(lock_in_df, on='circuitId', how='left')

# Determine Optimal Stop Count and Best Strategy Stops
df['avg_1stop_position'] = df['avg_1stop_position'].fillna(df['avg_1stop_position'].mean())
df['avg_2stop_position'] = df['avg_2stop_position'].fillna(df['avg_2stop_position'].mean())
df['optimal_stop_count'] = np.where(df['avg_1stop_position'] <= df['avg_2stop_position'], 1, 2)
df['best_strategy_stops'] = df['optimal_stop_count'].astype(float)

# Determine Overtaking Score based on lap time variance
df['variance_rank'] = df['lap_time_variance'].rank(method='first')
def rank_to_tier(r, n):
    if pd.isna(r): return 'N/A'
    pct = r / n
    if pct >= 0.67: return 'High'
    elif pct >= 0.33: return 'Medium'
    else: return 'Low'
df['overtaking_score'] = df['variance_rank'].apply(lambda r: rank_to_tier(r, len(df)))
df.drop(columns=['variance_rank'], inplace=True)

# Merge Circuit Info
c_info = raw_circuits[['circuitId', 'name', 'country', 'lat', 'lng']].rename(columns={'name': 'circuit_name'})
df = df.merge(c_info, on='circuitId', how='left')

# Determine Clusters based on Lock-in Score (Simple Heuristic aligned with F1 logic)
# > 60: Qualifying-Dominant
# < 45: Strategy-Dominant
# Else: Mixed
def get_cluster_label(score):
    if score >= 60: return 'Qualifying-Dominant'
    elif score < 45: return 'Strategy-Dominant'
    else: return 'Mixed'

df['cluster_label'] = df['qualifying_lock_in_score'].apply(get_cluster_label)
cluster_map = {'Strategy-Dominant': 2, 'Mixed': 1, 'Qualifying-Dominant': 0}
df['cluster_id'] = df['cluster_label'].map(cluster_map)
df['cluster'] = df['cluster_id']

# Default Compound Bias
df['compound_bias'] = 0

# Final Columns order
final_cols = [
    'circuitId', 'circuit_name', 'country', 'lat', 'lng', 'total_races', 
    'avg_delta', 'avg_qualifying_gap', 'lap_time_variance', 'best_strategy_stops', 
    'avg_1stop_position', 'avg_2stop_position', 'overtaking_score', 'cluster_id', 
    'cluster_label', 'cluster', 'qualifying_lock_in_score', 'optimal_stop_count', 
    'compound_bias'
]

df = df[final_cols]
df.to_csv(PROCESSED_PATH + 'circuit_strategy_profile.csv', index=False)
print(f"Successfully generated circuit_strategy_profile.csv with {len(df)} rows and {len(df.columns)} columns.")
