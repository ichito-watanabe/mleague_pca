# Mリーグ選手 打ち筋PCA分析

Mリーグ公式サイトの個人成績データを取得し、選手ごとの打ち筋を主成分分析（PCA）で可視化するプログラムです。

成績の良し悪しだけではなく、以下のような指標から選手の特徴を分析します。

- 平均打点
- 副露率
- リーチ率
- 放銃率
- 放銃平均打点
- ラス回避率

## ファイル構成

```text
mleague_pca/
├── README.md
├── screiping.py
├── pca.py
├── mleague_team_player_stats.csv
├── pca_result.csv
├── pca_loading.csv
├── team_center.csv
└── pca_images/
```

主なファイルの役割は以下です。

| ファイル | 内容 |
| --- | --- |
| `screiping.py` | Mリーグ公式サイトから選手成績を取得し、CSVに保存する |
| `pca.py` | 取得したCSVを使ってPCAを実行し、結果とグラフを保存する |
| `mleague_team_player_stats.csv` | スクレイピングで取得した選手成績 |
| `pca_result.csv` | 各選手のPCA結果 |
| `pca_loading.csv` | 主成分負荷量 |
| `team_center.csv` | チームごとのPCA上の重心 |
| `pca_images/` | PCAで作成した画像の保存先 |

## セットアップ

プロジェクト直下で仮想環境を作成します。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

必要なライブラリをインストールします。

```powershell
pip install pandas requests lxml matplotlib scikit-learn
```

`pandas.read_html()` でエラーが出る場合は、以下も追加でインストールしてください。

```powershell
pip install beautifulsoup4 html5lib
```

## 実行方法

このプログラムは相対パスでCSVを読み書きするため、先に `mleague_pca` フォルダへ移動してから実行します。

```powershell
cd .\mleague_pca
```

まず、公式サイトからデータを取得します。

```powershell
python .\screiping.py
```

実行すると、以下のCSVが作成されます。

```text
mleague_team_player_stats.csv
```

次に、PCA分析を実行します。

```powershell
python .\pca.py
```

## 出力されるファイル

`pca.py` を実行すると、以下のCSVが作成されます。

```text
pca_result.csv
pca_loading.csv
team_center.csv
```

また、以下の画像が `pca_images` フォルダに保存されます。

```text
pca_images/pca_scatter.png
pca_images/pc1_loading.png
pca_images/pc2_loading.png
pca_images/team_center_pca.png
```

画像の内容は以下です。

| 画像 | 内容 |
| --- | --- |
| `pca_scatter.png` | 選手ごとのPCA散布図 |
| `pc1_loading.png` | 第1主成分の負荷量 |
| `pc2_loading.png` | 第2主成分の負荷量 |
| `team_center_pca.png` | チームごとの重心をプロットした図 |

## 分析の流れ

1. `screiping.py` でMリーグ公式サイトから成績表を取得する
2. 取得した表を選手ごとのデータに整形する
3. `mleague_team_player_stats.csv` に保存する
4. `pca.py` で分析対象の特徴量を選ぶ
5. `StandardScaler` で標準化する
6. `PCA` で2次元に圧縮する
7. 選手・チームごとの特徴をCSVと画像で出力する

## 使用している主なライブラリ

| ライブラリ | 用途 |
| --- | --- |
| `pandas` | 表データの読み込み、整形、CSV保存 |
| `requests` | WebページのHTML取得 |
| `lxml` | HTML内の表を読み取るために使用 |
| `matplotlib` | グラフ描画、画像保存 |
| `scikit-learn` | 標準化とPCA |

## 注意点

- `screiping.py` というファイル名はスペル上は `scraping.py` が一般的ですが、現在のコードでは `screiping.py` のまま使用しています。
- `pca.py` は `mleague_team_player_stats.csv` がある前提で動作します。先に `screiping.py` を実行してください。
- 日本語フォントとして `Noto Sans CJK JP` を指定しています。環境にフォントがない場合、グラフの日本語が文字化けすることがあります。
- 公式サイトのHTML構造が変わると、スクレイピング結果が変わったり、取得に失敗したりする可能性があります。
