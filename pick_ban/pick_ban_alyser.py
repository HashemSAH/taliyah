import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


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


champ_stats = defaultdict(lambda: {'wins': 0, 'games': 0})

df[['RP1', 'RP2']] = df['RP1-2'].str.split(',', expand=True)
df[['BP2', 'BP3']] = df['BP2-3'].str.split(',', expand=True)
df[['BP4', 'BP5']] = df['BP4-5'].str.split(',', expand=True)
df['RP1'] = df['RP1'].str.strip()
df['RP2'] = df['RP2'].str.strip()
df['BP3'] = df['BP3'].str.strip()
df['BP2'] = df['BP2'].str.strip()
df['BP4'] = df['BP4'].str.strip()
df['BP5'] = df['BP5'].str.strip()



for _, row in df.iterrows():
    blue_team = [row['BP1'], row['BP2'], row['BP3'],row['BP4'], row['BP5']]
    red_team = [row['RP1'], row['RP2'], row['RP3'], row['RP4'], row['RP5']]
    winner = row['Winner']
    
    # Update games played
    for champ in blue_team + red_team:
        champ_stats[champ]['games'] += 1
    
    # Update wins
    if winner == 1:
        for champ in blue_team:
            champ_stats[champ]['wins'] += 1
    elif winner == 2:
        for champ in red_team:
            champ_stats[champ]['wins'] += 1

# Calculate final winrate
final_winrates = {
    champ: stats['wins'] / stats['games']
    for champ, stats in champ_stats.items()
}

# Convert to DataFrame for display
winrate_df = pd.DataFrame([
    {'champion': champ, 'wins': stats['wins'], 'games': stats['games'], 'winrate': final_winrates[champ]}
    for champ, stats in champ_stats.items()
]).sort_values(by='winrate', ascending=False)

winrate_df = winrate_df.sort_values(by='games', ascending=False).reset_index(drop=True)


winrate_df.to_csv('winrate.csv')




# col = df['BP1']
# teams = df['Blue']  # This is the column with team names


# pick_counts = pd.crosstab(col, teams)

# # Plot stacked bar chart
# pick_counts.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab10')

# # Set plot labels and title
# plt.xlabel("Champion Picks")
# plt.ylabel("Frequency")
# plt.title("Champion Picks Frequency by Team")
# plt.xticks(rotation=45)

# # Optional: Add a legend to indicate teams
# plt.legend(title="Teams", bbox_to_anchor=(1.05, 1), loc='upper left')

# plt.tight_layout()
# plt.savefig("champ_by_team")
# plt.show()


