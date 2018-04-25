
import os
from PIL import Image

def crop(Path, input, height, width, k, page, area):
    im = Image.open(input)
    imgwidth, imgheight = im.size
    for i in range(0,imgheight,height):
        for j in range(0,imgwidth,width):
            box = (j, i, j+width, i+height)
            a = im.crop(box)
            try:
                o = a.crop(area)
                o.save(os.path.join(Path,"PNG","%s" % page,"IMG-%s.png" % k))
            except:
                pass
            k +=1


def convert2Jpeg(in_file, out_file):
    im = Image.open(in_file)
    rgb_im = im.convert('RGB')
    rgb_im.save(out_file)

