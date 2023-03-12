from google.cloud import bigquery

client = bigquery.Client()
dataset_ref = client.dataset('crypto_bitcoin', project='bigquery-public-data')
dataset = client.get_dataset(dataset_ref)
table_ref = dataset_ref.table('transactions')
table = client.get_table(table_ref)
print(client.list_rows(table, max_results=5).to_dataframe())

query_with_CTE = """
                 WITH time AS
                 (
                    SELECT DATE(block_timestamp) AS trans_date
                    FROM `bigquery-public-data.crypto_bitcoin.transactions`
                 )
                 SELECT COUNT(1) AS transactions, trans_date
                 FROM time
                 GROUP BY trans_date
                 ORDER BY trans_date
                 """

safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
query_job = client.query(query_with_CTE, job_config=safe_config)
transactions_by_date = query_job.to_dataframe()
print(transactions_by_date.head())
