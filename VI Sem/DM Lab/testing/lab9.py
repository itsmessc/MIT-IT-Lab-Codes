Q2 and Q3

import numpy as np
import re
from collections import defaultdict, Counter
from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics import confusion_matrix
from math import log
import matplotlib.pyplot as plt

# 1. Load the dataset
newsgroups = fetch_20newsgroups(subset='all')
X_raw = newsgroups.data
y = np.array(newsgroups.target)
labels = newsgroups.target_names
num_classes = len(labels)

# 2. Text preprocessing: Tokenization + Lowercasing + Word Filtering
def preprocess(text):
    text = text.lower()
    words = re.findall(r'\b[a-z]{3,}\b', text)  # Keep words with 3+ letters
    return words

X_processed = [preprocess(doc) for doc in X_raw]

# 3. Split data (manually, e.g., 80/20 split)
def train_test_split_manual(X, y, test_size=0.2):
    indices = np.arange(len(X))
    np.random.seed(42)
    np.random.shuffle(indices)
    split = int(len(X) * (1 - test_size))
    train_idx, test_idx = indices[:split], indices[split:]
    return [X[i] for i in train_idx], [X[i] for i in test_idx], y[train_idx], y[test_idx]

X_train, X_test, y_train, y_test = train_test_split_manual(X_processed, y)

# 4. Build Vocabulary & Class-Wise Word Frequencies
class_word_counts = [defaultdict(int) for _ in range(num_classes)]
class_doc_counts = [0] * num_classes
vocab = set()

for doc, label in zip(X_train, y_train):
    class_doc_counts[label] += 1
    for word in doc:
        class_word_counts[label][word] += 1
        vocab.add(word)

vocab = list(vocab)
vocab_index = {word: idx for idx, word in enumerate(vocab)}
vocab_size = len(vocab)

# 5. Calculate Priors and Likelihoods (with Laplace smoothing)
class_total_words = [sum(c.values()) for c in class_word_counts]
priors = [class_doc_counts[c] / len(X_train) for c in range(num_classes)]

def compute_likelihood(word, class_id):
    # Laplace smoothing
    return (class_word_counts[class_id][word] + 1) / (class_total_words[class_id] + vocab_size)

# 6. Predict function
def predict(doc):
    word_counts = Counter(doc)
    scores = []
    for c in range(num_classes):
        log_prob = log(priors[c])
        for word, count in word_counts.items():
            if word in vocab_index:
                prob = compute_likelihood(word, c)
                log_prob += count * log(prob)
        scores.append(log_prob)
    return np.argmax(scores)

# 7. Evaluate on test set
y_pred = [predict(doc) for doc in X_test]

# 8. Confusion Matrix using sklearn
conf_matrix = confusion_matrix(y_test, y_pred)

# 9. Accuracy, Precision, Recall
def accuracy_score(y_true, y_pred):
    return np.mean(np.array(y_true) == np.array(y_pred))

def precision_score(conf_matrix):
    precisions = []
    for c in range(num_classes):
        tp = conf_matrix[c, c]
        fp = sum(conf_matrix[:, c]) - tp
        precisions.append(tp / (tp + fp) if (tp + fp) > 0 else 0)
    return np.mean(precisions)

def recall_score(conf_matrix):
    recalls = []
    for c in range(num_classes):
        tp = conf_matrix[c, c]
        fn = sum(conf_matrix[c, :]) - tp
        recalls.append(tp / (tp + fn) if (tp + fn) > 0 else 0)
    return np.mean(recalls)

# 10. Print Results
print("Confusion Matrix:\n", conf_matrix)
print("\nAccuracy:", round(accuracy_score(y_test, y_pred), 4))
print("Precision (Macro):", round(precision_score(conf_matrix), 4))
print("Recall (Macro):", round(recall_score(conf_matrix), 4))
