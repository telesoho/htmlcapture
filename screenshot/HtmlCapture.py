"""
This script uses a simplified version of the one here:
https://snipt.net/restrada/python-selenium-workaround-for-full-page-screenshot-using-chromedriver-2x/

It contains the *crucial* correction added in the comments by Jason Coutu.
"""
import sys
import util
import os
from selenium import webdriver
from pyvirtualdisplay import Display
from PIL import Image
import log

def walk_dir(mypath, out_path):
    display = Display(visible=0, size=(1024, 768))
    display.start()

    chromedriver = "/usr/local/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.set_window_size(1024, 768)
    out_path = os.path.abspath(out_path)

    for (dirpath, dirnames, filenames) in os.walk(mypath, ):
        # print dirpath
        # print dirnames
        # print filenames
        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            basefilename = os.path.splitext(filename)[0]
            if ext == '.html':
                url = 'file:///' + os.path.abspath(os.path.join(dirpath, filename))
                log.hclog.info('Rendering %s' % url)
                out_png = os.path.join(out_path, basefilename + '.png')
                driver.get(url)
                util.fullpage_screenshot(driver, out_png)
        break
    
    driver.quit()
    display.stop()

if __name__ == "__main__":
    # unittest.main(argv=[sys.argv[0]])
    walk_dir('../data/html/', '../data/screenshot/')

