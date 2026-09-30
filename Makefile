.PHONY: up down init seed dbt-run dbt-test logs

up:
	docker compose up -d
	@echo "Airflow:  http://localhost:8080 (admin/admin)"
	@echo "MinIO:    http://localhost:9001 (minioadmin/minioadmin)"
	@echo "Trino:    http://localhost:8081"

down:
	docker compose down -v

init:
	docker compose run --rm airflow-init

seed:
	docker compose exec spark spark-submit /opt/spark/jobs/seed.py

dbt-run:
	docker compose exec airflow-scheduler bash -c "cd /opt/airflow/dbt && dbt run"

dbt-test:
	docker compose exec airflow-scheduler bash -c "cd /opt/airflow/dbt && dbt test"

logs:
	docker compose logs -f airflow-scheduler
