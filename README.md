# Milvus DB Uploader

Embed text segments with Gemini and upload them to Milvus.

This library prepares text segments for vector search by:
- generating embeddings with Gemini (via `BoEmbedder`), and
- inserting records into a Milvus collection (via `pymilvus`).

Requires Python 3.8+.

## Installation

### From GitHub

```bash
pip install "git+https://github.com/OpenPecha/milvus_db_uploader.git"
```

### From source

```bash
git clone https://github.com/OpenPecha/milvus_db_uploader.git
cd milvus_db_uploader
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Runtime dependencies (if not pulled in automatically)
pip install pymilvus BoEmbedder
```

## Usage

Set your Gemini API key (used by the embedder):

```bash
export GOOGLE_GEMINI_KEY=your_api_key
```

Then upload an OpenPecha instance to Milvus:

```python
from milvus_db_uploader.pipeline import upload_op_instance_to_milvus

milvus_db_config = {
    "uri": "http://localhost:19530",
    "token": "root:Milvus",          # or an API token if using Zilliz Cloud
    "collection_name": "texts",
}

# NOTE: implement `get_text_from_op_api(instance_id)` in `milvus_db_uploader/text.py`
# to fetch the title and segments from the OP API.
upload_op_instance_to_milvus(instance_id="OP_INSTANCE_ID", milvus_db_config=milvus_db_config)
```

Alternatively, if you already have a title and list of segments (`[{id, content}, ...]`), you can prepare records and insert them yourself:

```python
from milvus_db_uploader.prepare_text import get_milvus_text_segments
from pymilvus import MilvusClient

title = "Example Title"
segments = [
    {"id": "1", "content": "First paragraph..."},
    {"id": "2", "content": "Second paragraph..."},
]

records = get_milvus_text_segments(title, segments)

client = MilvusClient(uri="http://localhost:19530", token="root:Milvus", collection_name="texts")
client.insert("texts", records)
```

## Contributing

Issues and pull requests are welcome. Feel free to open an issue to discuss changes or improvements.

## License

MIT License. See the [`LICENSE`](./LICENSE) file for details.
