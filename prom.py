from prometheus_api_client import PrometheusConnect

def get_prometheus_data():
    # Prometheusのエンドポイントを指定
    prometheus_url = "http://192.168.100.237:9090"
    prom = PrometheusConnect(url=prometheus_url)

    # リクエスト数を取得するためのクエリ文字列
    request_count_name = 'istio_requests_total{namespace="sock-shop",name="front-end"}'

    # Prometheusクライアントを使用してメトリクスの範囲データを取得
    request_count_data = prom.get_metric_range_data(metric_name=request_count_name)

    # リクエスト数だけを抽出して返す
    values = request_count_data[1].get('values')
    return values

if __name__ == "__main__":
    # スクリプトが直接実行された場合の処理をここに記述
    values = get_prometheus_data()
    print("\nリクエスト数:")
    for timestamp, value in values:
        print(f"Timestamp: {timestamp}, Value: {value}")