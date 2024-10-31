import logging

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt="%Y-%m-%dT%H:%MM:%S")
logger = logging.getLogger()

