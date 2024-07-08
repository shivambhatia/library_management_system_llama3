from langchain_community.utilities import SerpAPIWrapper
from transformers import pipeline
from models import Book, Review
from langchain import PromptTemplate
from conn import sql_connection
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Book, Review

# Assuming the Book and Review models are defined somewhere above this snippet
# and your database URI is correctly set in 'your_database_uri'
engine = create_engine('sqlite:///books.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

"""
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Book, Review

# Assuming the Book and Review models are defined somewhere above this snippet
# and your database URI is correctly set in 'your_database_uri'
engine = create_engine('sqlite:///books.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_book_summary(book_name):
    db: Session = SessionLocal()
    try:
        # Query for the book details using ORM
        book_details = db.query(Book).filter(Book.title == book_name).first()
        if book_details:
            # Directly access reviews from the book_details object
            reviews_list = db.query(Review).filter(Review.book_id == book_details.id).all()
            
            # Assuming you have a way to load and use your LLaMA model correctly
            # This part of the code needs to be adjusted based on how you use the model
            model_id = "meta-llama/Meta-Llama-3-8B"
            book_info = {
                "id": book_details.id,
                "title": book_details.title,
                "author": book_details.author,
                "reviews": reviews_list
            }
            # Construct and format your prompt here
            # Ensure you have the correct method to format and send this prompt to your model
            
            # Example placeholder for model prediction
            prediction = "This is where the model prediction would go."
        else:
            print("Book not found.")
    except Exception as e:
        print('Error:', e)
    finally:
        db.close()
 
    return "Summary of the book is:"


"""

def get_book_summaryy(book_name):
    db: Session = SessionLocal()
    try:
        # Query for the book details using ORM
        book_details = db.query(Book).filter(Book.title == book_name).first()
        if book_details:
            # Directly access reviews from the book_details object
            reviews_list = db.query(Review).filter(Review.book_id == book_details.id).all()
            
            # Assuming you have a way to load and use your LLaMA model correctly
            # This part of the code needs to be adjusted based on how you use the model
            model_id = "meta-llama/Meta-Llama-3-8B"
            book_info = {
                "id": book_details.id,
                "title": book_details.title,
                "author": book_details.author,
                "reviews": reviews_list
            }
            # Construct and format your prompt here
            # Ensure you have the correct method to format and send this prompt to your model
            
            # Step 4: Construct the Dictionary
            book_info = {
                "id": book_details.id,
                "title": book_details.title,
                "author": book_details.author,
                "reviews": reviews_list
            }
            # create the prompt
            prompt_template: str = """/
            You are a experienced Book Summarizer .Provide short and precise summary responses to the following/ 
            question: {question}. Based on user ratings and review text build a comprehensive summary of the book.
            """

            prompt = PromptTemplate.from_template(template=prompt_template)

            # format the prompt to add variable values
            prompt_formatted_str: str = prompt.format(
                question=book_info)

            # instantiate the OpenAI intance
            llama_pipeline = pipeline("text-generation", model=model_id,  max_new_tokens=250)

            # make a prediction
            prediction = llama_pipeline(prompt_formatted_str)
            return {"text":prediction["output"]}

        else:
            return {"text":"Book not found.","status_code":400}
    except Exception as e:
        print('Error:', e)
    finally:
        db.close()
        
        




