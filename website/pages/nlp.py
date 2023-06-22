import spacy

# Load the pre-trained spaCy English model
nlp = spacy.load('en_core_web_sm')

# Define the generic topics/categories
topics = ['politics', 'sports', 'international', 'crime', 'religion']

# Function to categorize a news title
def categorize_news_title(title):
    doc = nlp(title)
    # Initialize a dictionary to store topic scores
    topic_scores = {topic: 0 for topic in topics}
    
    # Extract relevant features and update topic scores
    for token in doc:
        if token.pos_ == 'NOUN':  # Consider only nouns for topic extraction
            for topic in topics:
                if topic in token.text.lower():
                    topic_scores[topic] += 1
    
    # Find the topic with the highest score
    max_score = max(topic_scores.values())
    top_topics = [topic for topic, score in topic_scores.items() if score == max_score]
    
    return top_topics

# Sample news titles
news_titles = [
    "Political leaders discuss economic reforms",
    "Football match ends in a draw",
    "International conference on climate change",
    "Robbery at a local bank",
    "Religious festival celebrated with fervor"
]

# Categorize each news title
for title in news_titles:
    categories = categorize_news_title(title)
    print(f"Title: {title}")
    print(f"Categories: {', '.join(categories)}")
    print()
