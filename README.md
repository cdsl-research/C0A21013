## 目的
マイクロサービスにおいて冗長なエラーメッセージを受信することで管理者は異常がある場所の特定が困難ということであるため，提案ソフトウェアによりマイクロサービ
スで構築するアプリケーション内にある各サービスのPodのCPU使用量で原因特定を行う．

## 準備するもの
Prometheus,Istio

## 使い方
* cpu_use.py
kubectl top コマンドにより各Pod の Sock Shop の CPU 使用量を取得する(getcpumemory.sh)．取得した CPU 使用量を 1 分間ごとの平均値を出す．最新の平均値が直前の平均値より減少したかを判定する．

* prom.py
直前の平均値より減少したかを判定する．prom.py では，1 分間ごとのリクエスト数を取得する.

* notification.py
cpu use.py によって判定された Pod を notification.py により管理者に原因場所の通知が slack に送られる．

## 注意点
* Prometheusを起動した状態でないと使えません．
* cpu_use.pyから実行してください．
* cpu_use.pyの39行目の変数exclude_stringsは指定したPodを表示させないようにするため，各自で指定してください．
* prom.pyの5行目の変数prometheus_urlにPrometheusのエンドポイントを指定を指定してください．
* notification.pyのWEB_HOOK_URLはslackから自分のWebhook URLを取得して貼り付けてください．



