from datasets import DatasetDict, Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, DataCollatorWithPadding
import evaluate
import numpy as np
import json
from scipy.special import softmax

# ================== Load Model ===============================

# pre-trained model path
model_path = "timter/bert-vectormail"

# load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)

# add classification head

id2label = {
    0: "kfz-schaden", 
    1: "hausrat-schaden", 
    2: "haftpflichtschaden", 
    3: "reiseschaden", 
    4: "tierkrankheit"
}

label2id = {
    "kfz-schaden": 0,
    "hausrat-schaden": 1,
    "haftpflichtschaden": 2,
    "reiseschaden": 3,
    "tierkrankheit": 4
}

model = AutoModelForSequenceClassification.from_pretrained(
    model_path, 
    num_labels = 5, 
    id2label = id2label, 
    label2id = label2id
)    

# ================== Prepare Model for training  ===============================


# freeze all base model parameters
for name, param in model.base_model.named_parameters():
    param.requires_grad = False

# unfreeze base model pooling layers
for name, param in model.base_model.named_parameters():
    if "pooler" in name:
        param.requires_grad = True


# ================== Load Trainingsdata ===============================

with open("training_data/emails_2.json", 'r', encoding='utf-8') as f:
    data_from_json = json.load(f)

# Create a Hugging Face Dataset object from the list of email dictionaries.
full_dataset = Dataset.from_list(data_from_json)

# Split the full dataset into training and testing (or validation) sets.
train_test_split = full_dataset.train_test_split(test_size=0.2, seed=42)

# Create a DatasetDict to store the train and validation splits.
dataset_dict = DatasetDict({
    'train': train_test_split['train'],          # Assign the training split
    'validation': train_test_split['test']       # Assign the test split as the validation set
})


# ================== Pre-Procces Data ===============================

# define text preprocessing
def preprocess_function(examples):
     # Tokenisierung des Textes mit Truncation und maximaler Länge
    tokenized_inputs = tokenizer(examples["text"], truncation=True, max_length=128)
    tokenized_inputs["labels"] = [label2id[label_name] for label_name in examples["label"]]
    
    return tokenized_inputs

# preprocess all datasets
tokenized_data = dataset_dict.map(preprocess_function, batched=True, remove_columns=["label"])

# create data collator
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# ================== Define Metrics ===============================


accuracy_metric = evaluate.load("accuracy")
roc_auc_metric = evaluate.load("roc_auc")
precision_metric = evaluate.load("precision")
recall_metric = evaluate.load("recall")
f1_metric = evaluate.load("f1")

# Die id2label-Zuordnung (wie zuvor definiert)
id2label = {0: "Kfz-Schaden", 1: "Hausrat-Schaden", 2: "Haftpflichtschaden", 3: "Reiseschaden", 4: "Tierkrankheit"}
num_labels = len(id2label) # Anzahl der Labels, basierend auf id2label

def compute_metrics(eval_pred):
    # Unpack predictions and true labels
    logits, labels = eval_pred.predictions, eval_pred.label_ids

    # Get predicted class (index of highest logit)
    predictions = np.argmax(logits, axis=-1)

    # Convert logits to probabilities (needed for AUC)
    probabilities = softmax(logits, axis=-1)

    metrics = {}

    # =============================
    # 1. General Metrics
    # =============================

    # Accuracy
    accuracy_result = accuracy_metric.compute(predictions=predictions, references=labels)
    metrics.update(accuracy_result)

    # AUC (Area Under Curve) - only for multi-class
    if num_labels > 1:
        try:
            auc_result = roc_auc_metric.compute(
                prediction_scores=probabilities,
                references=labels,
                multi_class='ovr',
                average='weighted',
                labels=list(range(num_labels))
            )
            metrics['auc'] = auc_result['roc_auc']
        except ValueError as e:
            print(f"Warning: AUC could not be computed (Error: {e}). Setting AUC to NaN.")
            metrics['auc'] = float('nan')
    else:
        metrics['auc'] = float('nan')

    # =============================
    # Per-Label Metrics
    # =============================

    # Precision per class
    precision_results = precision_metric.compute(predictions=predictions, references=labels, average=None, labels=list(range(num_labels)))
    if precision_results and 'precision' in precision_results:
        for i, p_score in enumerate(precision_results['precision']):
            metrics[f"precision_{id2label.get(i, f'label_{i}')}"] = p_score

    # Recall per class
    recall_results = recall_metric.compute(predictions=predictions, references=labels, average=None, labels=list(range(num_labels)))
    if recall_results and 'recall' in recall_results:
        for i, r_score in enumerate(recall_results['recall']):
            metrics[f"recall_{id2label.get(i, f'label_{i}')}"] = r_score

    # F1 score per class
    f1_results = f1_metric.compute(predictions=predictions, references=labels, average=None, labels=list(range(num_labels)))
    if f1_results and 'f1' in f1_results:
        for i, f1_score in enumerate(f1_results['f1']):
            metrics[f"f1_{id2label.get(i, f'label_{i}')}"] = f1_score

    return metrics

    

# ================== Define Trainingarguments ===============================

# hyperparameters
lr = 2e-5
batch_size = 8
num_epochs = 10

training_args = TrainingArguments(
    output_dir="bert-label-classifier_teacher",
    learning_rate=lr,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=num_epochs,
    logging_strategy="epoch",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)


# ================== Train Model ===============================


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data["train"],
    eval_dataset=tokenized_data["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()