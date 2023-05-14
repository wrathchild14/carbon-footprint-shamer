from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image

image = Image.open("./examples/luka.jpg")
text = "Which country?"

processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

# prepare inputs
encoding = processor(image, text, return_tensors="pt")

# forward pass
outputs = model(**encoding)
logits = outputs.logits

idx = logits.argmax(-1).item()
print("Predicted answer:", model.config.id2label[idx])