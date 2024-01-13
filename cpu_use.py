import subprocess
import csv
import numpy as np
import pandas as pd
from prom import get_prometheus_data
from notification import send_notification

def get_cpu_result():
    # シェルスクリプトのパス
    script_path = 'getcpumemory.sh'

    # シェルスクリプトを実行
    result = subprocess.run(['bash', script_path])

    # シェルスクリプトが存在するか確認
    if result.returncode != 0:
        return f"Error: Script execution failed with return code {result.returncode}"

    # subprocess.run()が完了するまで待機してからCSVファイルを開くことで、実行結果のCSVファイルを処理できる

    # subprocess.run()が完了するまで待機してからデータを取得
    values = get_prometheus_data()

    # データを表示
    print("\nリクエスト数:")
    for timestamp, value in values:
        print(f"Timestamp: {timestamp}, Value: {value}")

    # CSVファイルのパス
    csv_file_path = 'monicsv/moni_1017_t.csv'

    # 文字列の列のインデックス
    string_column_index = 1

    # 数値の列のインデックス
    numeric_column_index = 2

    # 特定のpodをリストで指定 最後にPodname変更した方がいい
    exclude_strings = ['carts-db-77dcb9c7b7-7k2jt', 'catalogue-db-d764d45d6-nn2rb', 'orders-db-6d74d86657-4j495',
                       'payment-67f94cc7b8-764tj', 'queue-master-cc96b5649-lr444', 'rabbitmq-5c6f77d9dd-x6d8g',
                       'session-db-76d658cbf8-n8plq', 'user-db-5bfb568f5b-mg2kh']

    pod_dict_key = []   # pod名
    pod_dict_value = [] # podのCPU使用量

    # CSVファイルを開いて読み込む
    with open(csv_file_path, 'r') as csv_file:
        # CSVリーダーを作成
        csv_reader = csv.reader(csv_file)

        # 1行目をスキップ
        header = next(csv_reader, None)

        # 文字列と数値の列の値を取り出す
        for current_row, row in enumerate(csv_reader, start=2):  # 2から始めることで一番目の行をスキップ
            # 行の長さが文字列と数値の列のインデックスよりも長い場合
            if len(row) > max(string_column_index, numeric_column_index):
                # 文字列の列の値を取り出す
                string_value = row[string_column_index]

                # 数値の列の値を取り出し、整数に変換する
                try:
                    numeric_value = int(float(row[numeric_column_index]))
                except ValueError:
                    return f"At row {current_row}: Unable to convert numeric value to integer."

                # 特定の文字列の行を除外して表示
                if string_value not in exclude_strings:
                    pod_dict_key.append(string_value)  # pod名
                    pod_dict_value.append(numeric_value)  # CPU使用量
            else:
                return f"At row {current_row}: Row length is insufficient for columns."

    # 一時的なリストを作成し、重複を除いた一意のポッド名のリストを取得
    string_value_list = list(set(pod_dict_key))

    # データフレームの作成
    df = pd.read_csv("./monicsv/moni_1017_t.csv")
    del df["memory_usage(Mi)"]

    notification_messages = []
    # pod名で回す
    for pod in string_value_list:
        pod_value = []
        chunk_size = 12  # 60秒ごとにリストに入れる,shファイルで５秒ごとに記録するため12個

        # 特定のポッドに関連する行だけを取り出してリストに格納
        pod_value = [df.iloc[num, 2] for num in range(len(df)) if df.iloc[num, 1] == pod]

        # リストを特定のチャンクサイズごとに分割
        split_list = [pod_value[i:i + chunk_size] for i in range(0, len(pod_value), chunk_size)]
        # print(split_list)

        ave_list = []
        # 各チャンクの平均値を計算し、リストに格納
        for splited in split_list:
            ave = np.mean(np.array(splited))
            ave_list.append(ave)

        # 平均値の変動を確認してメッセージを出力
        for number, _ in enumerate(ave_list):
            if number == 0:
                continue

            #elif ave_list[number] == ave_list[number - 1]:
            #    notification_messages.append(f"{pod} is same")  # 平均値が同じ場合のメッセージ

            elif ave_list[number] < ave_list[number - 1]:
                notification_messages.append(f"{pod} is down")  # 平均値が前回よりも小さい場合のメッセージ

    return notification_messages


notification_messages = get_cpu_result()

# notification.py を呼び出し、Slack に通知
send_notification(notification_messages)