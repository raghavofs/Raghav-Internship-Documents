

import openai
from openai import OpenAI 
import os
import time
#ANSI escape code for colors
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m' 
NEON_GREEN = '\033[92m'
RESET_COLOR= '\033[0m'
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def chatgpt_streamed (user_input):
    """
    Function to send a query to OpenAI's GPT-3.5-Turbo model, stream the response, and print each full line in yellow color.
    :param user_input: The query string from the user.
    :return: The complete response from the OpenAI GPT model after all chunks have been received.
    """
# Send the query to the OpenAI API with streaming enabled
    streamed_completion = client.chat.completions.create(
        model="RichardErkhov/EleutherAI_-_Mistral-7B-v0.1-population-first-ft-gguf ",
        messages=[{"role": "user", "content": user_input}],
        stream=True
    )
#Initialize variables to hold the streamed response and the current Line buffer
    full_response = ""
    line_buffer = ""


    for chunk in streamed_completion:
        delta_content = chunk.choices[0].delta.content
        if delta_content is not None:
            line_buffer+=delta_content

            if '\n' in line_buffer:
                lines = line_buffer.split('\n')
                for line in lines[:-1]: # Print all but the Last Line (which might be incomplete) print (NEON_GREEN + line + RESET_COLOR)
                    full_response += line + '\n'
                    line_buffer = lines [-1] # Keep the Last Line in the buffer

    

    if line_buffer:
        print (NEON_GREEN + line_buffer + RESET_COLOR) 
        full_response += line_buffer
        return full_response
 
while True:
    user_prompt = input("Enter your prompt (enter 'quit' or 'exit' to end): ")
    if user_prompt.lower() in ['quit', 'exit']:
        print("Exiting the program...")
        break
    else:
        solution = chatgpt_streamed(user_prompt)
        print("Response:\n", solution)


