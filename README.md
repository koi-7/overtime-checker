# overtime-checker

今月の残業時間を算出する。

## 使い方

### 準備

日頃から残業時間を Google カレンダーに記録する（予定名は「残業」にする）

以下スクリプト実行のための準備

1. Google Calender の API を有効にする
1. API を叩くための json ファイル（credentials.json）を入手する
1. 入手した json ファイルを auth フォルダに入れる

### 実行

``` bash
$ cd /path/to/ovetime-checker/
$ python3 -m overtime-checker
```

※初回実行時には実行を許可するための URL に誘導されたりする
