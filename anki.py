import pandas as pd
import pykakasi
import genanki

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

# Define the model for Anki cards with furigana overlay
my_model = genanki.Model(
  1607392319,
  'Furigana Model',
  fields=[
    {'name': 'Kanji'},
    {'name': 'Furigana'},
    {'name': 'Meaning'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Kanji}}',
      'afmt': '{{furigana:Kanji}}<br>{{Meaning}}',
    },
  ],
  css="""
    .card {
      font-family: arial;
      font-size: 20px;
      text-align: center;
      color: black;
      background-color: white;
    }
    ruby {
      ruby-position: over;
    }
  """
)

# Create a new Anki deck
my_deck = genanki.Deck(
  2059400110,
  'N4 Kanji Vocabulary')

# Add notes to the deck
for index, row in df.iterrows():
    note = genanki.Note(
        model=my_model,
        fields=[row['Kanji'], row['Furigana'], row['Meaning']]
    )
    my_deck.add_note(note)

# Save the deck to a file
output_file_path = 'N4_Kanji_Vocabulary.apkg'
genanki.Package(my_deck).write_to_file(output_file_path)

print(f"Anki deck has been exported to {output_file_path}"