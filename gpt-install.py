from transformers import GPT2Tokenizer, GPT2Model

# Specify the GPT-2 model size ('gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl')
model_name = 'gpt2-medium'

# Download the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2Model.from_pretrained(model_name)
