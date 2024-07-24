from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_id = "lmsys/fastchat-t5-3b-v1.0"

# Download the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir="./local_model")
model = AutoModelForSeq2SeqLM.from_pretrained(model_id, cache_dir="./local_model")

# Save the model and tokenizer locally
tokenizer.save_pretrained("./local_model")
model.save_pretrained("./local_model")
