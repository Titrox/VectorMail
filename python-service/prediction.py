from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


tokenizer = AutoTokenizer.from_pretrained("timter/bert-vectormail")
model = AutoModelForSequenceClassification.from_pretrained("timter/bert-vectormail")



def predict_label(email):

    # Tokenize
    inputs = tokenizer(email, return_tensors="pt", truncation=True, max_length=128)

    # Aktivate Eval-Mode
    model.eval()

    # Predict propabilities 
    with torch.no_grad(): 
        outputs = model(**inputs)

    # Raw output
    logits = outputs.logits

    # Apply Softmax Function
    probabilities = torch.softmax(logits, dim=-1)

    return probabilities

