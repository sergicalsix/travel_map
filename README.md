# travel_map
https://share.streamlit.io/sergicalsix/travel_map/main.py


# メモ
### frontend
- streamlit
travel_plan
1. 時刻(必須でない)、場所の名称(必須)を入力→緯度経度入りのdataframeを出力

or ファイル入力(require)

2. 出力ボタン->  ２D地図、経路

### travel plan mode

### backend
1.  Webアプリで名称を入力→google map api or mapbox系のapiで緯度経度を取得
(場所を追加するごとに逐次的)

できればラベル付けする(mapboxが有力)

2. 2次元の地図はfolium、経路はpulpで出す

