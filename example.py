from anki_db.ankidb import Ankidb

# Path to Anki db
path = 'testing\\collection.anki2'

# Create new Ankidb object
anki = Ankidb(path=path)

# Table names
print(anki.tables)

# Dump all tables to csv
#anki.to_csv_all(folder='testing')

# Get Review History of a card
reviews = anki.review_history(cardid=1574285327044)
for review in reviews:
    print(review)

# Get number of reviews of a card
count = anki.review_count(cardid=1574285327044)
print(count)

# Get number of reviews for multiple cards
counts = anki.review_counts(cardids=[1574285327044, 1412036486155])
for key, value in counts.items():
    print(key, value)

# Get information on a card
card = anki.card_row(cardid=1574285327044)
print(card)

# Close connection to db
anki.close()
