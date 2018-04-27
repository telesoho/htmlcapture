"""
"""
import sys
import util
import os
from selenium import webdriver
from pyvirtualdisplay import Display
from PIL import Image
import log

def walk_dir(mypath, out_path):
    '''
    Render HTML page in @mypath, and capture whole screenshot to @out_path
    '''
    # Use virtual display to prevent browser been shown.
    display = Display(visible=0, size=(1024, 768))
    display.start()

    # Setup chrome browser driver
    chromedriver = "/usr/local/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.set_window_size(1024, 768)
    out_path = os.path.abspath(out_path)

    for (dirpath, dirnames, filenames) in os.walk(mypath):
        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            basefilename = os.path.splitext(filename)[0]
            if ext == '.html':
                url = 'file:///' + os.path.abspath(os.path.join(dirpath, filename))
                log.hclog.info('Rendering %s' % url)
                # Open HTML in browser
                driver.get(url)
                # Capture screenshot to .png file
                out_png = os.path.join(out_path, basefilename + '.png')
                util.fullpage_screenshot(driver, out_png)
        break
    
    driver.quit()
    display.stop()



