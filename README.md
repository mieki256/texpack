# texpack.py

Texture Atlas用の画像を生成するPythonスクリプト。

* 複数のpngファイルを1枚のpng画像に配置する。
* Windows7 x64 + Python 2.6.6 + PIL で動作確認。

## 使い方

    Usage:
        texpack.py -i img\*.png -o out.png -x out.xml
        texpack.py --help
    
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

- - - -

## 履歴

2012/09/13 ver 0.0.5

* xml出力時、ファイル名でソートできてなかったバグを修正。

2012/09/07 ver 0.0.4

* PEP8に従ってソースを整形。

2012/09/07 ver 0.0.3

* trim有効時のxml出力を修正。
* xml出力時、ファイル名でソートしてから出力するようにした。

2012/09/02 ver 0.0.2

* BLF法での配置処理を追加。

2012/09/01 ver 0.0.1

* Next-Fit法での配置処理のみ実装。

- - - -

## 結果画像の例

* ギッシリ詰め込んだ感じの結果サンプル (--trim --mode blf)

[![ギッシリ詰め込んだ感じの結果サンプル](https://dl.dropbox.com/u/84075965/screenshot/texpack/out2.png)](https://dl.dropbox.com/u/84075965/screenshot/texpack/out2.png)

[出力xmlのサンプル](https://dl.dropbox.com/u/84075965/screenshot/texpack/out2.xml)

* 賢くない感じの詰め込み結果サンプル (--sortoff --mode nextfit)

[![賢くない感じの詰め込み結果サンプル](https://dl.dropbox.com/u/84075965/screenshot/texpack/out1.png)](https://dl.dropbox.com/u/84075965/screenshot/texpack/out1.png)

