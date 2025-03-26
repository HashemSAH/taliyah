import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.ticker as mticker
import seaborn as sns
from adjustText import adjust_text
import numpy as np 
import matplotlib.patches as mpatches

df = pd.read_csv("DFM_picks_and_bans_LCP2025_1.csv")

role_prio = defaultdict(lambda: {'blue_pick_order': [], 'red_pick_order': []})


champ_stats = defaultdict(lambda: {
    'wins': 0, 
    'games': 0, 
    'bans': 0, 
    'pick_order_blue': [],  
    'pick_order_red': []    })

banned_champs = defaultdict(lambda: {'games': 0, 'ban_order_blue': [], 'ban_order_red': []})



# Split columns and clean whitespace
df[['RP1', 'RP2']] = df['RP1-2'].str.split(',', expand=True)
df[['BP2', 'BP3']] = df['BP2-3'].str.split(',', expand=True)
df[['BP4', 'BP5']] = df['BP4-5'].str.split(',', expand=True)

for col in ['RP1', 'RP2', 'RP3', 'RP4', 'RP5', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5']:
    df[col] = df[col].str.strip()

# Initialize counters
n = len(df)
win = 0 

# Iterate through matches
for _, row in df.iterrows():
    blue_team = [row['BP1'], row['BP2'], row['BP3'], row['BP4'], row['BP5']]
    red_team = [row['RP1'], row['RP2'], row['RP3'], row['RP4'], row['RP5']]
    blue_team_bans = [row['BB1'], row['BB2'], row['BB3'], row['BB4'], row['BB5']]
    red_team_bans = [row['RB1'], row['RB2'], row['RB3'], row['RB4'], row['RB5']]
    blue_pos =  [row['BR1'], row['BR2'], row['BR3'], row['BR4'], row['BR5']]
    red_pos = [row['RR1'], row['RR2'], row['RR3'], row['RR4'], row['RR5']]
    
    winner = row['Winner']
    blue_team_name = row['Blue']
    red_team_name = row['Red']



    if blue_team_name == 'DetonatioN FocusMe':
        for i, champ in enumerate(blue_team):    
            champ_stats[champ]['games'] += 1
            champ_stats[champ]['pick_order_blue'].append(i + 1)  # Store blue-side pick order
        for champ in red_team_bans:
            champ_stats[champ]['bans'] += 1
        for i, champ in enumerate(blue_team_bans):
            banned_champs[champ]['games'] += 1
            banned_champs[champ]['ban_order_blue'].append(i + 1) 
        for i, role in enumerate(blue_pos):    
            role_prio[role]['blue_pick_order'].append(i + 1)

        

    if red_team_name == 'DetonatioN FocusMe':
        for i, champ in enumerate(red_team):    
            champ_stats[champ]['games'] += 1
            champ_stats[champ]['pick_order_red'].append(i + 1)  # Store red-side pick order
        for champ in blue_team_bans:
            champ_stats[champ]['bans'] += 1
        for i,champ in enumerate(red_team_bans):
            banned_champs[champ]['games'] += 1
            banned_champs[champ]['ban_order_red'].append(i + 1) 
        for i, role in enumerate(red_pos): 
            role_prio[role]['red_pick_order'].append(i + 1)   

    # Track wins
    if winner == 1 and blue_team_name == 'DetonatioN FocusMe':
        for champ in blue_team:
            champ_stats[champ]['wins'] += 1
        win += 1
    elif winner == 2 and red_team_name == 'DetonatioN FocusMe':
        for champ in red_team:
            champ_stats[champ]['wins'] += 1
        win += 1



final_winrates = {
    champ: stats['wins'] / stats['games'] if stats['games'] > 0 else 0
    for champ, stats in champ_stats.items()
}


roles = pd.DataFrame([
    {
        'role': role,
        'blue_pick_times': stats['blue_pick_order'],
        'red_pick_times': stats['red_pick_order'],
        'avg_blue_pick_times': np.mean(stats['blue_pick_order']),   
        'avg_red_pick_times': np.mean(stats['red_pick_order']),  
        'avg_pick_time': np.mean(stats['blue_pick_order'] + (stats['red_pick_order']))
   
    }
    for role, stats in role_prio.items()
])


roles.to_csv('role_prio_dfm.csv', index=False)

banned_df = pd.DataFrame([
    {
        'champion': champ,
        'games': stats['games'],
        'ban_order_blue': stats['ban_order_blue'],
        'ban_order_red': stats['ban_order_red']       
    }
    for champ, stats in banned_champs.items()
])

banned_df = banned_df.sort_values(by='games', ascending=False).reset_index(drop=True)

banned_df.to_csv('banned_dfm.csv', index=False)

winrate_df = pd.DataFrame([
    {
        'champion': champ,
        'wins': stats['wins'],
        'games': stats['games'],
        'bans': stats['bans'],
        'pick_order_blue': stats['pick_order_blue'],
        'pick_order_red': stats['pick_order_red'],        
        'winrate': final_winrates[champ]
    }
    for champ, stats in champ_stats.items()
])

winrate_df = winrate_df.sort_values(by='games', ascending=False).reset_index(drop=True)

winrate_df.to_csv('winrates_dfm.csv', index=False)


#DFM picks, winrate, bans against them

plt.scatter(winrate_df['games'], winrate_df['winrate'])

# Create a dictionary to store champion names at each (games, winrate) point
points = {}
for i, (xi, yi) in enumerate(zip(winrate_df['games'], winrate_df['winrate'])):
    if (xi, yi) not in points:
        points[(xi, yi)] = []
    points[(xi, yi)].append(i)  # Store the index for each champion

# Function to classify pick order priority
def classify_priority(avg_pick):
    avg_pick = np.mean(avg_pick)
    if avg_pick < 3:
        return "Early"
    elif avg_pick == 3:
        return "Medium"
    else:
        return "Late"

for (xi, yi), indices in points.items():
    sorted_indices = sorted(indices, key=lambda idx: -winrate_df['bans'][idx])

    text_box_lines = []
    for idx in sorted_indices:
        champion_name = winrate_df['champion'][idx]
        bans = winrate_df['bans'][idx]

        # Get Blue and Red pick order priority
        blue_prio = classify_priority(winrate_df['pick_order_blue'][idx]) if winrate_df['pick_order_blue'][idx] else "-"
        red_prio = classify_priority(winrate_df['pick_order_red'][idx]) if winrate_df['pick_order_red'][idx] else "-"

        text_box_lines.append(f"{champion_name} (Bans: {bans}) | Blue: {blue_prio} | Red: {red_prio}")

    # Join all champion names at this point
    text_box = '\n'.join(text_box_lines)
    plt.text(xi, yi + 0.02, text_box, fontsize=9,ha='center', va='bottom', 
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

# Add a dotted line at y = 0.5
plt.axhline(y=0.5, color='green', linestyle='--', linewidth=1)
plt.axhline(y=win/n, color='red', linestyle='--', linewidth=1)

# Set x-axis to only show integers
plt.xticks(range(min(winrate_df['games']), max(winrate_df['games']) + 1))

# Add labels and title
plt.xlabel('Number of Games')
plt.ylabel('Winrate')
plt.title('DFM picks, winrate, bans and pick prio')


def classify_bans(lis):
    avg_pick = np.mean(lis)
    if avg_pick < 3:
        return "First"
    else:
        return "Second"

priority_colors = {
    'Early': 'green',
    'First': 'green',
    'Second': 'red',
    'Late': 'red'
}


#DFM bans

banned_df['blue_bans'] = banned_df['ban_order_blue'].apply(lambda x: sum(1 for i in x if i > 0))
banned_df['red_bans'] = banned_df['ban_order_red'].apply(lambda x: sum(1 for i in x if i > 0))

banned_df['blue_prio'] = banned_df['ban_order_blue'].apply(lambda x: classify_bans(x) if x else "-")
banned_df['red_prio'] = banned_df['ban_order_red'].apply(lambda x: classify_bans(x) if x else "-")

df = banned_df[['champion', 'blue_bans', 'red_bans', 'blue_prio', 'red_prio']]

df.set_index('champion', inplace=True)

ax = df[['blue_bans', 'red_bans']].plot(kind='bar', stacked=True, figsize=(10, 6), color=['#6495ed', '#ff6347'], width=0.3)  # Blue and red colors

for idx, (champion, row) in enumerate(df.iterrows()):
    b = row['blue_prio']
    r = row['red_prio']
    
    text_box = f"Blue Prio: {b}\nRed Prio: {r}"
    
    blue_color = priority_colors.get(b, 'black')  # Default to black if priority is not found
    red_color = priority_colors.get(r, 'black')  # Default to black if priority is not found

    vertical_offset = 0.25 * (1 if idx % 2 == 0 else -1)  # Alternate between positive and negative offset

    if b != "-":
        ax.text(idx, row['blue_bans'] + vertical_offset, 
                f"Blue Prio: {b}", ha='center', va='bottom', fontsize=9, 
                color=blue_color, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    
    if r != "-":
        ax.text(idx, row['blue_bans'] + row['red_bans'] + vertical_offset, 
                f"Red Prio: {r}", ha='center', va='bottom', fontsize=9, 
                color=red_color, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))


plt.title('DFM bans by side')
plt.xlabel('Champion')
plt.ylabel('Number of Bans')
ax.set_xticklabels(df.index, rotation=45)
plt.tight_layout()
#plt.show()
