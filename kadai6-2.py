import requests
import pandas as pd
#世界経済や社会指標を国別・年別に提供する API。
#エンドポイント構成：https://api.worldbank.org/v2/country/{国コード}/indicator/{指標コード}
API_URL = "https://api.worldbank.org/v2/country/JPN/indicator/NY.GDP.MKTP.CD"#URLで国・指標指定
params = {
    "format": "json",  # JSON 形式で取得
    "per_page": 10    # 年別データを10件取得
}

#API からデータ取得
response = requests.get(API_URL, params=params)
data = response.json()
stats_data = data[1]

#DataFrame に変換
df = pd.DataFrame(stats_data)

#メタ情報相当の項目を、日本語表示に変換
#country、indicator は辞書型→'value'抽出
df['国名']     = df['country'].apply(lambda x: x['value'] if isinstance(x, dict) else x)
df['指標名']   = df['indicator'].apply(lambda x: x['value'] if isinstance(x, dict) else x)

# 5. 列名を日本語に整形
col_rename = {
    'date': '年',
    'value': 'GDP（USD）',
    '国名': '国名',
    '指標名': '指標名'
}

df_simple = df[['date', 'value', '国名', '指標名']].rename(columns=col_rename)

# 6. 年順にソート（任意：降順にする場合は ascending=False）
df_simple = df_simple.sort_values('年', ascending=False).reset_index(drop=True)

# 出力
print(df_simple)
