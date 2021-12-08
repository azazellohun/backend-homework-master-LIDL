import logging, logging.config, sys, yaml
from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
from pathlib import Path

from reader.CsvReader import CsvReader, ConversionError


def main(*args):
    topic_name = 'events'    
    produce_records(topic_name, '/data')
    consum_records(topic_name)


def produce_records(topic_name, data_path):
    """ Produce and log records to topic reading from data_path. 
        :param topic_name: Name of the topic
        :param data_path: Data path
    """ 
    logger = logging.getLogger('producer')
    error_logger = logging.getLogger('error')

    producer = KafkaProducer(bootstrap_servers=['kafka:9094'],
                            api_version=(0,10,2),
                            value_serializer=lambda x: dumps(x).encode('utf-8')
                            )

    reader = CsvReader(data_path)
    
    # Sending events to kafka
    for record in reader:        
        if isinstance(record, ConversionError):
            error_logger.error(record.error_msg)
            continue
        
        transaction_id, event_type,date, store_number, item_number, value = record
        data = {
            'transaction_id':transaction_id,
            'event_type': event_type, 
            'date': date.strftime('%Y-%m-%dT%H:%M:%S'), 
            'store_number':store_number, 
            'item_number':item_number, 
            'value':value}
        producer.send(topic_name, value=data)
        logger.info(f'Data sent: {str(data)}')


def consum_records(topic_name):
    """ Consume and log records from topic. 
        :param topic_name: Name of the topic
    """ 

    logger = logging.getLogger('consumer')
    consumer = KafkaConsumer(topic_name,
                             bootstrap_servers=['kafka:9092'],
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='my-group',
                             value_deserializer=lambda x: loads(x.decode('utf-8'))
                            )

    for consumer_record in consumer:
        logger.info(f"Consumed: {consumer_record.value}")


def set_up_logging():
    logging_config_path = Path(__file__).parent.joinpath('log_conf.yaml')

    with open(logging_config_path, 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    logging.config.dictConfig(config)
    logger = logging.getLogger('importer')
    logger.info('Logging is now set up')


if __name__ == '__main__':    
    set_up_logging()
    rootLogger = logging.getLogger()

    try:        
        main(sys.argv)
    except:
        rootLogger.critical('', exc_info=True)