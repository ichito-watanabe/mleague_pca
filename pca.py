import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ======================
# 日本語フォント
# ======================

font_candidates = [
    Path("C:/Windows/Fonts/NotoSansJP-VF.ttf"),
    Path("C:/Windows/Fonts/YuGothM.ttc"),
    Path("C:/Windows/Fonts/meiryo.ttc"),
    Path("C:/Windows/Fonts/msgothic.ttc"),
]

for font_path in font_candidates:
    if font_path.exists():
        font_manager.fontManager.addfont(font_path)
        font_name = font_manager.FontProperties(
            fname=font_path
        ).get_name()
        plt.rcParams["font.family"] = font_name
        break

plt.rcParams["axes.unicode_minus"] = False

# ======================
# 画像保存先
# ======================

output_dir = Path("pca_images")
output_dir.mkdir(exist_ok=True)

# ======================
# チームカラー
# ======================

team_colors = {
    "EARTH JETS": "#e60012",
    "赤坂ドリブンズ": "#b51f32",
    "EX風林火山": "#d61718",
    "KADOKAWAサクラナイツ": "#f08aaa",
    "KONAMI 麻雀格闘倶楽部": "#231815",
    "渋谷ABEMAS": "#bfa566",
    "セガサミーフェニックス": "#0081cc",
    "TEAM RAIDEN / 雷電": "#fbc600",
    "BEAST X": "#003050",
    "U-NEXT Pirates": "#008fd0",
}

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

# PCAに使ったデータを確認用に保存
pca_input_df = df[
    ["選手名", "チーム名"] + features
]

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
        color=team_colors.get(team, "gray"),
        edgecolors="white",
        linewidths=0.8,
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

plt.savefig(
    output_dir / "pca_scatter.png",
    dpi=300,
    bbox_inches="tight"
)

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

plt.savefig(
    output_dir / "pc1_loading.png",
    dpi=300,
    bbox_inches="tight"
)

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

plt.savefig(
    output_dir / "pc2_loading.png",
    dpi=300,
    bbox_inches="tight"
)

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

for team, row in team_center.iterrows():
    plt.scatter(
        row["PC1"],
        row["PC2"],
        s=250,
        color=team_colors.get(team, "gray"),
        edgecolors="white",
        linewidths=1.0
    )

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

plt.savefig(
    output_dir / "team_center_pca.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ======================
# CSV保存
# ======================

csv_outputs = [
    (
        pca_input_df,
        "pca_input_data.csv",
        {"index": False}
    ),
    (
        pca_df,
        "pca_result.csv",
        {"index": False}
    ),
    (
        loading,
        "pca_loading.csv",
        {}
    ),
    (
        team_center,
        "team_center.csv",
        {}
    ),
]

saved_csv_files = []
failed_csv_files = []

for output_df, output_path, options in csv_outputs:
    try:
        output_df.to_csv(
            output_path,
            encoding="utf-8-sig",
            **options
        )
        saved_csv_files.append(output_path)
    except PermissionError:
        failed_csv_files.append(output_path)

print("\n======================")
print("保存完了")
print("======================")

for saved_csv_file in saved_csv_files:
    print(f"・{saved_csv_file}")

print("・pca_images/pca_scatter.png")
print("・pca_images/pc1_loading.png")
print("・pca_images/pc2_loading.png")
print("・pca_images/team_center_pca.png")

if failed_csv_files:
    print("\n======================")
    print("保存できなかったCSV")
    print("======================")
    for failed_csv_file in failed_csv_files:
        print(f"・{failed_csv_file}")
    print("Excelなどで開いている場合は閉じてから再実行してください。")
