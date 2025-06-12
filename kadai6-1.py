# における「民間給与実態調査（第1表）」の統計データを取得・表示するプログラム
import requests
import json
APP_ID = "dda9883741613e71b17173269a0b851e1cab39c7"

# エンドポイント：getStatsData
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

# 統計データの種類民間給与実態統計調査
#「第1表　給与所得者数・給与額・税額　事業所規模別（2014年～）」を使用

# ◆ 千葉市の6区とその地域コード（cdArea）
chiba_wards = {
    "中央区": "12101",
    "花見川区": "12102",
    "稲毛区": "12103",
    "若葉区": "12104",
    "緑区": "12105",
    "美浜区": "12106"
}

# ◆ 各区ごとにデータを取得・表示
for ward_name, cd_area in chiba_wards.items():
    # リクエストパラメータ設定
    params = {
        "appId": APP_ID,               # APIキー
        "statsDataId": "0004009600",   # 民間給与の統計データID
        "lang": "J",                   # 日本語で取得
        "metaGetFlg": "N",             # メタ情報は不要
        "cntGetFlg": "N",              # 件数だけの取得はしない
        "sectionHeaderFlg": "1",       # セクションヘッダーを有効（階層構造）
        "cdArea": cd_area,             # 各区の地域コードで絞り込み
        "replaceSpChars": "0"          # 特殊文字は置換しない
    }

    print(f"\n--- {ward_name}（地域コード: {cd_area}）のデータ ---")

    # APIへリクエスト送信
    response = requests.get(API_URL, params=params)

    # HTTPレスポンスの確認と結果表示
    if response.status_code == 200:
        data = response.json()
        # 統計データ本体（DATA_INF > VALUE）にアクセス
        values = data.get("GET_STATS_DATA", {}).get("STATISTICAL_DATA", {}).get("DATA_INF", {}).get("VALUE", [])
        
        if not values:
            print("データが見つかりませんでした。")
        else:
            for entry in values[:10]:                 # 上位10件を表示（年ごとのデータ）
                year = entry.get("@time")             # 時間（西暦年）
                value = entry.get("$")                # 実際の値（人数、金額など）
                category = entry.get("@cat01")        # カテゴリコード（A1101など）
                print(f"{year}年: {value} （カテゴリ: {category}）")
    else:
        print("取得失敗")
