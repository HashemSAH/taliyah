import pandas as pd
import ast
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import seaborn as sns

df1 = pd.read_csv('neme_data2.csv')
df2 = pd.read_csv('neme_data2_1.csv')

df = pd.concat([df1, df2], ignore_index=True)



df['objs_me'] = df['objs_me'].apply(ast.literal_eval)



DRAGON_values = [row['DRAGON'] for row in df[df['Win'] == True]['objs_me'] if 'DRAGON' in row]
DRAGON_values2 = [row['DRAGON'] for row in df[df['Win'] == False]['objs_me'] if 'DRAGON' in row]
plt.boxplot([DRAGON_values, DRAGON_values2], labels=['Win', 'Loss'])
plt.ylabel('Number of Dragons')
plt.title('Distribution of Dragons Taken: Win vs Loss')
plt.grid(True)
plt.show()

print(DRAGON_values)

# df['gold_me'] = df['gold_me'].apply(ast.literal_eval)
# df['xp_me'] = df['xp_me'].apply(ast.literal_eval)  # Make sure this column exists

# # Separate wins and losses
# gold_win = df[df['Win'] == True]['gold_me'].apply(pd.Series)
# gold_loss = df[df['Win'] == False]['gold_me'].apply(pd.Series)
# xp_win = df[df['Win'] == True]['xp_me'].apply(pd.Series)
# xp_loss = df[df['Win'] == False]['xp_me'].apply(pd.Series)

# # Compute averages
# avg_gold_win = gold_win.mean()
# avg_gold_loss = gold_loss.mean()
# avg_xp_win = xp_win.mean()
# avg_xp_loss = xp_loss.mean()

# # Plot
# fig, ax1 = plt.subplots(figsize=(10, 6))

# # Plot XP on left y-axis
# ax1.plot(avg_xp_win, label='XP - Wins', color='green', linestyle='--')
# ax1.plot(avg_xp_loss, label='XP - Losses', color='red', linestyle='--')
# ax1.set_ylabel('Average XP')
# ax1.set_xlabel('Time (snapshot index)')
# ax1.legend(loc='upper left')
# ax1.grid(True)

# # Plot Gold on right y-axis
# ax2 = ax1.twinx()
# ax2.plot(avg_gold_win, label='Gold - Wins', color='blue')
# ax2.plot(avg_gold_loss, label='Gold - Losses', color='yellow')
# ax2.set_ylabel('Average Gold')
# ax2.legend(loc='upper right')

# plt.title('Average Gold and XP Over Time: Wins vs Losses')
# plt.tight_layout()
# plt.show()

def t_test_func(col):
    group_1 = df[df[col] == True]['Win']
    group_2 = df[df[col] == False]['Win']
    
    print(f"True mean: {group_1.mean():.4f}, False mean : {group_2.mean():.4f}")

    t_stat, p_val = ttest_ind(group_1, group_2, equal_var=False)
    print(f"T-statistic: {t_stat:.4f}, p-value: {p_val:.4f}")