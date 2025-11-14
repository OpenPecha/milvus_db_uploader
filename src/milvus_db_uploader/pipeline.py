from pymilvus import MilvusClient
import os

from milvus_db_uploader.prepare_text import get_milvus_text_segments
from milvus_db_uploader.text import get_text_from_op_api
MILVUS_URI = os.getenv("MILVUS_URI")
MILVUS_TOKEN = os.getenv("MILVUS_TOKEN")
MILVUS_COLLECTION_NAME = os.getenv("MILVUS_COLLECTION_NAME", "test_kangyur_tengyur")

def upload_op_instance_to_milvus(instance_id, text_id, annotation_id) -> None:
    data = get_text_from_op_api(instance_id,text_id,annotation_id)
    
    try:
        client = MilvusClient(
            uri=MILVUS_URI,
            token=MILVUS_TOKEN,
            collection_name=MILVUS_COLLECTION_NAME
        )

        client.insert(MILVUS_COLLECTION_NAME,data)
        print(f"Uploaded {len(data)} text segments to Milvus")
    except Exception as e:
        print(f"Error uploading text segments to Milvus: {e}")
        raise e



