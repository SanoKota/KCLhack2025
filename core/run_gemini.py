import os
import pandas as pd
from dotenv import load_dotenv
from typing import Type, List
from pydantic import BaseModel
from core.create_math import createdifferential, createintegral, USER_PROMPT
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
    text = response.text
    # CSVヘッダーから始まる部分だけ抽出
    match = re.search(r"(ID,Question,formula,Hint1,Hint2,select1,select2,Answer,Explanation[\s\S]+)", text)
    if match:
        csv_text = match.group(1)
        # 余計な空行を除去
        csv_text = "\n".join([line for line in csv_text.splitlines() if line.strip()])
        df = pd.read_csv(io.StringIO(csv_text))
        return df
    else:
        raise ValueError("CSV部分が見つかりません")

def run_gemini(subject: str) -> pd.DataFrame:
    """
    Gemini APIを使用してコンテンツを生成し、ID自動付与でCSVに保存する関数。
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
        df = formatter(response)
        # ここでID自動付与でCSV保存
        save_problem_with_incremented_id(subject, df)
        return df
    else:
        raise RuntimeError("APIキーが設定されていません")

def save_problem_with_incremented_id(subject: str, problem_df: pd.DataFrame):
    """
    既存CSVのIDの最大値+1から連番で新しいIDを付与し、全問題を追記保存する
    subject: "微分" または "積分"
    problem_df: 複数問分のDataFrame
    """
    if subject == "微分":
        csv_path = "GameFrame/GameData/differentioal.csv"
    elif subject == "積分":
        csv_path = "GameFrame/GameData/integral.csv"
    else:
        raise ValueError("未対応のsubject")
    # 既存CSVのID最大値を取得
    import pandas as pd
    try:
        existing = pd.read_csv(csv_path, encoding="utf-8")
        max_id = existing['ID'].astype(int).max()
    except Exception:
        max_id = -1
    # 10問分に連番IDを付与
    problem_df = problem_df.copy()
    problem_df['ID'] = range(max_id + 1, max_id + 1 + len(problem_df))
    # 追記保存
    problem_df.to_csv(csv_path, mode="a", header=False, index=False, encoding="utf-8")
    print(f"{csv_path} にID={max_id+1}～{max_id+len(problem_df)}で問題を追加保存しました")

if __name__ == "__main__":
    subject = "微分"
    df = run_gemini(subject)
    print(df.columns)
    print(df.Question)