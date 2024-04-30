import pandas as pd

df = pd.read_csv('merged_form2data.csv')
df.head()

# keep only those rows with missing values for all columns after the first two columns
df = df[df.iloc[:, 2:].isnull().all(1)]
df.head
# Rename 'Proposal' to 'Proposal.No.'
df.rename(columns={'Proposal': 'Proposal.No.'}, inplace=True)
# Keep only 'proposal.no.' column
df = df[['Proposal.No.']]
df.head()
df.to_csv('unique_form2_missed.csv')