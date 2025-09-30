import os
import pandas as pd
from dotenv import load_dotenv
from typing import Type, List
from pydantic import BaseModel
from create_math import createdifferential, createintegral, USER_PROMPT
import io

# APIキーを使用してGemini APIを設定
import google.generativeai as genai

class MathProblem(BaseModel):
    Question: str
    formula: str
    Hint1: str
    Hint2: str
    select1: str
    select2: str
    Answer: str
    Explanation: str

def formatter(response):
    import io
    import re
    # CSV部分だけ抽出（余計な説明文がある場合に備えて）
    text = response.text
    match = re.search(r"(Question,formula,Hint1,Hint2,select1,select2,Answer,Explanation[\s\S]+)", text)
    if match:
        text = match.group(1)
    df = pd.read_csv(io.StringIO(text))
    return df

def run_gemini(subject: str) -> pd.DataFrame:
    """
    Gemini APIを使用してコンテンツを生成する関数。
    """
    # .envファイルのパスを明示的に指定
    load_dotenv()

    # 環境変数からAPIキーを取得
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if subject == "微分":
        SYSTEM_PROMPT = createdifferential.SYSTEM_PROMPT
    elif subject == "積分":
        SYSTEM_PROMPT = createintegral.SYSTEM_PROMPT

    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-pro')
        response = model.generate_content([
            {"text": SYSTEM_PROMPT},
            {"text": USER_PROMPT}
        ])
        # DataFrameで返す
        return formatter(response)
    else:
        print("APIキーが設定されていません。")
        return pd.DataFrame()


if __name__ == "__main__":
    subject = "微分"
    df = run_gemini(subject)
    print(df.columns)
    print(df.Question)