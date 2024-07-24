from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

model_id = "./local_model"  # Path to the locally saved model

# Load the model and tokenizer from the local directory
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

# Create a text generation pipeline
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=1000)

def ask_question():
    while True:
        question = input("Ask me anything (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        response = generator(question)
        print("Answer:", response[0]['generated_text'])

# Start the interactive question-answer loop
if __name__ == "__main__":
    ask_question()
