from openai import OpenAI
api_key = "500293d613d84863bfcff567380fe4d1"
base_url = "https://api.aimlapi.com"
client = OpenAI(api_key=api_key, base_url=base_url)
def ask_question():
    print("Welcome to the AI Assistant!")
    print("Ask me anything, and I'll do my best to answer.")
    conversation_history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        conversation_history.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {"role": "system", "content": "You are an AI assistant who knows everything."},
            ] + conversation_history,
        )
        message = response.choices[0].message.content
        print(f"Assistant: {message}")
        conversation_history.append({"role": "assistant", "content": message})
if __name__ == "__main__":
    ask_question()

#llamaindex
#langchain
#RAG - focus
