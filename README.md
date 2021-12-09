# travel_map

https://share.streamlit.io/sergicalsix/travel_map/main.py

## 技術選定の理由

### アプリについて

  無料でデプロイできる and 使用経験がある and 聴衆の方に馴染みがある可能性が高いことから`Streamlit`を採用


### 地図について
  
  マーカーのカスタマイズ性 and 地図の中身が日本語 and 実装が簡単なので`folium`を選択。

他の選択肢として、デフォルト(`streamlit`)、`(geo)pandas`、`skmob`、`pydeck`などがあった。
今回`shp`ファイルに書き出す必要性を感じなかったので`pandas`系は採用しなかった。

余談だが、地図について 1 行で`html`に書き出すことが可能である。

###  経路探索と移動時間の計算
  
  本実装ではまず`scipy.spatial`の`distance`メソッドで空間を無視した全ユークリッド距離を算出した。
  理由はピュア python や numpy で実装に他に比べて最も高速だからである。

次に最適化は`pulp`で行った。これに関しては、特に理由はなく他のライブラリで実装しても全く変わりはない。

最後に移動時間の計算は、選択された経路に対して`skmob.utils.gislib`の`getDistance`メソッドを利用した。
このメソッドでは地球を球体と仮定して、経路を算出するためユークリッド距離よりも正確である。
ただ国土地理院の公式サイトで計算する or 楕円球体と仮定して計算した方が正確だが、実装の難易度および時間の制約から断念した。

距離の算出方法を変えた理由として、
計算量が多いものは高速に、少ないものは正確に計算を行ったためである。
( 全距離は地点数 n に対して計算量が O(n^2)のオーダーに対して、
一方で選択された経路は（今回のアルゴリズムでは）計算量が O(n)である)


## カスタマイズ Tips

- 地図のマーカーを変えたい
  `codes.py/marker_decoration`を変更
- 巡回経路を変えたい
  `codes.py/route_selection`の`p`に加える制約条件を変更

- API を Open Street Map から変えたい
  　`codes.py/get_place_datum`の`geocoder`のメソッドを変更

## メモ

### frontend

- streamlit
  travel_plan

1. 時刻(必須でない)、場所の名称(必須)を入力 → 緯度経度入りの dataframe を出力

or ファイル入力(require)

2. 出力ボタン-> ２ D 地図、経路

### backend

1.  Web アプリで名称を入力 →google map api or mapbox 系の api で緯度経度を取得
    (場所を追加するごとに逐次的)

できればラベル付けする(mapbox が有力)

2. 2 次元の地図は folium、経路は pulp で計算
