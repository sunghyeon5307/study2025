# === TEST EVAL (전체 테스트셋) ===
import torch
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.eval()

all_preds, all_labels = [], []

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        logits = model(images)
        preds = logits.argmax(1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

acc = accuracy_score(all_labels, all_preds)
f1  = f1_score(all_labels, all_preds, average="binary")  # cats=0, dogs=1 기준
print(f"Accuracy: {acc:.4f}")
print(f"F1-score: {f1:.4f}\n")

# 클래스별 정밀도/재현율/F1 및 서포트
print(classification_report(all_labels, all_preds, target_names=train_data.classes))

# 혼동행렬(행=실제, 열=예측)
print("Confusion matrix:\n", confusion_matrix(all_labels, all_preds))
