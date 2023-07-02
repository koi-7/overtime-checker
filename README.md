# overtime-checker

残業時間チェッカー

- 毎日の残業時間を Google カレンダーから読み込んで Notion DB に記録する
- 月末にはその月の残業時間のまとめを Slack で通知する

## Usage

### ダウンロード

``` bash
$ git clone https://github.com/koi-7/overtime-checker.git
```

### 必要なファイル準備

必要なファイルは `overtime-checker/data/` ディレクトリに入れておく

- `credentials.json`: Google の認証に必要
- `google_token.json`: Google の認証に必要（ブラウザがない場合、適当に用意する）
- `database_url`: Notion DB の書き込みに必要
- `notion_token`: Notion の認証に必要
- `slack_token`: Slack の認証に必要

hint: ディレクトリ構成

```
overtime-checker
|-- README.md
|-- data
|   |-- credentials.json
|   |-- database_url.txt
|   |-- google_token.json
|   |-- notion_token
|   `-- slack_token
|-- overtime-checker
|   |-- __init__.py
|   |-- __main__.py
|   |-- __pycache__
|   |-- calendar_reader.py
|   |-- functions.py
|   |-- notion_operator.py
|   `-- slack_notifier.py
`-- requirements.txt
```

### requirements

必要なライブラリを入れる

``` bash
$ pip3 install -r requirements.txt
```

### Cron の設定例

毎晩 23 時 55 分にプログラムが動くようにする（タイムゾーン、PYTHONPATH の設定を忘れないように注意）

``` bash
$ crontab -e
```

```
CRON_TZ=Asia/Tokyo

PYTHONPATH=$PYTHONPATH:/opt/overtime-checker/
55 23 * * * /usr/bin/python3 -m overtime-checker
```

タイムゾーンを反映させるために crond を再起動する

``` bash
$ systemctl restart cron
```
