<p align="center">
  <img src="https://github.com/koi-7/overtime-checker/assets/61448492/651d4b05-3008-42d3-afce-cbf7a89f7148">
</p>

# overtime-checker

残業時間チェッカー

- 毎日の残業時間を Google カレンダーから読み込んで Notion DB に記録する
- 月末にはその月の残業時間のまとめを Slack で通知する

## Usage

### ダウンロード

``` bash
$ cd ~
$ git clone https://github.com/koi-7/overtime-checker.git
```

### 必要なファイル準備

必要なファイルは `overtime-checker/config/` ディレクトリに入れておく

- `credentials.json`: Google の認証に必要
- `google_token.json`: Google の認証に必要（ブラウザがない場合、適当に用意する）
- `config.ini`: `sample.ini` を参考に作成する

### requirements

``` bash
$ cd overtime-checker
$ pip3 install -r requirements.txt
```

### 好きな場所に配置（例: `/opt/` 配下）

``` bash
$ cd ~
$ sudo mv overtime-checker/ /opt/
```

## Example

毎晩 23 時 55 分にプログラムが動くように Cron を設定する（タイムゾーン、PYTHONPATH の設定を忘れないように注意）

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
$ sudo systemctl restart cron
```
