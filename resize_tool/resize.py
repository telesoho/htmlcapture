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
