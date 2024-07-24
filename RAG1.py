import requests

# Initialize the AIML API client
aiml_api_key = "942b7a80a84f421297055246c302c365"
base_url = "https://api.aimlapi.com"

def get_answer_from_aiml(prompt):
    headers = {
        'Authorization': f'Bearer {aiml_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "system", "content": "You are an AI assistant who knows everything."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(f"{base_url}/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()  # Raise error for bad HTTP response
        response_json = response.json()
        answer = response_json.get('choices', [{'message': {'content': 'I could not understand your question.'}}])[0]['message']['content']
    except requests.exceptions.RequestException as e:
        answer = f"An error occurred while querying the AIML API: {str(e)}"
    except KeyError:
        answer = "Unexpected response format from the AIML API."
    
    return answer

def search_wikipedia(query):
    wikipedia_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles={query.replace(' ', '%20')}"
    try:
        response = requests.get(wikipedia_url)
        response.raise_for_status()
        data = response.json()
        page_id = next(iter(data['query']['pages']))
        if page_id == '-1':
            return None
        else:
            return data['query']['pages'][page_id]['extract']
    except requests.exceptions.RequestException as e:
        return f"An error occurred while querying Wikipedia: {str(e)}"
    except KeyError:
        return "Unexpected response format from Wikipedia."

def main():
    print("Welcome to the AI Assistant!")
    print("Ask me anything, and I'll try to answer using Wikipedia and AIML.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        
        # Search Wikipedia for user input
        wikipedia_summary = search_wikipedia(user_input)
        
        if wikipedia_summary:
            prompt = f"Based on the information from Wikipedia:\n\n{wikipedia_summary}\n\nCan you provide more details on '{user_input}'?"
        else:
            prompt = f"I couldn't find detailed information on '{user_input}' on Wikipedia. Can you provide more details?"
        
        # Get answer from AIML API
        answer = get_answer_from_aiml(prompt)
        
        print(f"Assistant: {answer}")

if __name__ == "__main__":
    main()
