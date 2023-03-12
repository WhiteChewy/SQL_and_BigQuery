from google.cloud import bigquery

# Create client
client = bigquery.Client()
# Getting reference to dataset
dataset_ref = client.dataset('hacker_news', project='bigquery-public-data')
# API request to fetch the dataset
dataset = client.get_dataset(dataset_ref)
# Getting list of tables
tables = list(client.list_tables(dataset))
for table in tables:
    print(table.table_id)
table_ref = dataset_ref.table('full')
table = client.get_table(table_ref)

# Getting information on all the columns int the 'full' table in hacker_news dataset
full_table_schema = table.schema
client.list_rows(table=table, max_results=5).to_arrow()

# Getting 1st 5entries of 'by' column in 'full' table
first_five_bys = client.list_rows(table=table, selected_fields=full_table_schema[:1], max_results=5).to_dataframe()
