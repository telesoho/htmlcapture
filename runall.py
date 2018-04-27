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
    '''
    Unzip an zip file to destination directory.
    '''
    zip_ref = zipfile.ZipFile(zip_file, 'r')
    zip_ref.extractall(dest_dir)
    zip_ref.close()

def zip_folder(folder_path, zip_file):
    """Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """
    parent_folder = os.path.dirname(folder_path)
    # Retrieve the paths of the folder contents.
    contents = os.walk(folder_path)
    try:
        zip_file = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
        for root, folders, files in contents:
            # Include all subfolders, including empty ones.
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(parent_folder + '\\',
                                                      '')
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(parent_folder + '\\',
                                                      '')
                zip_file.write(absolute_path, relative_path)
        log.hclog.info("'%s' created successfully." % zip_file)
    except IOError, message:
        log.hclog.error(message)
    except zipfile.BadZipfile, message:
        log.hclog.error(message)
    finally:
        zip_file.close()


def remove_tree(folder):
    '''
    Remove tree prevent all error message been shown.
    '''
    try:
        diru.remove_tree(folder)
    except OSError as exc:
        pass

    
def get_script_path():
    '''
    Get start python script file's path
    '''
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def copy_dir_struct(src_dir, dest_dir):
    '''
    Copy directory struct to other folder.
    '''
    src_dir = os.path.abspath(src_dir)
    dest_dir = os.path.abspath(dest_dir)
    for root, subdirs, files in os.walk(src_dir):
        root_relpath = os.path.relpath(root, src_dir)
        new_root_path = os.path.realpath(os.path.join(dest_dir, root_relpath))
        if not os.path.isdir(new_root_path):
            os.makedirs(new_root_path)


def main():
    BASE_DIR = get_script_path()
    
    # Initialize log.
    log.init()

    # Get input zip and output zip filename from command line argument.
    if len(sys.argv) == 3:
        input_zip = sys.argv[1]
        output_zip = sys.argv[2]

    # Set default data folder.
    input_dir = os.path.join(BASE_DIR, 'data/html')
    output_dir = os.path.join(BASE_DIR, 'data/result')
    data_path = os.path.join(BASE_DIR, 'data')

    input_dir = os.path.abspath(input_dir)
    output_dir= os.path.abspath(output_dir)
    data_path = os.path.abspath(data_path)

    # unzip input zip to input directory.
    if(os.path.isfile(input_zip)):
        # remove input directory while exist
        if(os.path.isdir(input_dir)):
            shutil.rmtree(input_dir, ignore_errors=True)
        unzip_file(input_zip, data_path)


    log.hclog.info("Capture HTML {} to {}".format(input_dir, output_dir))
   
    # copy src folder to reslut folder
    img_dir = os.path.join(input_dir, 'src/images')
    result_dir = output_dir
    remove_tree(result_dir)
    shutil.copytree(img_dir, result_dir)

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
    os.system('zip -r {} {}'.format(output_zip, result_dir))

    log.hclog.info('RESULT_FILE:%s' % output_zip)

if __name__ == "__main__":
    try:
        main()
    except Exception, e:
        log.hclog.error(e)

    log.hclog.info('--ALL DONE--')
        