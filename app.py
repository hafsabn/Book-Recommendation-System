from scripts.preprocessing import load_and_prepare_data
from scripts.fp_growth import get_book_recommendations
import streamlit as st
from PIL import Image
import joblib
import os

# Set page config
st.set_page_config(page_title="Book Recommendation System", page_icon="📚", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .title {
        font-size: 5rem;
        font-weight: bold;
        text-align: center;
        color: #6A5ACD; 
        margin-top: 0;
        margin-bottom: 1rem;
    }

    .container {
        display: flex;
        justify-content: space-between;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    
    .left {
        width: 49%;
    }
    
    .right {
        width: 49%;
        display: flex;
        flex-direction: column;
    }

    div[data-baseweb="select"] {
        color: black;
        border-radius: 0.25rem;
        border: 2px solid black;
        text-align: center;
        background-color: #white;
    }

    .recommended-books-title {
        text-decoration: underline;
    }

    div[data-testid="stButton"] > button {
        background-color: #F9F16F;
        color: black;
        padding: 0.8rem 4rem;
        font-size: 1.4rem;
        border-radius: 0.5rem;
        border: 2px solid black;
        cursor: pointer;
        margin-left: 35%;
        transition: all 0.3s ease; 
    }
    
    div[data-testid="stButton"] > button:hover {
        background-color: #F9F16F;
        border-color: black;
        color: black; 
    }

    .st-emotion-cache-1ogg8jh:focus:not(:active) {
        color: black;
    }

    div[data-testid="stButton"] > button[disabled] {
        background-color: #d3d3d3;  
        color: #747878;
        cursor: not-allowed;
        border-radius: 0.5rem;
    }
     
    div[data-testid="stButton"] > button[disabled]:hover {
        color: #747878;
    }

    div[data-testid="stButton"] > button:active {
        background-color: #F9F16F;
        border-color: black;
        color: black;
        transform: scale(0.98);
    }

    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }

    .recommended-books {
        display: flex;
        justify-content: flex-start;
        flex-wrap: wrap;
        flex-direction: row;
        gap: 10px;
    }

    .book-box {
        padding: 2px;
        border-radius: 8px;
        width: 200px;
        text-align: center;
    }

    .recommended-books img {
        width: 100%;
        border-radius: 8px;
    }

    .book-title {
        font-size: 1rem;
        font-weight: bold;
        text-align: left;
        margin-top: 2px;
        margin-bottom: 2px;
    }

    .book-author {
        text-align: left;
        font-size: 0.8rem;
        margin-top: 2px;
        margin-bottom: 2px;
        color: #747878;
    }
     
    @media (max-width: 768px) {
        .title {
            font-size: 2rem;
        }

        .container {
            flex-direction: column;
            align-items: center;
        }

        .left, .right {
            width: 100%;
            margin-bottom: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_data():
    return load_and_prepare_data()

# Load model data
model_path = os.path.join('notebooks', '04-models', 'fp_growth_model.pkl')
model_data = joblib.load(model_path)

# Extract data from model data
books_in_rules = model_data['books_in_rules']
transactions_with_titles = model_data['transactions_with_titles']
book_titles = model_data['book_titles']
rules = model_data['rules']

def main():
    # Header
    st.markdown('<h1 class="title">Discover Your Next Read</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 3])

    with col1:
        image = Image.open("figures/recommendation_books_ssytem_image.png")
        st.image(image, use_column_width=True)

    with col2:
        selected_book = st.selectbox("", ["Pick a book you loved"] +  [book for book in books_in_rules], index=0)

        # Load data
        books_df = load_data()
    
        if selected_book == "Pick a book you loved":
            search_button_disabled = True
        else:
            search_button_disabled = False
    
        # Book recommendation interface
        if st.button("Recommend", disabled=search_button_disabled):

            # Get book recommendations
            recommendations = get_book_recommendations(selected_book, rules, books_df)
            book_list = []

            if recommendations is not None:
                st.markdown('<div class="recommended-books-title">Books You\'ll Love: </div>', unsafe_allow_html=True)
                for i, (_, row) in enumerate(recommendations.iterrows()):
                    book_component = f'''
                        <div class="book-box">
                            <img src="{row["Image-URL-M"]}" alt="{row["Book-Title"]}" />
                            <p class="book-title">
                                {row["Book-Title"]}
                            </p>
                            <p class="book-author">
                                {row["Book-Author"]}
                            </p>
                        </div>'''
                    book_list.append(book_component)
                st.markdown('<div class="recommended-books">' + ''.join(book_list) + '</div>', unsafe_allow_html=True)
            else:
                st.warning("No recommendations found for this book.")
    
if __name__ == "__main__":
    main()
