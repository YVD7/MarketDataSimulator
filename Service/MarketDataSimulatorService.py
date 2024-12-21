import json
import yaml
from kafka import KafkaProducer

yml_file = "config.yml"
with open(yml_file, "r") as file:
    config = yaml.safe_load(file)
kafka_config = config['kafka_conf']

class MarketDataSimulatorService:
    def __init__(self):
        self.producer_config = {
                'bootstrap_servers': kafka_config['bootstrap_servers']
            }

    def kafka_producer(self, data, topic):
        key = data['ticker']
        print(data)
        producer = KafkaProducer(
            bootstrap_servers=self.producer_config['bootstrap_servers'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        producer.send(topic, value=data, key=key.encode('utf-8'))
        producer.flush()
        producer.close()



