from pymilvus import MilvusClient

from milvus_db_uploader.prepare_text import get_milvus_text_segments
from milvus_db_uploader.text import get_text_from_op_api


def upload_op_instance_to_milvus(instance_id, milvus_db_config) -> None:
    instance_title, instance_segments = get_text_from_op_api(instance_id)
    milvus_segments = get_milvus_text_segments(instance_title, instance_segments)
    
    try:
        client = MilvusClient(
            uri=milvus_db_config["uri"],
            token=milvus_db_config["token"],
            collection_name=milvus_db_config["collection_name"]
        )

        client.insert(milvus_db_config["collection_name"],milvus_segments)
        print(f"Uploaded {len(text_segments)} text segments to Milvus")
    except Exception as e:
        print(f"Error uploading text segments to Milvus: {e}")
        raise e




