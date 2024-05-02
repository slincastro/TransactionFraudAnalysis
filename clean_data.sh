echo " Removiendo datos de ingesta"

rm -rf data_ingestion/documental/data.json
python3 data_ingestion/documental/clean.py
python3 data_ingestion/graph/clean.py