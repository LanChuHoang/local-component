from confluent_kafka import Producer
import logging
import socket
from utils import test_case, handle_kafka_error
from confluent_kafka.schema_registry.schema_registry_client import SchemaRegistryClient


kafka_config = {
    "bootstrap.servers": "localhost:9092",
    "client.id": socket.gethostname(),
    "error_cb": handle_kafka_error,
}
test_topic = "test_topic"
producer = Producer(kafka_config)

schema_registry_config = {"url": "http://localhost:8085"}
schema_registry_client = SchemaRegistryClient(schema_registry_config)


@test_case
def test_produce_message():
    def on_delivery(err, msg):
        if err:
            handle_kafka_error(err)

    producer.produce(
        test_topic, key="test_key", value="test_value", on_delivery=on_delivery
    )
    producer.flush()


@test_case
def test_kafka_get_metadata():
    return producer.list_topics(timeout=5)


@test_case
def test_get_schema_list():
    return schema_registry_client.get_subjects()


def main():
    test_kafka_get_metadata()
    test_produce_message()
    test_get_schema_list()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
