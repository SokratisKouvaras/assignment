from fastparquet import ParquetFile
import requests
import pyarrow as pa
import pyarrow.parquet as pq
import logging
logger = logging.getLogger(__name__)
URL = 'https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_2024-01.parquet'
with open("my_file.txt", "wb") as binary_file:
    # Write bytes to file
    logger.warning('trying to save file')
    binary_file.write(requests.get(URL).content)
    logger.warning('file saved')
import pyarrow.csv
logger.warning('trying to create csv file')
pa.csv.write_csv(pq.read_table('./my_file.txt'), "table.csv",
                 write_options=pa.csv.WriteOptions(include_header=True))
logger.warning('csv created')

#pf = ParquetFile('https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_2024-01.parquet')

#import pyarrow.csv
#pa.csv.write_csv(pq.read_table(r.text), "table.csv",
#                 write_options=pa.csv.WriteOptions(include_header=True))