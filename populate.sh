
echo " Generando ingesta de data - UHE - Slin Castro"
echo " ."
echo " .."
echo " Generando data Transaccional en Data.json"
python3 init_data/specific_users_generation.py
echo " ."
echo " .."
echo " Ingestando data desde el archivo json hacia MongoDB"
python3 data_ingestion/ingest.py 
python3 data_ingestion/verification.py 
echo " ."
echo " .."
echo " Ingestando data desde mongo db hacia Neo4j"
python3 graph/financial_etl.py
echo " ."
echo " .."
echo "Verificar los resultados en http://localhost:7474/browser/"
echo "Fin ..."
