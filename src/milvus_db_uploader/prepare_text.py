import os

from pathlib import Path
from BoEmbedder.gemini import embed_texts_batch
from milvus_db_uploader.text import get_text_from_op_api

def get_milvus_text_segments(text_title, text_segments):
    milvus_text_segments = []

    text_segments_embeddings = embed_texts_batch(text_segments, api_key=os.getenv("GOOGLE_GEMINI_KEY"))
    
    for text_segment, text_segment_embedding in zip(text_segments, text_segments_embeddings):
        segment_id = text_segment.get("id", "")
        segment_str = text_segment.get("content", "")

        milvus_text_segments.append({
            "id": segment_id,
            "text": segment_str,
            "title": text_title,
            "dense_vector": text_segment_embedding,
        })
    return milvus_text_segments



