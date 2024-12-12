import pyfpgrowth

def get_book_recommendations(book_title, rules, df):
    recommendations = set()
    for rule_antecedent, rule_consequent in rules.items():
        if book_title in rule_antecedent:
            recommendations.update(rule_consequent[0])
    
    recommendations.discard(book_title)
    
    recommended_books = df[df['Book-Title'].isin(recommendations)].drop_duplicates('Book-Title')[['Book-Title', 'Image-URL-M']]
    return recommended_books if not recommended_books.empty else None

