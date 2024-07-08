
from flask import Flask, request, jsonify
from models import db, Book, Review
import transformers
import torch
from llama_agent_langchain import get_book_summary
from conn import sql_connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_scoped_session
from book_recommender.inference import recommend_books_for_user
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_id = "meta-llama/Meta-Llama-3-8B"

# pipeline = transformers.pipeline("text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto",max_new_tokens=250)
# print(pipeline("Hey how are you doing today?"))

DATABASE_URL = "sqlite+aiosqlite:///./books.db" 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
Session = async_scoped_session(async_session_factory, scopefunc=asyncio.current_task)


# model_id = "meta-llama/Meta-Llama-3-8B"
# pipeline = transformers.pipeline("text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto", max_new_tokens=250)

@app.route('/books', methods=['POST'])
async def add_book():
    async with Session() as session:
        async with session.begin():
            data = request.json
            book = Book(title=data['title'], author=data['author'], genre=data['genre'], year_published=data['year_published'], summary=data['summary'])
            session.add(book)
            logger.info(f"Adding book: {data['title']} by {data['author']}")
        await session.commit()
    logger.info("Book added successfully")
    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/books', methods=['GET'])
def get_all_books():
    logger.info("Fetching all books")
    books = Book.query.all()
    books_json = [{'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'year_published': book.year_published} for book in books]
    logger.info(f"Found {len(books)} books")
    return jsonify(books_json)

@app.route('/books/<int:id>/summary', methods=['GET'])
def get_book_summary(id):
    try:
        book = Book.query.get_or_404(id)
        logger.info(f"Retrieved summary for book ID: {id}")
        return jsonify({'summary': book.summary})
    except Exception as e:
        logger.error(f"Error retrieving summary for book ID: {id}: {e}")
        return jsonify({'error': 'Error retrieving book summary'}), 500

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    try:
        conn = sql_connection()
        input_name = "The Hunger Games"
        book = conn.execute(text("SELECT * FROM books where title='{}'".format(input_name))).fetchone()
        if book is None:
            logger.info(f"Book not found: {input_name}")
            return jsonify({'message': 'Book not found'}), 404
        else:
            reviews = Review.query.filter_by(book_id=book.id).all()

        recommended_books, similarity_scores = recommend_books_for_user(reviews)

        books = []
        if recommended_books is not None:
            logger.info("Generating recommendations")
            for book, score in zip(recommended_books, similarity_scores):
                books.append(book)
        else:
            logger.info("No recommendations found for the given input.")
            return jsonify({'message': 'No recommendations found'}), 404

        return jsonify({'recommended_books': books})
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/generate-summary', methods=['POST'])
def generate_summary():
    # Attempt to generate a book summary based on the provided book name
    try:
        # Extract the book name from the request's JSON body
        content = request.json['content']
        logger.info(f"Received request to generate summary for: {content['book_name']}")

        # Generate the summary for the given book name
        summary = get_book_summary(content["book_name"])
        
        # Return the generated summary
        return jsonify({'summary': summary["text"]})
    except KeyError as e:
        # Log and handle missing book name in the request
        logger.error(f"Missing key in request: {e}")
        return jsonify({'error': 'Missing book name in request'}), 400
    except Exception as e:
        # Log and handle any other errors
        logger.error(f"Error generating summary: {e}")
        return jsonify({'error': 'Error generating summary'}), 500
    

@app.route('/generate-summary', methods=['POST'])
def generate_summary():
    # Attempt to generate a book summary based on the provided book name
    try:
        # Extract the book name from the request's JSON body
        content = request.json['content']
        logger.info(f"Received request to generate summary for: {content['book_name']}")

        # Generate the summary for the given book name
        summary = get_book_summary(content["book_name"])
        
        # Return the generated summary
        return jsonify({'summary': summary["text"]})
    except KeyError as e:
        # Log and handle missing book name in the request
        logger.error(f"Missing key in request: {e}")
        return jsonify({'error': 'Missing book name in request'}), 400
    except Exception as e:
        # Log and handle any other errors
        logger.error(f"Error generating summary: {e}")
        return jsonify({'error': 'Error generating summary'}), 500
    



import logging
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/add-review', methods=['POST'])
def add_review():
    try:
        data = request.json
        new_review = Review(book_id=data['book_id'], user_id=data['user_id'], rating=data['rating'], review_text=data["review_text"])
        db.session.add(new_review)
        db.session.commit()
        logger.info(f"Review added successfully for book ID: {data['book_id']}")
        return jsonify({'message': 'Review added successfully'}), 201
    except SQLAlchemyError as e:
        logger.error(f"Database error while adding review: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Unexpected error while adding review: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/get-reviews/<int:book_id>', methods=['GET'])
def get_reviews(book_id):
    try:
        reviews = Review.query.filter_by(book_id=book_id).all()
        reviews_data = [{'id': review.id, 'user_id': review.user_id, 'rating': review.rating, 'review_text': review.review_text, 'book_id': review.book_id} for review in reviews]
        logger.info(f"Retrieved reviews for book ID: {book_id}")
        return jsonify(reviews_data)
    except SQLAlchemyError as e:
        logger.error(f"Database error while retrieving reviews for book ID {book_id}: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Unexpected error while retrieving reviews for book ID {book_id}: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/delete-review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    try:
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        logger.info(f"Review ID: {review_id} deleted successfully")
        return jsonify({'message': 'Review deleted successfully'}), 204
    except SQLAlchemyError as e:
        logger.error(f"Database error while deleting review ID {review_id}: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Unexpected error while deleting review ID {review_id}: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
    

    
@app.route('/delete-book-reviews/<int:book_id>', methods=['DELETE'])
def delete_reviews_and_books(book_id):
    # Delete all reviews associated with the book
    Review.query.filter_by(book_id=book_id).delete()
    # Delete the book
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book and all associated reviews deleted successfully'}), 204


@app.route('/delete-book/<int:book_id>', methods=['DELETE'])
def delete_book_and_reviews(book_id):
    # Delete all reviews associated with the book
    Review.query.filter_by(book_id=book_id).delete()
    # Delete the book
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book and all associated reviews deleted successfully'}), 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    
    app.run(debug=True)

