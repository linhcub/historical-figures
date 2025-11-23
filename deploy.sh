ssh ubuntu@140.245.117.24 "cd historical-figures && git pull && sudo docker-compose build && sudo docker-compose down && sudo docker-compose up -d"
ssh ubuntu@140.245.117.24 "sudo docker exec historical_figures_api python scripts/import_csv_to_db.py historical_figures_modern_era.csv"
