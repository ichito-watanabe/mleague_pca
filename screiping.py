import pandas as pd
import requests

from io import StringIO

# ======================
# URL
# ======================

url = "https://m-league.jp/stats/?season=L001_S022"

# ======================
# チーム名
# ======================

team_names = [
    "EARTH JETS",
    "赤坂ドリブンズ",
    "EX風林火山",
    "KADOKAWAサクラナイツ",
    "KONAMI 麻雀格闘倶楽部",
    "渋谷ABEMAS",
    "セガサミーフェニックス",
    "TEAM RAIDEN / 雷電",
    "BEAST X",
    "U-NEXT Pirates",
]

# ======================
# HTML取得
# ======================

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    url,
    headers=headers
)

# UTF-8固定
response.encoding = "utf-8"

html = response.text

# ======================
# 表取得
# ======================

tables = pd.read_html(
    StringIO(html)
)

print(f"取得表数: {len(tables)}")

# ======================
# 全チーム格納
# ======================

all_dfs = []

# ======================
# チームごと処理
# ======================

for team_id, (team_name, table) in enumerate(
    zip(team_names, tables),
    start=1
):

    # 列名整理
    table.columns = [
        str(c).replace("\n", "").strip()
        for c in table.columns
    ]

    # 1列目を項目名に
    table = table.rename(
        columns={
            table.columns[0]: "項目"
        }
    )

    # 縦横変換
    df = (
        table
        .set_index("項目")
        .T
        .reset_index()
    )

    # 選手名列
    df = df.rename(
        columns={
            "index": "選手名"
        }
    )

    # team_id追加
    df.insert(0, "team_id", team_id)

    # チーム名追加
    df.insert(1, "チーム名", team_name)

    all_dfs.append(df)

# ======================
# 結合
# ======================

result = pd.concat(
    all_dfs,
    ignore_index=True
)

# ======================
# CSV保存
# ======================

result.to_csv(
    "mleague_team_player_stats.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n保存完了")
print("mleague_team_player_stats.csv")