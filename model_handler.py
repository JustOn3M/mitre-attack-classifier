import torch
import numpy as np
import os
import re
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import BertConfig


class Model:
    def __init__(self, model_dir: str):
        self.model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
        self.available_models = self._find_available_models()
        self.model = None
        self.tokenizer = None
        self.thresholds = None
        self.label_names = [
            'Collection', 'Command and Control', 'Credential Access', 'Defense Evasion',
            'Discovery', 'Execution', 'Exfiltration', 'Impact', 'Initial Access',
            'Lateral Movement', 'Persistence', 'Privilege Escalation',
            'Reconnaissance', 'Resource Development'
        ]

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.change_model(model_dir)

    def _find_available_models(self):
        models = []
        root = "./models"
        if os.path.isdir(root):
            for entry in os.listdir(root):
                full_path = os.path.join(root, entry)
                if os.path.isdir(full_path):
                    models.append(full_path)
        return models

    def change_model(self, path: str):
        from pathlib import Path
        path = Path(path).resolve()
        self.tokenizer = BertTokenizer.from_pretrained(str(path), local_files_only=True)
        try:
            self.model = BertForSequenceClassification.from_pretrained(
                str(path),
                local_files_only=True
            ).to(self.device)
        except NotImplementedError as e:
            print("[!] Ошибка загрузки модели — вероятно, файл весов повреждён или пустой.")
            raise e
        self.model.eval()

        try:
            self.thresholds = np.load(os.path.join(path, "thresholds.npy"))
        except Exception:
            self.thresholds = [0.5] * len(self.label_names)

    def classify_text(self, text: str) -> list[str]:
        clean_text = self._preprocess(text)
        if len(clean_text) < 20 or len(clean_text.split()) < 5:
            return []

        inputs = self.tokenizer(clean_text, return_tensors="pt", truncation=True, padding=True, max_length=128).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.sigmoid(outputs.logits).squeeze().cpu().numpy()

        predicted_labels = [self.label_names[i] for i, prob in enumerate(probs) if prob >= self.thresholds[i]]
        return predicted_labels

    def _preprocess(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ.,!?;:()\'\"\\\-\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip().lower()
