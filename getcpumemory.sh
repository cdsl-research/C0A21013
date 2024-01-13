#!/bin/bash
# CSVファイルのヘッダを作成
echo "timestamp,pod,cpu_usage(m),memory_usage(Mi)" > monicsv/moni_1017_t.csv
count=0
while true; do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    # すべてのPodのリソース使用量を取得し、単位を取り除く
    kubectl top pod -n sock-shop --no-headers 2>/dev/null | while read -r pod cpu_usage memory_usage; do
        cpu_usage=$(echo $cpu_usage | tr -d 'm')
	    memory_usage=$(echo $memory_usage | tr -d 'Mi')
        echo "$timestamp,$pod,$cpu_usage" >> monicsv/moni_1017_t.csv
    done
    count=`expr $count + 1`
    if [ $count -eq 60 ]; then
         break
    fi
    sleep 5  # 5秒待機

    #echo >> monicsv/moni_1017_t.csv  #何行ずつ取り出すときに空行があるとエラーができので消した方が良い
done
