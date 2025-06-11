from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger()


tokenizer = AutoTokenizer.from_pretrained("timter/bert-vectormail")
model = AutoModelForSequenceClassification.from_pretrained("timter/bert-vectormail")




def predict_label(email):

    # Pre-proccesing
    processed_email = pre_process_input(email)

    # Tokenize
    inputs = tokenizer(processed_email, return_tensors="pt", truncation=True, max_length=128)

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


def pre_process_input(email):


    beginnings_to_remove = [
        "Sehr geehrte Damen und Herren",
        "Sehr geehrte Frau [NAME]",
        "Sehr geehrter Herr [NAME]",
        "Guten Tag Frau [NAME]",
        "Guten Tag Herr [NAME]",
        "Lieber Herr [NAME]",
        "Liebe Frau [NAME]",
        "Guten Tag",
        "Hallo Frau [NAME]",
        "Hallo Herr [NAME]"
        "Sehr geehrtes Team",
        "Werte Frau [NAME]",
        "Werter Herr [NAME]",
        "Sehr geehrte Versicherung"
    ]


    endings_to_remove = [
        "Mit freundlichen Grüßen",
        "Freundliche Grüße",
        "Viele Grüße",
        "Liebe Grüße",
        "Herzliche Grüße",
        "Mit besten Grüßen",
        "Für Rückfragen stehe ich Ihnen gerne zur Verfügung",
        "Vielen Dank im Voraus und freundliche Grüße",
        "Ich freue mich auf Ihre Rückmeldung",
        "Hochachtungsvoll",
        "Mit den besten Wünschen",
        "Vielen Dank"
    ]

    formatted_email = email

    # Remove Beginnings

    beginning_found = False

    for text in beginnings_to_remove:

        # Return if beginning already found
        if beginning_found:
            break

        # Name expected? TODO remove name correctly
        if "[NAME]" in text:
            text = text.replace("[NAME]", "").strip()
            
        if text.lower() in formatted_email.lower():

            beginning_found = True

            index = formatted_email.find(text)
            if index != -1:
                # Remove following word
                after = formatted_email[index + len(text):].strip()


                remaining = after.split(" ", 1)[1] if " " in after else ""
                formatted_email = "[BEGIN_EMAIL] " + remaining


    
    if not beginning_found:
        formatted_email = "[BEGIN_EMAIL] " + formatted_email




    # Remove Endings

    ending_found = False
    index_to_cut = 10000

    for text in endings_to_remove:

        # Check for ending 
        if text.lower() in formatted_email.lower():

            ending_found = True

            index = formatted_email.lower().find(text.lower()) 

            # Store index of first occuring ending 
            if index != -1 and index_to_cut > index:
                index_to_cut = index


    if ending_found:
        formatted_email = formatted_email[:index].rstrip() + " [END_EMAIL]" 
    else:
        formatted_email =  formatted_email + " [END_EMAIL]"
 

    logger.debug(formatted_email)

    return formatted_email
