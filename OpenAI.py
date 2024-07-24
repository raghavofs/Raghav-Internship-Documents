import openai

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = 'your-api-key'

def generate_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can use other engines like 'davinci', 'curie', 'babbage', 'ada', etc.
            prompt=prompt,
            max_tokens=150,  # Adjust the max tokens as needed
            n=1,
            stop=None,
            temperature=0.7  # Adjust the temperature as needed
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    generated_text = generate_response(user_prompt)
    print("Generated Response:\n", generated_text)
