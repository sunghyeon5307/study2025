from sklearn.metrics import accuracy_score, f1_score, classification_report

all_preds = []
all_labels = []

model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        preds = outputs.argmax(1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

print("Accuracy:", accuracy_score(all_labels, all_preds))
print("F1-score:", f1_score(all_labels, all_preds, average="binary"))
print(classification_report(all_labels, all_preds, target_names=train_data.classes))
