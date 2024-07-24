from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the model and tokenizer from the local directory
model_id = "./local_model"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

def generate_response(user_input):
    # Tokenize the input
    inputs = tokenizer(user_input, return_tensors="pt")
    
    # Generate the response
    outputs = model.generate(
        inputs['input_ids'],
        max_length=200,  # Adjust the max_length as needed
        num_beams=5,
        early_stopping=True
    )
    
    # Decode the generated tokens
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = generate_response(user_input)
        print("Chatbot:", response)
