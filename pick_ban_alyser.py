import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("picks_and_bans_LCP.csv")

col = df['BP1']
teams = df['Blue']  # This is the column with team names

pick_counts = pd.crosstab(col, teams)

# Plot stacked bar chart
pick_counts.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab10')

# Set plot labels and title
plt.xlabel("Champion Picks")
plt.ylabel("Frequency")
plt.title("Champion Picks Frequency by Team")
plt.xticks(rotation=45)

# Optional: Add a legend to indicate teams
plt.legend(title="Teams", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig("champ_by_team")
plt.show()


