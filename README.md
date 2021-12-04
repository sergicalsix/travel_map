# travel_map
## 簡易アプリの作成

### frontend
- streamlit
travel_plan
1. 時刻(必須でない)、場所の名称(必須)を入力→緯度経度入りのdataframeを出力

or ファイル入力(require)

2. 出力ボタン->  ２D(日本語), ３D地図(英語)の描画 

### travel plan mode

### backend
1.  Webアプリで名称を入力→google map api or mapbox系のapiで緯度経度を取得
(場所を追加するごとに逐次的)

できればラベル付けする(mapboxが有力)

2. 2次元の地図はfolium、3Dの地図はpydeckのTrip Layer

