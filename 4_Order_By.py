from google.cloud import bigquery

client = bigquery.Client()
dataset_ref = client.dataset('nhtsa_traffic_fatalities', project='bigquery-public-data')
dataset = client.get_dataset(dataset_ref)

table_ref = dataset_ref.table('accedent_2015')
table = client.get_table(table_ref)
print(client.list_rows(table, max_results=5).to_dataframe())

query = """
        SELECT COUNT(consecutive_number) as num_accidents,
        EXTRACT(DAYOFWEEK FROM timestamp_of_crash) AS day_of_week
        FROM `bigquery-public-data.nhtsa_traffic_fatalities.accident_2015`
        GROUP BY day_of_week
        ORDER BY num_accidents DESC
        """

safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**9)
query_job =client.query(query, job_config=safe_config)

accidents_by_day = query_job.to_dataframe()
print(accidents_by_day)