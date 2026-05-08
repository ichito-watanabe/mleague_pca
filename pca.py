import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ======================
# 日本語フォント
# ======================

plt.rcParams["font.family"] = "Noto Sans CJK JP"

# ======================
# CSV読み込み
# ======================

df = pd.read_csv("mleague_team_player_stats.csv")

# ======================
# PCA用特徴量
#
# 「成績」ではなく
# 「打ち筋」を見る
# ======================

features = [
    "平均打点",
    "副露率",
    "リーチ率",
    "放銃率",
    "放銃平均打点",
    "ラス回避率"
]

# ======================
# 使用データ
# ======================

X = df[features]

# ======================
# 標準化
# PCA前に超重要
# ======================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ======================
# PCA
# ======================

pca = PCA(n_components=2)

X_pca = pca.fit_transform(X_scaled)

# ======================
# PCA結果DataFrame
# ======================

pca_df = pd.DataFrame(
    X_pca,
    columns=["PC1", "PC2"]
)

pca_df["選手名"] = df["選手名"]
pca_df["チーム名"] = df["チーム名"]

# ======================
# 主成分負荷量
# 「軸が何を意味するか」
# ======================

loading = pd.DataFrame(
    pca.components_.T,
    columns=["PC1", "PC2"],
    index=features
)

# ======================
# 寄与率表示
# ======================

print("\n======================")
print("寄与率")
print("======================")

for i, ratio in enumerate(
    pca.explained_variance_ratio_,
    start=1
):
    print(f"PC{i}: {ratio:.4f}")

print(
    f"\n累積寄与率: "
    f"{sum(pca.explained_variance_ratio_):.4f}"
)

# ======================
# 主成分負荷量表示
# ======================

print("\n======================")
print("主成分負荷量")
print("======================")

print(loading)

# ======================
# PC1 解釈補助
# ======================

print("\n======================")
print("PC1 上位特徴")
print("======================")

print(
    loading["PC1"]
    .sort_values(ascending=False)
)

# ======================
# PC2 解釈補助
# ======================

print("\n======================")
print("PC2 上位特徴")
print("======================")

print(
    loading["PC2"]
    .sort_values(ascending=False)
)

# ======================
# PCA散布図
# ======================

plt.figure(figsize=(13, 10))

# チームごと描画
for team in pca_df["チーム名"].unique():

    temp = pca_df[
        pca_df["チーム名"] == team
    ]

    plt.scatter(
        temp["PC1"],
        temp["PC2"],
        s=120,
        label=team,
        alpha=0.8
    )

    # 選手名表示
    for _, row in temp.iterrows():

        plt.text(
            row["PC1"],
            row["PC2"],
            row["選手名"],
            fontsize=9
        )

# 原点線
plt.axhline(
    0,
    color="gray",
    linestyle="--"
)

plt.axvline(
    0,
    color="gray",
    linestyle="--"
)

# 軸ラベル
plt.xlabel("PC1")
plt.ylabel("PC2")

# タイトル
plt.title(
    "Mリーグ選手 打ち筋PCA"
)

plt.grid()

plt.legend()

plt.show()

# ======================
# PC1 loading 可視化
# ======================

plt.figure(figsize=(8, 6))

loading["PC1"].sort_values().plot(
    kind="barh"
)

plt.title("PC1 Loading")

plt.xlabel("Loading")

plt.grid()

plt.show()

# ======================
# PC2 loading 可視化
# ======================

plt.figure(figsize=(8, 6))

loading["PC2"].sort_values().plot(
    kind="barh"
)

plt.title("PC2 Loading")

plt.xlabel("Loading")

plt.grid()

plt.show()

# ======================
# チーム重心
# ======================

team_center = (
    pca_df
    .groupby("チーム名")[["PC1", "PC2"]]
    .mean()
)

print("\n======================")
print("チーム重心")
print("======================")

print(team_center)

# ======================
# チーム重心描画
# ======================

plt.figure(figsize=(10, 8))

plt.scatter(
    team_center["PC1"],
    team_center["PC2"],
    s=250
)

for team, row in team_center.iterrows():

    plt.text(
        row["PC1"],
        row["PC2"],
        team,
        fontsize=10
    )

plt.axhline(
    0,
    color="gray",
    linestyle="--"
)

plt.axvline(
    0,
    color="gray",
    linestyle="--"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.title("チーム重心 PCA")

plt.grid()

plt.show()

# ======================
# CSV保存
# ======================

pca_df.to_csv(
    "pca_result.csv",
    index=False,
    encoding="utf-8-sig"
)

loading.to_csv(
    "pca_loading.csv",
    encoding="utf-8-sig"
)

team_center.to_csv(
    "team_center.csv",
    encoding="utf-8-sig"
)

print("\n======================")
print("保存完了")
print("======================")

print("・pca_result.csv")
print("・pca_loading.csv")
print("・team_center.csv")