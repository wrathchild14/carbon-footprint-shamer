from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
# Load the model and tokenizer
model_name = 'google/flan-t5-large'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
torch.manual_seed(0)
# Set the input text
input_text = "I went to Camp Nou, I am blessed to be there!!!"

# Tokenize the input text
input_ids = tokenizer.encode(input_text + "Where I went or where will I go in terms of country?", return_tensors='pt')

# Generate the output text
outputs = model.generate(input_ids=input_ids, max_length=5, do_sample=True)

# Decode the output text
output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(output_text)