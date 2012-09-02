# textpack.py

Texture Atlas用の画像を生成するPythonスクリプト。

* 複数のpngファイルを1枚のpng画像に配置する。
* Windows7 x64 + Python 2.6.6 + PIL で動作確認。

  Usage: texpack.py [options]
  
  Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -i WILDCARD, --infile=WILDCARD
                          入力PNGファイル名(ワイルドカード指定) [default: .\*.png]
    -o FILE, --outpng=FILE
                          出力PNGファイル名 [default: out.png]
    -x FILE, --outxml=FILE
                          出力XMLファイル名 [default: out.xml]
    -m MODE, --mode=MODE  配置モード ('blf' or 'nextfit') [default: blf]
    -b NUM, --border=NUM  各画像の隙間のドット数 [default: 2]
    -t, --trim            各画像を配置前にトリミングする
    --sortoff             各画像を配置前にソートしない
    --show                結果画像を表示
    -v, --verbose         処理内容を詳細表示 [default]
    -q, --quiet           処理内容を詳細表示しない
    --debug               デバッグメッセージを表示

## 履歴

* 0.0.2  2012/09/02  BLF法での配置処理を追加。
* 0.0.1  2012/09/01  Next-Fit法での配置処理のみ実装。

