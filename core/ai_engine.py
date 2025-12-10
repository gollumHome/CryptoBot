import google.generativeai as genai
# 关键点：从 settings 导入模板，而不是在代码里写死
from config.settings import GEMINI_KEY, CRYPTO_PROMPT_TEMPLATE

class GeminiAnalyst:
    def __init__(self):
        if not GEMINI_KEY:
            raise ValueError("Gemini API Key 未配置！")
        genai.configure(api_key=GEMINI_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze(self, chat_text, group_name, hours):
        """
        组装提示词并调用 API
        """
        if not chat_text:
            return None

        # 使用 settings.py 中的模板进行填充
        prompt = CRYPTO_PROMPT_TEMPLATE.format(
            group_name=group_name,
            hours=hours,
            chat_history=chat_text
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return f"⚠️ 研报生成失败: {e}"