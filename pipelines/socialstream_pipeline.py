
import pandas as pd
import os
from azure.storage.filedatalake import DataLakeServiceClient
from etls.socialstream_etl import connect_reddit, extract_posts, transform_data
from utils.constants import CLIENT_ID, SECRET,USER_AGENT,ACCOUNT_URL,ACCOUNT_NAME,ACCOUNT_KEY,FILE_SYSTEM_NAME

def upload_to_azure(file_name: str, local_file_path: str):


    try:

        service_client = DataLakeServiceClient(
            account_url=ACCOUNT_URL,
            credential=ACCOUNT_KEY
        )
        file_system_client = service_client.get_file_system_client(FILE_SYSTEM_NAME)


        if os.path.exists(local_file_path):
            with open(local_file_path, 'rb') as file_data:
                data = file_data.read()
                file_client = file_system_client.get_file_client(file_name)


                file_client.create_file()
                file_client.append_data(data=data, offset=0, length=len(data))
                file_client.flush_data(len(data))  # Flush the correct length

            print(f"File '{file_name}' uploaded successfully to Azure under '{FILE_SYSTEM_NAME}' container.")
        else:
            print(f"Local file does not exist: {local_file_path}")

    except Exception as e:
        print(f"Error uploading file to Azure: {e}")


def socialstream_pipeline(file_name: str, subreddit: str, time_filter='all', limit=None):

    instance = connect_reddit(CLIENT_ID, SECRET, USER_AGENT)
    posts = extract_posts(instance, subreddit, time_filter, limit)
    post_df = pd.DataFrame(posts)
    post_df = transform_data(post_df)

    output_folder = './data'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  #

    local_file_path = os.path.join(output_folder, f'{file_name}.csv')


    try:
        post_df.to_csv(local_file_path, index=False)
        print(f"Data successfully loaded to CSV at {local_file_path}")


        upload_to_azure(f'{file_name}.csv', local_file_path)
    except Exception as e:
        print(f"An error occurred while loading data to CSV or uploading to Azure: {e}")

    return local_file_path

