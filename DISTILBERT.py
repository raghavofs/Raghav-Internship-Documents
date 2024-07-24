from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, pipeline

# Load pre-trained model and tokenizer
model_name = 'distilbert-base-uncased'
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(model_name)

# Create a sentiment analysis pipeline
classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

# Initialize context
context = None

while True:
    # Get user input
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() == 'exit':
        print("Chatbot: Goodbye!")
        break

    # Concatenate with context if available
    if context:
        user_input = context + " " + user_input

    # Perform sentiment analysis
    outputs = classifier(user_input)

    # Extract sentiment label
    sentiment_label = outputs[0]['label']

    # Generate response based on sentiment
    if sentiment_label == 'POSITIVE':
        response = "That sounds great!"
    else:
        response = "I'm sorry to hear that."

    # Display response
    print("Chatbot:", response)

    # Update context
    context = user_input
