## これは何
市区町村の境界座標データを`json/{pref_name}.json`に配置。

## 作成手順
1. `gml/` にあらかじめzipデータを用意。用意手順は `gml/README.txt`を参照。
1. `tools/make_municipality_border.py` に都道府県を足す
1. `cd tools`
1. `streamlit run make_municipality_border.py`
1. 対象の都道府県を選択
