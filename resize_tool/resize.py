# coding=utf-8
import os
import errno
import log

from PIL import Image

def crop(Path, input, height, width):
    im = Image.open(input)
    imgwidth, imgheight = im.size
    if imgwidth < width:
        width = imgwidth

    k = 1
    for i in range(0,imgheight,height):
        bottom = i + height
        if bottom > imgheight:
            bottom = imgheight
        box = (0, i, width, bottom)
        a = im.crop(box)
        try:
            a.convert('RGB')
            filename = os.path.splitext(os.path.basename(input))[0]
            output_filename = os.path.join(Path, filename + "_%s.jpeg" % k)
            a.save(output_filename)
            log.hclog.info('crop to %s' % output_filename)
        except Exception, e:
            print e
            pass
        k +=1

def crop2jpeg(in_file, target_folder):
    print in_file, target_folder
    crop(target_folder, in_file, 1540, 790)
    return

def walk_dir(in_path, out_path):
    out_path = os.path.abspath(out_path)
    for (dirpath, dirnames, filenames) in os.walk(in_path):
        for filename in filenames:           
            ext = os.path.splitext(filename)[1].lower()
            if ext in '.png .jpg .jpeg':
                in_file = os.path.abspath(os.path.join(dirpath,filename))
                basefilename = os.path.splitext(os.path.basename(in_file))[0]
                target_folder = os.path.join(out_path, basefilename, 'Material')
                try:
                    os.makedirs(target_folder)
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
                    pass
                crop2jpeg(in_file, target_folder)
        break



def main():
    # rem ++++++++++++++++++++++++++++++++++++++++
    # rem + 第1引数：ソースフォルダ(必須)
    # rem ++++++++++++++++++++++++++++++++++++++++
    # set _resize_source_dir=%_SCREENSHOT_OUTPUT_DIR%
    _resize_source_dir='/home/hilines/prjs/HtmlCapture/data/screenshot/'

    # rem ++++++++++++++++++++++++++++++++++++++++
    # rem + 第2引数：出力フォルダ(必須)
    # rem +++++++++++++++++++++++++++++++++++++++
    # set _resize_output_dir=%_BASE_DIR%\data\resize
    _resize_output_dir = '/home/hilines/prjs/HtmlCapture/data/resize/'

    # rem ++++++++++++++++++++++++++++++++++++++++
    # rem + 第3引数：リサイズフラグ(必須) ※幅790にリサイズする
    # rem ++++++++++++++++++++++++++++++++++++++++
    # set _resize_flag=false
    _resize_flag='false'

    # rem ++++++++++++++++++++++++++++++++++++++++
    # rem + 第4引数：トリミングフラグ(必須) ※縦1540超える場合、1540毎にトリミングする。横が790までトリミングする
    # rem ++++++++++++++++++++++++++++++++++++++++
    # set _resize_trim_flag=true
    _resize_trim_flag='true'

    # rem ****** 以降は実行コマンドです。必要のない限り修正しないでください。******
    # set _JARPATH=.\resize_tool\libs\resize.jar
    #  %_JAVAPATH% -jar %_JARPATH% %_resize_source_dir% %_resize_output_dir% %_resize_flag% %_resize_trim_flag%
    cmd = 'java -jar ./resize_tool/libs/resize.jar {0} {1} {2} {3}'.format(
        _resize_source_dir,
        _resize_output_dir,
        _resize_flag,
        _resize_trim_flag
    )

    walk_dir(_resize_source_dir, _resize_output_dir)

if __name__ == '__main__':
    main()