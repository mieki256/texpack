#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python; Encoding: utf8n -*-

"""
Texture Atlas用の画像を生成するPythonスクリプト。

* 複数のpngファイルを1枚のpng画像に配置する。
* Windows7 x64 + Python 2.7.3 + PIL で動作確認。

usage:
    python texpack.py -i *.png -o out.png -x out.xml
    python texpack.py --help

履歴
----

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

"""


from optparse import OptionParser
import glob
from PIL import Image
import os
import sys
from operator import attrgetter
from collections import namedtuple

VER = "0.0.4"  # バージョン番号


def chk_arg():
    """コマンドラインオプションを解析."""

    parser = OptionParser(version="%prog " + VER)

    parser.set_defaults(verbose=True, debug=False, border=2,
                        mode="blf",
                        infile=".\\*.png",
                        outpng="out.png",
                        outxml="out.xml",
                        trim=False, show=False, sortoff=False)

    parser.add_option("-i", "--infile", metavar="WILDCARD",
                      help=u"入力PNGファイル名(ワイルドカード指定) [%default]")
    parser.add_option("-o", "--outpng", metavar="FILE",
                      help=u"出力PNGファイル名 [%default]")
    parser.add_option("-x", "--outxml", metavar="FILE",
                      help=u"出力XMLファイル名 [%default]")
    parser.add_option("-m", "--mode", metavar="MODE", type="choice",
                      choices=['blf', 'nextfit'],
                      help=u"配置モード(blf|nextfit) [%default]")
    parser.add_option("-b", "--border", type="int", metavar="NUM",
                      help=u"各画像の隙間のドット数 [default: %default]")
    parser.add_option("-t", "--trim", action="store_true",
                      help=u"各画像を配置前にトリミングする")
    parser.add_option("--sortoff", action="store_true",
                      help=u"各画像を配置前にソートしない")
    parser.add_option("--show", action="store_true",
                      help=u"結果画像を表示")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      help=u"処理内容を詳細表示 [default]")
    parser.add_option("-q", "--quiet", dest="verbose", action="store_false",
                      help=u"処理内容を詳細表示しない")
    parser.add_option("--debug", action="store_true",
                      help=u"デバッグメッセージを表示")

    (opts, args) = parser.parse_args()
    if len(args) != 0:
        parser.print_help()
        sys.exit(1)

    if not (opts.mode == "nextfit" or opts.mode == "blf"):
        parser.error("Unknown Mode = " + opts.mode)

    if opts.verbose:
        print "Input File : %s" % (opts.infile)
        print "Output PNG : %s" % (opts.outpng)
        print "Output XML : %s" % (opts.outxml)
        print "Mode : %s" % (opts.mode)

    return opts


class ImageRect:
    """画像一枚分の情報を格納するクラス"""

    def __init__(self, fn, border, i):
        self.name, self.ext = os.path.splitext(os.path.basename(fn))

        self.img = Image.open(fn)
        self.img.load()

        self.fn = fn
        self.idx = i
        self.border = int(border)

        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.rw = 0
        self.rh = 0
        self.set_wh()

        self.trim_enable = False
        self.frame_x = 0
        self.frame_y = 0
        self.frame_w = self.rw
        self.frame_h = self.rh

    def set_wh(self):
        """幅と高さを取得・記録する"""
        self.rw = self.img.size[0]
        self.rh = self.img.size[1]
        self.w = self.rw + (self.border * 2)
        self.h = self.rh + (self.border * 2)

    def trim(self):
        """最小サイズでトリミング"""
        tbox = self.img.getbbox()
        if tbox[0] != 0 or tbox[1] != 0 or \
                tbox[2] != self.rw or tbox[3] != self.rh:
            self.trim_enable = True
            self.frame_x = - tbox[0]
            self.frame_y = - tbox[1]
            self.img = self.img.crop(tbox)
            self.set_wh()

    def dump(self):
        """画像情報を出力"""
        s = "%4d %s %s " % (self.idx, self.name, self.fn)
        s += " x,y,w,h=%d,%d,%d(%d),%d(%d)" % \
            (self.x, self.y, self.w, self.rw, self.h, self.rh)
        if self.trim_enable:
            s += " trim fX,fY,fW,fH=%d,%d,%d,%d" % \
                (self.frame_x, self.frame_y, self.frame_w, self.frame_h)
        print s


def dump_all_image_info(lis):
    """全画像の情報をダンプ"""
    for im in lis:
        im.dump()


def open_image(opts):
    """画像ファイル群を開く."""

    # ファイル一覧を取得
    filelist = glob.glob(opts.infile)
    if len(filelist) <= 0:
        sys.exit("Error : Not Found File")

    # 画像を開いて画像情報を記録
    lis = []
    for i, f in enumerate(filelist):
        lis.append(ImageRect(f, opts.border, i))

    if opts.verbose:
        dump_all_image_info(lis)

    # 各画像を最小サイズでトリミング
    if opts.trim:
        for im in lis:
            im.trim()

    # 縦幅、横幅でソート
    if not opts.sortoff:
        sortlis_h = sorted(lis, key=attrgetter('h', 'w'), reverse=True)
        lis = sortlis_h
        if opts.debug:
            print "# sort"
            dump_all_image_info(lis)

    # 画像を配置
    dw = 0
    dh = 0
    r_lis = []
    if opts.mode == "blf":
        (dw, dh, r_lis) = set_pos_blf(lis, opts.debug)
    else:
        (dw, dh, r_lis) = set_pos_nextfit(lis, opts.debug)

    # 画像を生成
    bkimg = Image.new('RGBA', (dw, dh), (0, 0, 0, 0))
    for im in r_lis:
        bkimg.paste(im.img, (im.x + im.border, im.y + im.border))

    # 画像リストを元の並びにソート
    if not opts.sortoff:
        sortlis_h = sorted(lis, key=attrgetter('fn'), reverse=False)
        lis = sortlis_h

    # 確認のために各画像の配置状態をダンプ
    if opts.verbose:
        print "# Result"
        dump_all_image_info(lis)

    # 画像を保存
    bkimg.save(opts.outpng, 'PNG')
    if opts.verbose:
        print "output %s" % (opts.outpng)

    # xmlを出力
    output_xml(opts.outxml, opts.outpng, lis)
    if opts.verbose:
        print "output %s" % (opts.outxml)

    # 確認のために結果画像を関連付けされたアプリで開く
    if opts.show:
        bkimg.show()


def output_xml(outfn, pngfn, lis):
    """xmlを出力"""

    png_basename = os.path.basename(pngfn)
    f = open(outfn, "w")
    f.write(u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write(u"<TextureAtlas imagePath=\"%s\">\n" % (png_basename))

    for img in lis:
        x = img.x + img.border
        y = img.y + img.border
        s = u"    <SubTexture name=\"%s\"" % (img.name)
        s += u" x=\"%d\" y=\"%d\"" % (x, y)
        s += u" width=\"%d\" height=\"%d\"" % (img.rw, img.rh)
        if img.trim_enable:
            s += " frameX=\"%d\" frameY=\"%d\"" % (img.frame_x, img.frame_y)
            s += " frameWidth=\"%d\" frameHeight=\"%d\"" % \
                (img.frame_w, img.frame_h)

        s += u"/>\n"
        f.write(s)

    f.write(u"</TextureAtlas>\n")
    f.close()


def set_pos_nextfit(lis, dbg):
    """Next-Fit法で配置"""

    aw = 2
    ah = 2
    i = 0
    dx = 0
    dy = 0
    dh = 0
    while i < len(lis):
        im = lis[i]

        if (dx + im.w) <= aw:
            # 横方向に置ける場合
            im.x = dx
            im.y = dy
            dx += im.w
            if dh < im.h:
                dh = im.h
            if dbg:
                im.dump()
            i += 1
            continue

        # 横方向に置けない場合は次のレベルへ
        dx = 0
        dy += dh
        dh = 0
        if (dy + im.h) <= ah and (dx + im.w) <= aw:
            # 縦方向に置ける場合
            im.x = dx
            im.y = dy
            dx += im.w
            if dh < im.h:
                dh = im.h
            if dbg:
                im.dump()
            i += 1
            continue

        # 横にも縦にも置けない。
        # 転送先画像サイズを大きくして最初から配置し直し。
        if aw >= ah:
            ah *= 2
        else:
            aw *= 2
        if dbg:
            print "dest image size = (%d,%d)" % (aw, ah)
        i = 0
        dx = 0
        dy = 0
        dh = 0

    return (aw, ah, lis)


def set_pos_blf(lis, dbg):
    """BLF法で配置"""

    Blp = namedtuple('Blp', 'x y w h')
    aw = 2
    ah = 2

    bp = [Blp(0, 0, 0, 0)]
    num1 = range(len(lis))
    num2 = []

    while len(num1) > 0:
        c = lis[num1[0]]
        minx = sys.maxint
        miny = sys.maxint

        # 矩形を配置できそうなBL安定点を探す
        found_idx = -1
        for i, s in enumerate(bp):
            if c.w < s.w or c.h < s.h:
                continue

            x1 = s.x
            y1 = s.y
            x2 = s.x + c.w
            y2 = s.y + c.h
            if y1 < miny or (y1 == miny and x1 < minx):
                if x2 > aw or y2 > ah:
                    # 配置先エリアをオーバーしてる。コレジャナイ
                    continue

                for n in num2:
                    d = lis[n]
                    if (x1 < (d.x + d.w) and d.x < x2 and
                            y1 < (d.y + d.h) and d.y < y2):
                        # 衝突している矩形がある。コレジャナイ
                        break
                else:
                    # 衝突している矩形は無いので、配置予定座標を記憶
                    minx = x1
                    miny = y1
                    found_idx = i

        if minx >= sys.maxint or miny >= sys.maxint:
            # 矩形が入る場所が見つからなかった
            # 転送先画像サイズを拡大して最初からやり直し
            if aw >= ah:
                ah *= 2
            else:
                aw *= 2
            if dbg:
                print "dest image size = (%d,%d)" % (aw, ah)
            bp = [Blp(0, 0, 0, 0)]
            num1 = range(len(lis))
            num2 = []
            continue

        # 入る場所があったので配置
        c.x = minx
        c.y = miny
        num2.append(num1[0])
        del num1[0]

        # 配置に使ったBL安定点候補はもう使えないはずなので、除去する
        if found_idx >= 0:
            del bp[found_idx]

        # エリア枠と矩形で作れるBL安定点候補を追加登録
        cx1 = c.x
        cx2 = c.x + c.w
        cy1 = c.y
        cy2 = c.y + c.h
        tblp = []
        tblp.append(Blp(cx2, 0, 0, cy1))
        tblp.append(Blp(0, cy2, cx1, 0))

        # 現矩形と配置済み矩形との間で作れるBL安定点候補を追加登録
        for j in range(len(num2)):
            p = lis[num2[j]]
            px1 = p.x
            px2 = p.x + p.w
            py1 = p.y
            py2 = p.y + p.h

            # 現矩形が配置済み矩形の左側にある場合
            if cx2 <= px1 and cy2 > py2:
                t = (cy1 - py2) if (cy1 > py2) else 0
                tblp.append(Blp(cx2, py2, px1 - cx2, t))

            # 現矩形が配置済み矩形の右側にある場合
            if px2 <= cx1 and py2 > cy2:
                t = (py1 - cy2) if (py1 > cy2) else 0
                tblp.append(Blp(px2, cy2, cx1 - px2, t))

            # 現矩形が配置済み矩形の上側にある場合
            if cy2 <= py1 and cx2 > px2:
                t = (cx1 - px2) if (cx1 > px2) else 0
                tblp.append(Blp(px2, cy2, t, py1 - cy2))

            # 現矩形が配置済み矩形の下側にある場合
            if py2 <= cy1 and px2 > cx2:
                t = (px1 - cx2) if (px1 > cx2) else 0
                tblp.append(Blp(cx2, py2, t, cy1 - py2))

        # 配置済み矩形群と、得られたBL安定点候補が重なっていないなら、
        # BL安定点候補として登録する
        for b in tblp:
            if b.x < 0 or b.x >= aw or b.y < 0 or b.y >= ah:
                # そもそも配置先エリアをオーバーしてる
                continue

            for n in num2:
                d = lis[n]
                if (d.x <= b.x and b.x < (d.x + d.w) and
                        d.y <= b.y and (b.y < d.y + d.h)):
                    # 配置済み矩形の中にBL安定点候補が入っている
                    break
            else:
                # BL安定点候補として使えそうなので追加登録
                bp.append(Blp(b.x, b.y, b.w, b.h))

    return (aw, ah, lis)


def main():
    """メイン処理"""

    opts = chk_arg()
    open_image(opts)


if __name__ == '__main__':
    main()
