import gpt4all

# Example of initializing GPT4All with a larger context length
model_path = "/Users/raghavsubramaniam/Library/Application Support/nomic.ai/GPT4All"
context_length = 4500  # Adjust this according to your needs

model = gpt4all.GPT4All(model_name="hermes", model_path=model_path, allow_download=False, context_length=context_length)
