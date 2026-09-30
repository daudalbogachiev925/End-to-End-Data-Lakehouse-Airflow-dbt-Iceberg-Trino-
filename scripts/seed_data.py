"""Генерирует сырые события в MinIO (bucket raw-bucket/events/)."""
import json, random, uuid
from datetime import datetime, timedelta
from faker import Faker
import boto3

fake = Faker()

s3 = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)

EVENT_TYPES = ["page_view", "add_to_cart", "purchase", "login"]
COUNTRIES = ["US", "DE", "FR", "RU", "BR", "IN"]

def make_event(ts):
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": random.randint(1, 10_000),
        "event_type": random.choice(EVENT_TYPES),
        "product_id": random.randint(1, 500),
        "price": round(random.uniform(5, 2000), 2),
        "country": random.choice(COUNTRIES),
        "timestamp": ts.isoformat(),
    }

def upload_day(day):
    key = f"events/date={day.strftime('%Y-%m-%d')}/events.json"
    rows = []
    base = datetime.combine(day, datetime.min.time())
    for _ in range(5000):
        ts = base + timedelta(seconds=random.randint(0, 86399))
        rows.append(make_event(ts))
    body = "\n".join(json.dumps(r) for r in rows)
    s3.put_object(Bucket="raw-bucket", Key=key, Body=body.encode())
    print(f"✅ uploaded s3://raw-bucket/{key} ({len(rows)} rows)")

if __name__ == "__main__":
    today = datetime.utcnow().date()
    for i in range(7):
        upload_day(today - timedelta(days=i))
    print("Done.")
