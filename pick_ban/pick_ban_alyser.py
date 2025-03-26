import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.ticker as mticker
import seaborn as sns

df = pd.read_csv("picks_and_bans_LCP.csv")

# Step 1: Reverse to chronological order
df = df[::-1].reset_index(drop=True)

# Step 2: Initialize records dictionary
records = defaultdict(lambda: {'W': 0, 'L': 0})

# Step 3: Track running W-L records
team1_records = []
team2_records = []

for i, row in df.iterrows():
    t1 = row['Blue']
    t2 = row['Red']
    res = row['Winner']
    
    # Get pre-game records
    t1_record = records[t1]
    t2_record = records[t2]
    
    team1_records.append(f"{t1_record['W']}-{t1_record['L']}")
    team2_records.append(f"{t2_record['W']}-{t2_record['L']}")
    
    # Update records based on result
    if res == 1:
        records[t1]['W'] += 1
        records[t2]['L'] += 1
    elif res == 2:
        records[t1]['L'] += 1
        records[t2]['W'] += 1

# Step 4: Add records and reverse back to original order
df['team1_record'] = team1_records
df['team2_record'] = team2_records
df = df[::-1].reset_index(drop=True)

print(df.head())
champ_stats = defaultdict(lambda: {'wins': 0, 'games': 0})
champ_stats_weighted = defaultdict(lambda: {'wins': 0, 'games': 0})

df['wins1'] = df['team1_record'].str.split('-').str[0].astype(int)
df['wins2'] = df['team2_record'].str.split('-').str[0].astype(int)
df['loss1'] = df['team1_record'].str.split('-').str[1].astype(int)
df['loss2'] = df['team2_record'].str.split('-').str[1].astype(int)

# Expand all RP and BP columns
df[['RP1', 'RP2']] = df['RP1-2'].str.split(',', expand=True)
df[['BP2', 'BP3']] = df['BP2-3'].str.split(',', expand=True)
df[['BP4', 'BP5']] = df['BP4-5'].str.split(',', expand=True)

# Strip whitespace
for col in ['RP1', 'RP2', 'RP3', 'RP4', 'RP5', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5']:
    df[col] = df[col].str.strip()

# Loop through rows
for _, row in df.iterrows():
    blue_team = [row['BP1'], row['BP2'], row['BP3'], row['BP4'], row['BP5']]
    red_team = [row['RP1'], row['RP2'], row['RP3'], row['RP4'], row['RP5']]
    winner = row['Winner']

    # Games played
    for champ in blue_team + red_team:
        champ_stats[champ]['games'] += 1
        champ_stats_weighted[champ]['games'] += 1

    # Calculate total for weighting
    total_games = row['wins1'] + row['wins2'] + row['loss1'] + row['loss2']
    if total_games == 0:
        total_games = 1  # avoid division by zero

    if winner == 1:
        weight = 1 - (row['wins1'] - row['wins2']) / total_games
        for champ in blue_team:
            champ_stats[champ]['wins'] += 1
            champ_stats_weighted[champ]['wins'] += weight

    elif winner == 2:
        weight = 1 - (row['wins2'] - row['wins1']) / total_games
        for champ in red_team:
            champ_stats[champ]['wins'] += 1
            champ_stats_weighted[champ]['wins'] += weight

# Compute final winrates
final_winrates = {
    champ: stats['wins'] / stats['games'] if stats['games'] > 0 else 0
    for champ, stats in champ_stats.items()
}

final_winrates_adj = {
    champ: stats['wins'] / stats['games'] if stats['games'] > 0 else 0
    for champ, stats in champ_stats_weighted.items()
}

# Create DataFrame
winrate_df = pd.DataFrame([
    {
        'champion': champ,
        'wins': stats['wins'],
        'games': stats['games'],
        'winrate': final_winrates[champ],
        'adj': final_winrates_adj[champ]
    }
    for champ, stats in champ_stats.items()
])

# Sort by number of games and reset index
winrate_df = winrate_df.sort_values(by='games', ascending=False).reset_index(drop=True)

# Save to CSV
winrate_df.to_csv('winrates_adj_lcp.csv', index=False)





custom_colors = sns.color_palette("tab10", 2)  # 2 teams

filtered_bp1 = df[df['Blue'].isin(['DetonatioN FocusMe', 'Chiefs Esports Club'])]
pick_counts_bp1 = pd.crosstab(filtered_bp1['BP1'], filtered_bp1['Blue'])

df_melted = df.melt(id_vars=['Red'], value_vars=['RP1', 'RP2'], var_name="Pick Position", value_name="Champion")
df_target_team = df_melted[df_melted['Red'].isin(['DetonatioN FocusMe', 'Chiefs Esports Club'])]
pick_counts_rp = pd.crosstab(df_target_team['Champion'], df_target_team['Red'])

fig, axes = plt.subplots(2, 1, figsize=(12, 12), sharex=False)

pick_counts_bp1.plot(kind='bar', stacked=True, ax=axes[0], color=custom_colors)
axes[0].set_ylabel("Frequency")
axes[0].set_xlabel("Champion")
axes[0].set_title("BP1 Picks Frequency by Team")
axes[0].legend(title="Teams", bbox_to_anchor=(1.05, 1), loc='upper left')
axes[0].yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

pick_counts_rp.plot(kind='bar', stacked=True, ax=axes[1], color=custom_colors)
axes[1].set_xlabel("Champion")
axes[1].set_ylabel("Frequency")
axes[1].set_title("RP1-2 Picks Frequency by Team")
axes[1].legend(title="Teams", bbox_to_anchor=(1.05, 1), loc='upper left')
axes[1].yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("champ_picks_stacked.png")
plt.show()
