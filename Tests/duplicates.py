import pandas as pd

csv_file = 'mappings/Makemodern_deduped.csv'
pd.set_option('display.max_rows', None)  # <-- show ALL rows

df = pd.read_csv(csv_file)
duplicates = df[df.duplicated(subset='code', keep=False)]

if duplicates.empty:
    print("✅ No duplicates found.")
else:
    print("⚠️ Duplicate codes found:")
    print(duplicates.sort_values('code'))
