import json
from model_handler import Model


class App:
    def __init__(self, model_path: str):
        self.model = Model(model_path)
        self.result = None

    def change_model(self, model_path: str):
        self.model.change_model(model_path)

    def classify(self, text: str):
        self.result = self.model.classify_text(text)
        return self.result

    def save_result(self, original_text: str) -> str:
        return json.dumps({
            "input_text": original_text,
            "predicted_labels": self.result
        }, ensure_ascii=False, indent=2)
