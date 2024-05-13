from faker import Faker
import random
import pandas as pd
from common.database_connector import factory

# Connect to PostgreSQL
conn = factory.get_connector(
    database_type="postgres",
    # database_name="sendgrid",
    database_name="postgres",
    username="postgres",
    # password="0cTKyRRCJi",
    password="postgres",
    host="localhost",
    port="5435",
)
table_name = "sendgrid"
schema_name = None

# Create Faker instance
fake = Faker()

# Define batch size
total_records = 10**6 * 5
batch_size = 10**4 * 2


def gen_mock_record():
    return {
        "sg_event_id": fake.uuid4(),
        "email": fake.email(),
        "event": random.choice(
            [
                "proccessed",
                "dropped",
                "delivered",
                "deferred",
                "bounce",
                "blocked",
                "open",
                "click",
                "spamreport",
                "unsubscribe",
                "group_unsubscribe",
                "group_resubscribe",
            ]
        ),
        "attempt": random.randint(1, 100),
        "response": fake.sentence(),
        "sg_message_id": fake.uuid4(),
        "sg_template_id": fake.uuid4(),
        "sg_template_name": fake.word(),
        "smtp_id": fake.uuid4(),
        "timestamp": fake.date_time_between(start_date="-1y", end_date="now"),
        "tls": random.randint(0, 1),
    }


# Generate and insert mock data in batches
for num_inserted in range(0, total_records, batch_size):
    data_batch = []
    for _ in range(batch_size):
        mock_record = gen_mock_record()
        data_batch.append(mock_record)

    df = pd.DataFrame(data_batch)
    conn.insert(df, table=table_name, schema=schema_name)
    print(f"Inserted {num_inserted + batch_size}/{total_records}")
