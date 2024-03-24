import random
import re
import json
import datetime

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and extra whitespace
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def get_intent(user_input, intents):
    preprocessed_input = preprocess_text(user_input)

    # Implement intent recognition logic
    # Match the preprocessed input with the patterns in intents
    # Return the intent label

    for intent in intents:
        patterns = intent['patterns']
        for pattern in patterns:
            if re.search(pattern, preprocessed_input, re.IGNORECASE):
                return intent['tag']

    # If no intent is recognized, return a default intent
    return 'fallback'

def generate_response(intent, user_input, intents):
    # Retrieve the responses corresponding to the intent
    for intent_data in intents:
        if intent_data['tag'] == intent:
            if 'patterns' in intent_data and 'responses' in intent_data:
                patterns = intent_data['patterns']
                responses = intent_data['responses']
                if patterns and responses:
                    for i, pattern in enumerate(patterns):
                        if re.search(pattern, user_input, re.IGNORECASE):
                            return responses[i]

    return "I'm sorry, but I couldn't understand your request. Could you please rephrase?"

def recommend_questions(user_input, intents):

    questions = [
        "Is ADTU a private university?",
        "Where is ADTU University located?",
        "Which companies visit university for placements?",
        "Are scholarships available?",
        "Tell me more about the campus facilities.",
        "How to get admission in undergraduate programs?",
        "What is the student-to-faculty ratio?",
        "Can I apply for an educational loan through ADTU University?",
        "Can international students apply to ADTU University?",
        "What is the duration of undergraduate programs at ADTU University?",
        "What are the hostel facilities?",
        "Are there any research opportunities for undergraduates?",
        "How is the education system structured at AdtU?",
        "What courses does ADTU University offer?",
        "Are there any scholarships available for international students?",
        "Is there any attendance requirement for appearing in the End semester Examination?",
        "Which language should be used for official communication?",
        "Can I pursue a PhD program at ADTU University?",
        "What are the admission requirements for the MBA program?",
        "How can I contact the admission office of ADTU University?",
        "Can I apply for the Computer Science program if I have a diploma in computer science?",
        "does adtu provide mba specialization courses?",
        "What is the placement record of ADTU University",
        "does university have placement facility?",
        "Are there opportunities for part time employment?",
        "Does AdtU provide transport service?",
        "Does ADTU University have sports facilities for students?",
        "What programming languages are taught in the Computer Science program at ADTU University?"
    ]
    for intent_data in intents:
        if 'questions' in intent_data:
            questions.extend(intent_data['questions'])
    recommended_questions = random.sample(questions, 3)
    return recommended_questions

def perform_sentiment_analysis(user_input):
    positive_words = ["good", "great", "excellent", "positive"]
    negative_words = ["bad", "terrible", "poor", "negative"]

    # Tokenize the user input
    tokens = user_input.lower().split()

    # Calculate the sentiment score based on the presence of positive and negative words
    sentiment_score = 0
    for word in tokens:
        if word in positive_words:
            sentiment_score += 1
        elif word in negative_words:
            sentiment_score -= 1

    # Determine the sentiment label based on the sentiment score
    if sentiment_score > 0:
        sentiment_label = 'positive'
    elif sentiment_score < 0:
        sentiment_label = 'negative'
    else:
        sentiment_label = 'neutral'

    return sentiment_score, sentiment_label

def log_sentiment(user_input, response, sentiment_label, sentiment_score):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] User: {user_input} | Bot: {response} | Sentiment: {sentiment_label} | Score: {sentiment_score}\n"

    # Append the log entry to a log file or store it in a database
    with open('chatbot_log.txt', 'a') as log_file:
        log_file.write(log_entry)

def get_chatbot_response(user_input):
    intents = load_intents_from_file('intents.json')
    intent = get_intent(user_input, intents)
    response = generate_response(intent, user_input, intents)
    sentiment_score, sentiment_label = perform_sentiment_analysis(user_input)
    log_sentiment(user_input, response, sentiment_label, sentiment_score)

    # If sentiment is negative and there is no specific response for negative sentiment, provide an apology
    if sentiment_label == 'negative' and not any(intent_data['tag'] == 'negative' for intent_data in intents):
        apology_response = "I apologize if my previous response was not helpful. Please let me know how I can assist you."
        return apology_response, [], sentiment_label

    # If user says "thank you" or a closing statement, provide a response without recommending questions
    closing_statements = ["thank you", "thanks", "goodbye", "bye", "take care"]
    if any(statement in user_input.lower() for statement in closing_statements):
        closing_response = "You're welcome! If you have any more questions, feel free to ask."
        return closing_response, [], sentiment_label

    recommended_questions = recommend_questions(user_input, intents)
    return response, recommended_questions, sentiment_label

def load_intents_from_file(file_path):
    with open(file_path, 'r') as file:
        intents = json.load(file)
    return intents
