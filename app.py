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
    body {
        background-color: white;
    }
    .title {
        font-size: 5rem;
        font-weight: bold;
        text-align: center;
        color: #6A5ACD; 
        margin-top: 0;
        margin-bottom: 1rem;
    }

    /* Large Screen Layout */
    .container {
        display: flex;
        justify-content: space-between;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    
    /* Left part (Image container) */
    .left {
        width: 48%;
    }
    
    /* Right part (Dropdown + Button) */
    .right {
        width: 48%;
        display: flex;
        flex-direction: column;
    }

    div[data-baseweb="select"] {
        font-size: 1.2rem;
        border-color: #6A5ACD;
    }

    div[data-testid="stButton"] > button {
        background-color: #6A5ACD;
        color: white;
        padding: 0.5rem 1rem;
        font-size: 1.2rem;
        border-radius: 0.25rem;
        margin-top: 1rem;
    }

    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }

    .recommended-books {
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
        overflow-x: auto;
        margin-top: 2rem;
    }

    .recommended-books div {
        margin-right: 1rem;
        text-align: center;
    }

    .recommended-books img {
        width: 150px;
        height: 220px;
        object-fit: cover;
        border-radius: 8px;
        width: 100%;
        max-width: 200px;
        height: auto;
        margin-bottom: 1rem;
    }

    .book-title {
        font-size: 1rem;
        font-weight: bold;
        text-align: center;
    }
     
    /* Responsive Design (Mobile view) */
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

        /* Make the recommended books grid fit smaller screens */
        .recommended-books {
            grid-template-columns: repeat(2, 1fr);
            flex-direction: column;
            align-items: center;
        }

        .recommended-books div {
            margin-bottom: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         font-weight: bold;
#         color: #1E3D59;
#         text-align: center;
#         margin-bottom: 2rem;
#         text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
#     }
#     .sub-header {
#         font-size: 1.8rem;
#         color: #1E3D59;
#         margin-bottom: 1rem;
#         border-bottom: 2px solid #FF6E40;
#         padding-bottom: 0.5rem;
#     }
#     .stat-box {
#         background-color: #F5F0E1;
#         border-radius: 10px;
#         padding: 1.5rem;
#         text-align: center;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#         transition: transform 0.3s ease;
#     }
#     .stat-box:hover {
#         transform: translateY(-5px);
#     }
#     .stat-number {
#         font-size: 2.5rem;
#         font-weight: bold;
#         color: #FF6E40;
#         margin-bottom: 0.5rem;
#     }
#     .stat-label {
#         font-size: 1.2rem;
#         color: #1E3D59;
#         text-transform: uppercase;
#     }
#     .stButton>button {
#         background-color: #FF6E40;
#         color: white;
#         font-weight: bold;
#         padding: 0.5rem 1rem;
#         border-radius: 5px;
#         border: none;
#         transition: background-color 0.3s ease;
#     }
#     .stButton>button:hover {
#         background-color: #E85A3A;
#     }
#     .stSelectbox {
#         color: #1E3D59;
#     }
#     .book-image {
#         width: 100%;
#         max-width: 200px;
#         height: auto;
#         margin-bottom: 1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

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
        image = Image.open("rapport/final-df.png")
        st.image(image, use_column_width=True)

    with col2:
        selected_book = st.selectbox("Select a book for recommendations:", books_in_rules)

        # Load data
        books_df = load_data()
    
        # Book recommendation interface
    
        if st.button("Get Recommendations"):
            recommendations = get_book_recommendations(selected_book, rules, books_df)
            if recommendations is not None:
                st.markdown('<h2>Recommended Books: </h2>', unsafe_allow_html=True)
                st.markdown('<div class="recommended-books">', unsafe_allow_html=True)
                # cols = st.columns(5)
                for i, (_, row) in enumerate(recommendations.iterrows()):
                    # if i % 5 == 0 and i != 0:
                        # cols = st.columns(5)
                    # with cols[i % 5]:
                        # st.image(row['Image-URL-M'], use_column_width=True, caption=row['Book-Title'])
                    st.markdown(f'<div><img src="{row["Image-URL-M"]}" alt="{row["Book-Title"]}" /><p class="book-title">{row["Book-Title"]}</p></div>', unsafe_allow_html=True)
            else:
                st.warning("No recommendations found for this book.")
    
# Run the Streamlit app
if __name__ == "__main__":
    main()
