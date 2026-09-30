# End-to-End-Data-Lakehouse-Airflow-dbt-Iceberg-Trino-
End-to-End Data Lakehouse (Airflow + dbt + Iceberg + Trino)  Пайплайн от сырых данных (S3) до BI-дашбордов с Medallion-архитектурой (Bronze → Silver → Gold).
# 🏔 Lakehouse E-commerce

End-to-end Lakehouse: MinIO → Spark → Iceberg → dbt → Trino.

## Стек
- **Storage:** MinIO (S3-compatible), Apache Iceberg
- **Compute:** Spark 3.5, Trino 449
- **Orchestration:** Airflow 2.9
- **Transform:** dbt-trino
- **Metastore:** Hive Metastore + Postgres

## Архитектура
