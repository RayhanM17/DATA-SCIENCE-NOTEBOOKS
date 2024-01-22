# Define the weights for each sub-criterion for all three hurricanes
wind_weight = 0.5
damage_weight = 0.5

# Calculate the overall scores for each city for each hurricane using the weighted sum method
scores_irma = wind_weight * df['irmaWind'] + damage_weight * (1 - df['irmaDamagePercentage'])
scores_frances = wind_weight * df['francesWind'] + damage_weight * (1 - df['francesDamagePercentage'])
scores_wilma = wind_weight * df['wilmaWind'] + damage_weight * (1 - df['wilmaDamagePercentage'])

# Create a new DataFrame to store the rankings for each hurricane
rankings_irma = pd.DataFrame({'City': df['damagedCity'], 'Score': scores_irma})
rankings_frances = pd.DataFrame({'City': df['damagedCity'], 'Score': scores_frances})
rankings_wilma = pd.DataFrame({'City': df['damagedCity'], 'Score': scores_wilma})

# Rank the cities for each hurricane based on their scores
rankings_irma = rankings_irma.sort_values(by='Score', ascending=False)
rankings_irma['Rank'] = rankings_irma['Score'].rank(ascending=False)
rankings_frances = rankings_frances.sort_values(by='Score', ascending=False)
rankings_frances['Rank'] = rankings_frances['Score'].rank(ascending=False)
rankings_wilma = rankings_wilma.sort_values(by='Score', ascending=False)
rankings_wilma['Rank'] = rankings_wilma['Score'].rank(ascending=False)

# Merge the rankings for all three hurricanes into a single DataFrame
rankings_combined = pd.merge(rankings_irma, rankings_frances, on='City')
rankings_combined = pd.merge(rankings_combined, rankings_wilma, on='City')

# Calculate the sum of the ranks for each city across all three hurricanes
rankings_combined['Rank_Total'] = rankings_combined['Rank_x'] + rankings_combined['Rank_y'] + rankings_combined['Rank']

# Sort the cities based on their total rank
rankings_combined = rankings_combined.sort_values(by='Rank_Total', ascending=True)
rankings_combined['Overall_Rank'] = rankings_combined['Rank_Total'].rank(ascending=True)

# Select only the columns that you want in the final output
final_rankings = rankings_combined[['City', 'Rank_Total', 'Overall_Rank']]

# Display the final rankings
print(final_rankings)