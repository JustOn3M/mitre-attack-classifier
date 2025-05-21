import streamlit as st
from controller import App
import os
import base64

from download_models import ensure_models
ensure_models()

# === Инициализация интерфейса ===
st.set_page_config(page_title="MITRE ATT&CK Классификация", page_icon="🛡️", layout="centered")
st.markdown("<h1 style='text-align: center;'>🛡️ Классификация кибератак по MITRE ATT&CK</h1>", unsafe_allow_html=True)
st.markdown("Введите описание кибератаки ниже. Выберите модель, выполните классификацию и при необходимости сохраните результат в формате JSON.")


# === Поиск доступных моделей ===
def list_available_models():
    models_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "models"))  # путь к ./models относительно корня проекта
    return sorted([f for f in os.listdir(models_path) if os.path.isdir(os.path.join(models_path, f))])


# === Класс Interface ===
class Interface:
    def __init__(self):
        self.models = list_available_models()
        self.selected_model_name = st.selectbox("Выберите модель:", self.models)
        self.app = App(model_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "models", self.selected_model_name)))


    def run(self):
        user_input = st.text_area("Описание кибератаки", height=200, placeholder="Пример: The attacker gained initial access via phishing and executed scripts to escalate privileges...")

        if st.button("Классифицировать"):
            clean_text = user_input.strip()
            word_count = len(clean_text.split())

            if not clean_text:
                st.error("Пожалуйста, введите текст.")
            elif len(clean_text) < 20:
                st.warning("Описание слишком короткое. Введите более развернутое описание атаки.")
            elif word_count < 5:
                st.warning("Слишком мало слов. Введите более содержательное описание.")
            else:
                with st.spinner("Анализируем..."):
                    result = self.app.classify(clean_text)
                if result:
                    st.success("Обнаружены следующие тактики:")
                    st.markdown("\n".join(f"- **{label}**" for label in result))

                    # === Сохранение в JSON ===
                    json_data = self.app.save_result(clean_text)
                    b64 = base64.b64encode(json_data.encode()).decode()
                    href = f'<a href="data:file/json;base64,{b64}" download="classification_result.json">📥 Скачать результат (JSON)</a>'
                    st.markdown(href, unsafe_allow_html=True)
                else:
                    st.info("Тактики не обнаружены.")


# === Запуск ===
if __name__ == "__main__":
    interface = Interface()
    interface.run()
