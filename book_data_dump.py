import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Book,Review
from sqlalchemy import text
import random

# Positive review samples
positive_samples = [
    "I absolutely loved this book! A must-read.",
    "This book was fantastic, couldn't put it down!",
    "A great read from start to finish.",
    "Engaging and well-written, highly recommend.",
    "An amazing story with memorable characters.",
    "Beautifully written and deeply moving.",
    "A masterpiece that I will read again.",
    "Simply brilliant. One of the best books I've read.",
    "A captivating story that kept me hooked.",
    "Thoroughly enjoyed this book, excellent plot.",
    "Great writing, and a fantastic plot.",
    "The characters were so relatable and well-developed.",
    "An incredible book with a powerful message.",
    "Stunning prose and an unforgettable story.",
    "A truly remarkable book, very inspiring.",
    "A perfect blend of suspense and emotion.",
    "I was completely engrossed in this book.",
    "Highly engaging and thought-provoking.",
    "One of my all-time favorites.",
    "An extraordinary book with a compelling plot.",
    "A fascinating read with a lot of depth.",
    "This book exceeded my expectations.",
    "An enchanting tale that I loved.",
    "A superbly written book with a great story.",
    "A wonderful book that I highly recommend.",
    "An unforgettable reading experience.",
    "A beautifully crafted story.",
    "A delightful book that I enjoyed immensely.",
    "An excellent read with great character development.",
    "A riveting story that I couldn't put down.",
    "A book that stays with you long after you finish it.",
    "A truly beautiful story.",
    "An exceptional book that I loved.",
    "A perfect book for anyone who loves a good story.",
    "A highly entertaining and well-written book.",
    "A thought-provoking and moving story.",
    "An incredibly well-told story.",
    "A wonderful read from beginning to end.",
    "A great book with a powerful message.",
    "A fantastic book that I thoroughly enjoyed.",
    "A must-read for anyone who loves books.",
    "A beautifully written book with an amazing story.",
    "A heartwarming and inspiring book.",
    "An amazing book that I highly recommend.",
    "A book that is hard to put down.",
    "A beautifully crafted and deeply moving story.",
    "A brilliant book with a captivating plot.",
    "An exceptional read that I couldn't put down.",
    "A wonderful story that I will read again.",
    "A powerful and unforgettable book.",
    "An inspiring book that I loved.",
    "A great book that I highly recommend.",
    "An engrossing and thought-provoking read.",
    "A beautifully written and engaging story.",
    "A book that I couldn't stop reading.",
    "A superb book with an excellent story.",
    "A truly captivating book.",
    "A highly recommended read.",
    "An outstanding book with a great plot.",
    "A wonderful and inspiring book.",
    "A beautifully written and deeply moving story.",
    "A brilliant and engaging book.",
    "An unforgettable book with a powerful message.",
    "A must-read for everyone.",
    "A great book with a compelling story.",
    "An excellent read with a lot of depth.",
    "A captivating and thought-provoking book.",
    "A beautiful story that I will cherish.",
    "A wonderful and entertaining book.",
    "An inspiring and moving book.",
    "A book that I loved from start to finish.",
    "A fantastic and unforgettable read.",
    "An amazing book with a powerful story.",
    "A beautifully written and inspiring book.",
    "A truly exceptional book.",
    "A great read with a lot of depth.",
    "A captivating and unforgettable story.",
    "A brilliant book that I highly recommend.",
    "An outstanding and inspiring read.",
    "A wonderful and thought-provoking book.",
    "A book that I couldn't put down.",
    "A great book with an amazing story.",
    "An inspiring and unforgettable read.",
    "A beautifully written and captivating story.",
    "An excellent book that I highly recommend.",
    "A thought-provoking and engaging book.",
    "A wonderful and inspiring read.",
    "A book that I will read again and again.",
    "A fantastic and captivating book.",
    "An amazing and unforgettable story.",
    "A beautifully written and inspiring read.",
    "A truly exceptional and inspiring book.",
    "A great read that I thoroughly enjoyed.",
    "An outstanding book with a lot of depth.",
    "A captivating and inspiring story.",
    "A brilliant book with a lot of depth.",
    "An inspiring and thought-provoking read.",
    "A wonderful and engaging book.",
    "A book that I couldn't put down.",
    "A great book with a powerful story.",
    "An amazing and unforgettable read."
]

# Neutral review samples
neutral_samples = [
    "The book was okay, not too bad but not great either.",
    "It was an average read, nothing special.",
    "The story was decent but didn't stand out.",
    "An alright book, but I've read better.",
    "It was fine, just not very memorable.",
    "An average story with some good moments.",
    "It was a decent read, but not very engaging.",
    "The book was okay, but I wouldn't read it again.",
    "An average book with a predictable plot.",
    "It was an okay book, but it didn't wow me.",
    "The story was okay, but a bit slow.",
    "An average read, with some good parts.",
    "The book was fine, but not very exciting.",
    "An okay read, but nothing special.",
    "The story was alright, but not very memorable.",
    "An average book with some good writing.",
    "It was okay, but I've read better.",
    "The book was decent, but not great.",
    "An okay story, but not very engaging.",
    "It was an alright read, but not very memorable.",
    "The book was fine, but not very exciting.",
    "An average story with some good parts.",
    "It was okay, but not very memorable.",
    "An alright book, but I've read better.",
    "The story was decent, but not very engaging.",
    "It was fine, but not very exciting.",
    "An average book with some good writing.",
    "It was okay, but not very memorable.",
    "The book was alright, but not very engaging.",
    "An average story with some good moments.",
    "It was an okay read, but not very memorable.",
    "The book was fine, but not very exciting.",
    "An average read, with some good parts.",
    "It was okay, but not very engaging.",
    "An alright book, but I've read better.",
    "The story was decent, but not very memorable.",
    "It was fine, but not very exciting.",
    "An average book with some good writing.",
    "It was okay, but not very memorable.",
    "The book was alright, but not very exciting.",
    "An average story with some good moments.",
    "It was an okay read, but not very engaging.",
    "The book was fine, but not very exciting.",
    "An average read, with some good parts.",
    "It was okay, but not very memorable.",
    "An alright book, but not very exciting.",
    "The story was decent, but not very engaging.",
    "It was fine, but not very memorable.",
    "An average book with some good writing.",
    "It was okay, but not very exciting.",
    "The book was alright, but not very memorable.",
    "An average story with some good moments.",
    "It was an okay read, but not very exciting.",
    "The book was fine, but not very engaging.",
    "An average read, with some good parts.",
    "It was okay, but not very memorable.",
    "An alright book, but not very engaging.",
    "The story was decent, but not very exciting.",
    "It was fine, but not very memorable.",
    "An average book with some good writing.",
    "It was okay, but not very exciting.",
    "The book was alright, but not very engaging.",
    "An average story with some good moments.",
    "It was an okay read, but not very memorable.",
    "The book was fine, but not very exciting.",
    "An average read, with some good parts.",
    "It was okay, but not very engaging.",
    "An alright book, but not very memorable.",
    "The story was decent, but not very exciting.",
    "It was fine, but not very memorable.",
    "An average book with some good writing.",
    "It was okay, but not very exciting.",
    "The book was alright, but not very memorable.",
    "An average story with some good moments.",
    "It was an okay read, but not very exciting.",
    "The book was fine, but not very engaging.",
    "An average read, with some good parts.",
    "It was okay, but not very memorable.",
    "An alright book, but not very engaging.",
    "The story was decent, but not very exciting.",
    "It was fine, but not very memorable.",
    "An average book with some good writing.",
    "It was okay, but not very exciting.",
    "The book was alright, but not very memorable.",
    "An average story with some good moments.",
    "It was an okay read, but not very engaging.",
    "The book was fine, but not very exciting.",
    "An average read, with some good parts.",
    "It was okay, but not very memorable.",
    "An alright book, but not very exciting."
]

# Negative review samples
negative_samples = [
    "I didn't like this book at all.",
    "The story was boring and poorly written.",
    "A waste of time, not recommended.",
    "This book was very disappointing.",
    "I couldn't finish it, it was so bad.",
    "Terrible book, don't bother reading.",
    "The plot was weak and uninteresting.",
    "Very poorly written, not enjoyable.",
    "A big letdown, wouldn't recommend.",
    "One of the worst books I've read.",
    "Not worth reading, very dull.",
    "Disappointing and poorly written.",
    "The story was confusing and boring.",
    "I didn't enjoy this book at all.",
    "A poorly written and boring book.",
    "This book was a huge letdown.",
    "The characters were flat and uninteresting.",
    "The plot was predictable and boring.",
    "A very disappointing book.",
    "I couldn't get into this book at all.",
    "A boring and poorly written book.",
    "This book was a big letdown.",
    "The story was dull and uninteresting.",
    "Very disappointing and poorly written.",
    "A waste of time, not recommended.",
    "I didn't like this book at all.",
    "The plot was boring and predictable.",
    "This book was very disappointing.",
    "A poorly written and boring book.",
    "The characters were uninteresting and flat.",
    "I couldn't finish this book, it was so bad.",
    "Terrible book, don't bother reading.",
    "The plot was weak and boring.",
    "Very poorly written, not enjoyable.",
    "A big letdown, wouldn't recommend.",
    "One of the worst books I've read.",
    "Not worth reading, very dull.",
    "Disappointing and poorly written.",
    "The story was confusing and boring.",
    "I didn't enjoy this book at all.",
    "A poorly written and boring book.",
    "This book was a huge letdown.",
    "The characters were flat and uninteresting.",
    "The plot was predictable and boring.",
    "A very disappointing book.",
    "I couldn't get into this book at all.",
    "A boring and poorly written book.",
    "This book was a big letdown.",
    "The story was dull and uninteresting.",
    "Very disappointing and poorly written.",
    "A waste of time, not recommended.",
    "I didn't like this book at all.",
    "The plot was boring and predictable.",
    "This book was very disappointing.",
    "A poorly written and boring book.",
    "The characters were uninteresting and flat.",
    "I couldn't finish this book, it was so bad.",
    "Terrible book, don't bother reading.",
    "The plot was weak and boring.",
    "Very poorly written, not enjoyable.",
    "A big letdown, wouldn't recommend.",
    "One of the worst books I've read.",
    "Not worth reading, very dull.",
    "Disappointing and poorly written.",
    "The story was confusing and boring.",
    "I didn't enjoy this book at all.",
    "A poorly written and boring book.",
    "This book was a huge letdown.",
    "The characters were flat and uninteresting.",
    "The plot was predictable and boring.",
    "A very disappointing book.",
    "I couldn't get into this book at all.",
    "A boring and poorly written book.",
    "This book was a big letdown.",
    "The story was dull and uninteresting.",
    "Very disappointing and poorly written.",
    "A waste of time, not recommended.",
    "I didn't like this book at all.",
    "The plot was boring and predictable.",
    "This book was very disappointing.",
    "A poorly written and boring book.",
    "The characters were uninteresting and flat.",
    "I couldn't finish this book, it was so bad.",
    "Terrible book, don't bother reading.",
    "The plot was weak and boring.",
    "Very poorly written, not enjoyable.",
    "A big letdown, wouldn't recommend.",
    "One of the worst books I've read.",
    "Not worth reading, very dull."
]

# Load CSV files
book_tags_df = pd.read_csv('book_recommender/data/book_tags.csv')
books_df = pd.read_csv('book_recommender/data/books.csv')[['book_id', 'authors', 'original_publication_year', 'original_title']]
tags_df = pd.read_csv('book_recommender/data/tags.csv')
ratings_df = pd.read_csv('book_recommender/data/ratings.csv')

# Merge book_tags with tags to get tag names
book_tags_merged = pd.merge(book_tags_df, tags_df, on='tag_id', how='left')

# Merge books with book_tags_merged to get all book information including tags
books_with_tags = pd.merge(books_df, book_tags_merged, left_on='book_id', right_on='goodreads_book_id', how='left')

# Select and rename columns for the book information DataFrame
book_information_df = books_with_tags[['book_id', 'authors', 'original_publication_year', 'original_title', 'tag_name']]
book_information_df.rename(columns={'tag_name': 'tags'}, inplace=True)

# The ratings DataFrame is already in the desired format, so we can use it directly
book_ratings_df = ratings_df[['user_id', 'book_id', 'rating']]



# Step 1: Aggregate tags for each book into a single entry
tags_grouped = book_information_df.groupby('book_id')['tags'].apply(lambda x: '-'.join(x.dropna())).reset_index()

# Step 2: Merge the aggregated tags with the original book_information_df to include additional columns
final_df = pd.merge(book_information_df.drop('tags', axis=1).drop_duplicates('book_id'), tags_grouped, on='book_id', how='left')

# Ensure only the desired columns are included in the final DataFrame
final_df = final_df[['book_id', 'authors', 'original_publication_year', 'original_title', 'tags']]
# Drop rows with any null values in the specified columns
final_df.dropna(subset=['book_id', 'authors', 'original_publication_year', 'original_title', 'tags'], inplace=True)
final_df['summary'] = 'summary'
# print("Final DataFrame with Additional Columns and Consolidated Tags:")
print(final_df.head())


# Step 0: Setup database connection and session
DATABASE_URI = 'sqlite:///books.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# # # Step 1: Dump book_ratings_df into the database

with engine.connect() as conn:
    # Delete all rows in the Book table
    #conn.execute(text("DELETE FROM books;"))
    conn.execute(text("DELETE FROM reviews;"))
    # Reset the auto-incremented ID sequence (if applicable)
    # Commit the transaction
    conn.commit()
#Step 2: Dump final_df into the database
# count=0
# for index, row in final_df.iterrows():
#     print("Book id count",row['book_id'])
#     book_info = Book(id=80980990, author=row['authors'],
#                                 year_published=row['original_publication_year'],
#                                 title=row['original_title'], genre=row['tags'],summary=row["summary"])

#     session.add(book_info)
#     break
    

# Fetch data from Review table and show top 5 rows

# Commit the session to save changes and close the session

for index, row in book_ratings_df.iterrows():
    if row['rating'] == 1:
        new_comment = random.choice(negative_samples)
    elif row['rating'] in [2, 3]:
        new_comment = random.choice(neutral_samples)
    elif row['rating'] in [4, 5]:
        new_comment = random.choice(positive_samples)
    
    book_rating = Review(user_id=row['user_id'], book_id=row['book_id'], rating=row['rating'],review_text=new_comment)
    session.add(book_rating)

session.commit()
session.close()

#print("Data successfully loaded into the database.")