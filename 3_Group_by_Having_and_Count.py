from google.cloud import bigquery

client = bigquery.Client()
dataset_ref = client.dataset('hacker_news', project='bigquery-public-data')
dataset = client.get_dataset(dataset_ref)
table_ref = dataset_ref.table('comments')
table = client.get_table(table_ref)
client.list_rows(table, max_results=5).to_dataframe()

query_popular = """
                SELECT parent, COUNT(id)
                FROM `bigquery-public-data.hacker_news.comments`
                GROUP BY parent
                HAVING COUNT(id) > 10
                """

safe_config = bigquery.QueryJobConfig(maximun_bytes_billed=10**10)
query_job =client.query(query_popular, job_config=safe_config)
popular_comments = query_job.to_dataframe()
print(popular_comments.head())

query_improved = """
                 SELECT parent, COUNT(1)
                 FROM `bigquery-public-data.hacker_news.comments`
                 GROUP BY parent
                 HAVING COUNT(1) > 10
                 """
imp_query_job = client.query(query_improved, job_config=safe_config)
popular_comments_imp = imp_query_job.to_dataframe()
print(popular_comments_imp.head())