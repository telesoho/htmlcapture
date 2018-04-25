import screenshot.HtmlCapture as hc
import distutils.dir_util as diru
import resize_tool.resize as resizetool
import errno
import os
import sys
import log


def remove_tree(folder):
    try:
        diru.remove_tree(folder)
    except OSError as exc:
        # if exc.errno != errno.EEXIST:
        #     raise
        pass
    
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def main():
    base_dir = get_script_path()
    log.init()
    if len(sys.argv) == 3:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        input_dir = os.path.join(base_dir, 'data/html')
        output_dir = os.path.join(base_dir, 'data/result')

    input_dir = os.path.abspath(input_dir)
    output_dir= os.path.abspath(output_dir)

    log.hclog.info("Capture HTML {} to {}".format(input_dir, output_dir))
   
    # copy src folder to reslut folder
    img_dir = os.path.join(input_dir, 'src/images')
    result_dir = output_dir
    remove_tree(result_dir)
    diru.copy_tree(img_dir, result_dir)

    # Remove all Material folder from result folder    
    for (dirpath, folders, filenames) in os.walk(result_dir):
        for folder in folders:
            material_folder = os.path.join(dirpath, folder, 'Material')
            remove_tree(material_folder)
        break

    # capture all htmls to pngs
    html_folder = input_dir
    screenshot_folder = os.path.join(result_dir , 'screenshot')
    log.hclog.info('Capture HTML starting... %s' % html_folder)
    remove_tree(screenshot_folder)
    os.makedirs(screenshot_folder)
    hc.walk_dir(html_folder, screenshot_folder)
    log.hclog.info('Capture HTML end %s' % screenshot_folder)

    # resize all pngs to jpeg clips for tmall
    log.hclog.info('Crop starting... %s' % screenshot_folder)
    resizetool.walk_dir(screenshot_folder, result_dir)
    log.hclog.info('Crop end %s' % result_dir)

    # remove screenshot folder

if __name__ == "__main__":
    try:
        main()
    except Exception, e:
        log.hclog.error(e)

    log.hclog.info('--ALL DONE--')
        