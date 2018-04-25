import logging

def init():
    global hclog
    hclog = logging.getLogger('htmlcapture')
    hdlr = logging.FileHandler('htmlcapture.log', mode='w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    hclog.addHandler(hdlr)
    hclog.addHandler(logging.StreamHandler())
    hclog.setLevel(logging.INFO)
    
