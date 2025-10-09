from supabase import create_client, Client
from dotenv import load_dotenv
import os

# DataFrameから一括保存する場合
def insert_math_problems_df(df):
    """
    Supabaseに数学問題のDataFrameを一括保存する関数。
    Args:
        df (pd.DataFrame): 保存する数学問題のDataFrame。
    Returns:
        dict: Supabaseからのレスポンス。
    """
    # .envファイルの読み込み
    load_dotenv()
    supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

    # ID列がなければ追加、既存なら連番で振り直す
    if "ID" not in df.columns:
        df["ID"] = range(1, len(df) + 1)
    else:
        # 既存IDが重複・欠損している場合は連番で振り直す
        df["ID"] = range(1, len(df) + 1)
    data_list = df.to_dict(orient="records")
    res = supabase.table("math_problem").insert(data_list).execute()
    return res