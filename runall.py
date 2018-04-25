import screenshot.HtmlCapture as hc
import distutils.dir_util as diru
import resize_tool.resize as resizetool
import errno
import os
import sys
import log

import shutil

import zipfile

def unzip_file(zip_file, dest_dir):
    zip_ref = zipfile.ZipFile(zip_file, 'r')
    zip_ref.extractall(dest_dir)
    zip_ref.close()

def zipdir(path, zip_file):
    zipf = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

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
        input_zip = sys.argv[1]
        output_zip = sys.argv[2]

    input_dir = os.path.join(base_dir, 'data/html')
    output_dir = os.path.join(base_dir, 'data/result')

    data_path = os.path.join(base_dir, 'data')

    if(os.path.isfile(input_zip)):
        if(os.path.isdir(input_dir)):
            shutil.rmtree(input_dir, ignore_errors=True)
        unzip_file(input_zip, data_path)

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
    remove_tree(screenshot_folder)

    # zip result to zip
    zipdir(result_dir, output_zip)

    log.hclog.info('RESULT_FILE:%s' % output_zip)

if __name__ == "__main__":
    try:
        main()
    except Exception, e:
        log.hclog.error(e)

    log.hclog.info('--ALL DONE--')
        