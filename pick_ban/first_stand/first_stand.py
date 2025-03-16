import pandas as pd
from collections import defaultdict

df = pd.read_csv('picks_and_bans_First_Stand_2025.csv')

target_team = "Karmine Corp"
team = target_team.split(' ')[0]
champ_stats = defaultdict(lambda: {'wins': 0, 'games': 0})

# Split RP1-2, BP2-3, BP4-5 columns
df[['RP1', 'RP2']] = df['RP1-2'].str.split(',', expand=True)
df[['BP2', 'BP3']] = df['BP2-3'].str.split(',', expand=True)
df[['BP4', 'BP5']] = df['BP4-5'].str.split(',', expand=True)

# Strip whitespace
for col in ['RP1', 'RP2', 'RP3', 'RP4', 'RP5', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5']:
    df[col] = df[col].str.strip()

# Loop through rows
for _, row in df.iterrows():
    blue_team_name = row['Blue']
    red_team_name = row['Red']  
    winner = row['Winner']  # 1 = Blue won, 2 = Red won

    blue_champs = [row['BP1'], row['BP2'], row['BP3'], row['BP4'], row['BP5']]
    red_champs = [row['RP1'], row['RP2'], row['RP3'], row['RP4'], row['RP5']]

    # Only include games where target team played
    if target_team == blue_team_name:
        for champ in blue_champs:
            champ_stats[champ]['games'] += 1
            if winner == 1:
                champ_stats[champ]['wins'] += 1

    elif target_team == red_team_name:
        for champ in red_champs:
            champ_stats[champ]['games'] += 1
            if winner == 2:
                champ_stats[champ]['wins'] += 1

# Compute winrates
final_winrates = {
    champ: stats['wins'] / stats['games'] if stats['games'] > 0 else 0
    for champ, stats in champ_stats.items()
}

# Create final DataFrame
winrate_df = pd.DataFrame([
    {
        'champion': champ,
        'wins': stats['wins'],
        'games': stats['games'],
        'winrate': round(final_winrates[champ] * 100, 1)
    }
    for champ, stats in champ_stats.items()
])


winrate_df = winrate_df.sort_values('games', ascending = False)
# Save to CSV
winrate_df.to_csv(f"winrates_{team}.csv", index=False)