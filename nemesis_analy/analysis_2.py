import pandas as pd
import ast
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import seaborn as sns
import numpy as np
import scipy.stats as st


df1 = pd.read_csv('neme_data2.csv')
df2 = pd.read_csv('neme_data2_1.csv')

df = pd.concat([df1, df2], ignore_index=True)

# Create new calculated columns
df['dmg/taken'] = df['Damage_done'] / df['Damage_taken']
df['dmg/min'] = df['Damage_done'] / df['Match_length']
df['dmg/gold_min'] = df['Damage_done'] / (df['Gold_earned'] / df['Match_length'])
df['cs/min'] = (df['Minions_slain'] + df['Monsters_killed']) / df['Match_length']
df['gold/min'] = df['Gold_earned'] / df['Match_length']

# Select numerical features
X = df[['dmg/taken', 'dmg/min', 'dmg/gold_min', 'cs/min', 'Damage share']]

# Function to compute confidence interval
def confidence_interval(series, confidence=0.95):
    n = len(series)
    mean = series.mean()
    std_dev = series.std()
    sem = std_dev / np.sqrt(n)
    ci_lower, ci_upper = st.t.interval(confidence, df=n-1, loc=mean, scale=sem)
    return mean, ci_lower, ci_upper

# Compute statistics for each column
statistics_data = []
for col in X.columns:
    mean, ci_lower, ci_upper = confidence_interval(X[col])
    statistics_data.append([
        mean, 
        X[col].median(), 
        X[col].std(), 
        X[col].max() - X[col].min(), 
        ci_lower, 
        ci_upper])

# Create a DataFrame with the results
statistics_table = pd.DataFrame(statistics_data, 
                                columns=['Average', 'Median', 'Standard Deviation', 'Range', '95% CI Lower', '95% CI Upper'], 
                                index=X.columns)

# Print statistics table
print(statistics_table)
print("\n")

#plt.figure(figsize=(12, 10))

# Define the binary column (Win or Loss)
y = df['Win'].astype(bool)  # Ensure it's boolean

# Loop through each column in X and plot its distribution
for i, column in enumerate(X.columns, 1):
    plt.subplot(2, 3, i)  # 2 rows, 3 columns
    sns.kdeplot(X.loc[y, column], label='Win', fill=True, alpha=0.5)
    sns.kdeplot(X.loc[~y, column], label='Loss', fill=True, alpha=0.5)
    plt.title(f'Distribution of {column}')
    plt.legend()
    plt.tight_layout()

# Show the plots
#plt.show()



def t_test_func(col):
    group_1 = df[df['Win'] == True][col]
    group_2 = df[df['Win'] == False][col]
    
    print(f"Win mean: {group_1.mean():.4f}, False mean : {group_2.mean():.4f}")

    t_stat, p_val = ttest_ind(group_1, group_2, equal_var=False)
    print(f"T-statistic {col}: {t_stat:.4f}, p-value: {p_val:.4f}")

t_test_func('Damage share')
print("\n")
t_test_func('dmg/min')




df['objs_me'] = df['objs_me'].apply(ast.literal_eval)

DRAGON_values = [row['DRAGON'] for row in df[df['Win'] == True]['objs_me'] if 'DRAGON' in row]
DRAGON_values2 = [row['DRAGON'] for row in df[df['Win'] == False]['objs_me'] if 'DRAGON' in row]

t_stat, p_value = st.ttest_ind(DRAGON_values, DRAGON_values2)

print("\n")
print(f"T-statistic Drags: {t_stat}")
print(f"P-value: {p_value}")
print(f"Win mean: {np.mean(DRAGON_values):.4f}, False mean : {np.mean(DRAGON_values2):.4f}")


HORDE_values = [row['HORDE'] for row in df[df['Win'] == True]['objs_me'] if 'HORDE' in row]

HORDE_values2 = [row['HORDE'] for row in df[df['Win'] == False]['objs_me'] if 'HORDE' in row]

t_stat, p_value = st.ttest_ind(HORDE_values, HORDE_values2)

print("\n")
print(f"T-statistic HORDE: {t_stat}")
print(f"P-value: {p_value}")
print(f"Win mean: {np.mean(HORDE_values):.4f}, False mean : {np.mean(HORDE_values2):.4f}")

# plt.boxplot([DRAGON_values, DRAGON_values2], labels=['Win', 'Loss'])
# plt.ylabel('Number of Dragons')
# plt.title('Distribution of Dragons Taken: Win vs Loss')
# plt.grid(True)
#plt.show()


df['gold_me'] = df['gold_me'].apply(ast.literal_eval)

gold_win = df[df['Win'] == True]['gold_me'].apply(pd.Series)
gold_loss = df[df['Win'] == False]['gold_me'].apply(pd.Series)

avg_gold_win = gold_win.mean()
avg_gold_loss = gold_loss.mean()

# plt.figure(figsize=(10, 6))
# plt.plot(avg_gold_win, label="Win", color="blue", linewidth=2)
# plt.plot(avg_gold_loss, label="Loss", color="red", linewidth=2, linestyle="dashed")

# plt.xlabel("Time Intervals")
# plt.ylabel("Average Gold")
# plt.title("Gold Advantage Over Time (Win vs. Loss)")
# plt.legend()
# plt.grid(True)

# plt.show()