import pandas as pd
import pykakasi

# Load the CSV file
file_path = 'N4 Kanji _ Vocabulary.csv'
df = pd.read_csv(file_path)

# Initialize pykakasi converter
kks = pykakasi.kakasi()

# Define a function to add furigana
def add_furigana(row):
    kanji = row['japanese/__text']
    meaning = row['text/__text']
    
    # Check for missing values
    if pd.isna(kanji):
        kanji = ''
    if pd.isna(meaning):
        meaning = ''
    
    meaning = meaning.split('/', 1)[-1].strip() if '/' in meaning else meaning
    
    # Generate furigana using pykakasi
    result = kks.convert(kanji)
    furigana = ''.join([item['hira'] for item in result])
    
    return pd.Series([kanji, furigana, meaning])

# Apply the function to each row
df[['Kanji', 'Furigana', 'Meaning']] = df.apply(add_furigana, axis=1)

# Drop the original columns
df = df.drop(columns=['japanese/_name', 'japanese/__text', 'text/_name', 'text/__text'])

# Save the cleaned data to a new CSV file
output_file_path = 'Anki_Formatted_Vocabulary_With_Furigana.csv'
df.to_csv(output_file_path, index=False)

# Display the dataframe (for debugging purposes if needed)
print(df.head())