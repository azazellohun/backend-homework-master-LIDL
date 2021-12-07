import logging, logging.config, sys, yaml
from kafka import KafkaProducer, KafkaConsumer
from time import sleep
from json import dumps, loads
from os import path


def main(*args):
    logger = logging.getLogger('importer')
    logger.info('test')


def set_up_logging():
    logging_config_path = path.join(path.dirname(path.abspath(__file__)), 'log_conf.yaml')

    with open(logging_config_path, 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    logging.config.dictConfig(config)
    logger = logging.getLogger('importer')
    logger.info('Logging is now set up')


if __name__ == '__main__':    
    set_up_logging()

    try:        
        main(sys.argv)
    except:
        logging.critical('', exc_info=True)