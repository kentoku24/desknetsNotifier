# desknetsNotifier
デスクネッツのスケジュールをpush通知します

- 使い方
  * credentials.template.yamlをcredentials.yamlにリネーム、必要な情報を記入し、このディレクトリ内でpython jmottoScraper.pyを実行してください。
    - JMOTTO_GROUP JMOTTO_USERNAME JMOTTO_PASSWORD これらには自分のJmottoの情報を記入してください。
    - SLACK_TOKEN は[こちら](https://api.slack.com/custom-integrations/legacy-tokens)から取得できます
    - SLACK_USER_ID は [users.info](https://api.slack.com/methods/users.info/test) あたりで自分のユーザ名リンクをクリックすると欄が埋まるので、それを使うと良いと思います。
  * 

- 前提条件
  * Chrome Canaryを導入したWindows端末で動作確認をしていますので、Windows版のChromeDriverを同梱しています。
  お使いのOSに対応する[ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) をこのディレクトリに置けば動くかもしれません。

- tips
  * pythonのREPLにライブラリとして放り込んで使う事もできます。
  ```python
  import jmottoScraper as j
  d = j.makeDriver(headless=False)
  j.loginDesknets(d)
  s = j.getSchedule(d)
  ```