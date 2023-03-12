from google.cloud import bigquery

client = bigquery.Client()
dataset_ref = client.dataset('openaq', project='bigquery-public-data')
dataset = client.get_dataset(dataset_ref)
tables = list(client.list_tables(dataset_ref))
for table in tables:
    print(table.table_id)

# Getting some (5) first rows of global air quality
table_ref = dataset_ref.table('global_air_quality')
table = client.get_table(table_ref)
client.list_rows(table, max_results=5).to_dataframe()

# Getting all the items from 'city' column where 'country' column is 'US'
query = """
        SELECT city
        FROM 'bigquery-public-data.openaq.qlobal_air_quality'
        WHERE country='US'
        """
# setting query job for bigquery
query_job = client.query(query)
# Running query and get DataFrame of result
us_city = query_job.to_dataframe()
# What 5 cities have the most measurements?
print(us_city.city.value_counts().head())