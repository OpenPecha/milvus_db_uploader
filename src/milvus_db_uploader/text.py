import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

base_url = "https://api-l25bgmwqoa-uc.a.run.app"

def get_metadata_from_op_api(text_id):
    logger.info(f"Fetching metadata for text_id: {text_id}")
    endpoint = f"/v2/texts/{text_id}"
    url = f"{base_url}{endpoint}"
    logger.info(f"Making GET request to: {url}")
    
    response = requests.get(url)
    response.raise_for_status()
    logger.info(f"Successfully received response with status code: {response.status_code}")
    
    data = response.json()
    logger.info(f"Parsed JSON response for text_id: {text_id}")
    
    # Extract language
    language = data.get("language", "en")
    logger.info(f"Extracted language: {language}")
    
    # Extract title based on language
    title_dict = data.get("title", {})
    title = title_dict.get(language, title_dict.get("en", ""))
    logger.info(f"Extracted title: {title}")
    
    result = {
        "title": title,
        "language": language,
    }
    logger.info(f"Returning metadata for text_id: {text_id}")
    return result

def get_annotations_from_op_api(annotation_id):
    logger.info(f"Fetching annotations for annotation_id: {annotation_id}")
    endpoint = f"/v2/annotations/{annotation_id}"
    url = f"{base_url}{endpoint}"
    logger.info(f"Making GET request to: {url}")
    
    response = requests.get(url)
    response.raise_for_status()
    logger.info(f"Successfully received response with status code: {response.status_code}")
    
    data = response.json()
    logger.info(f"Parsed JSON response for annotation_id: {annotation_id}")
    
    data = data.get("data", {})
    logger.info(f"Extracted data array, found {len(data)} annotation entries")
    
    annotations_ids = [i.get("id", "") for i in data]
    logger.info(f"Extracted {len(annotations_ids)} annotation IDs: {annotations_ids}")
    
    return annotations_ids

def get_annotations_content_from_op_api(instance_id, annotations_ids):
    """
    Fetch segment content for annotations from the OP API.
    
    Args:
        instance_id: The instance identifier (required, cannot be empty)
        annotations_ids: List of annotation/segment IDs
    
    Returns:
        dict or list: Segment content data
    """
    logger.info(f"Fetching segment content for instance_id: {instance_id}")
    logger.info(f"Number of annotation IDs to fetch: {len(annotations_ids)}")
    
    if not instance_id:
        logger.error("instance_id cannot be empty")
        raise ValueError("instance_id cannot be empty")
    
    endpoint = f"/v2/instances/{instance_id}/segment-content"
    
    # Build query string with comma-separated segment_ids (without URL encoding)
    segment_ids_str = ",".join(annotations_ids)
    url = f"{base_url}{endpoint}?segment_id={segment_ids_str}"
    logger.info(f"Making GET request to: {url}")
    
    response = requests.get(url)
    response.raise_for_status()
    logger.info(f"Successfully received response with status code: {response.status_code}")
    
    data = response.json()
    logger.info(f"Parsed JSON response, received {len(data)} segment content entries")
    
    return data


def get_text_from_op_api(instance_id, text_id, annotation_id):
    """
    Fetch metadata for a text from the OP API.
    
    Args:
        instance_id: Instance identifier (if needed for other operations)
        text_id: The text ID (e.g., "T12345678")
        annotation_id: The annotation ID
    
    Returns:
        list: List of dictionaries containing segment data with title and language
    """
    logger.info(f"Starting get_text_from_op_api with instance_id: {instance_id}, text_id: {text_id}, annotation_id: {annotation_id}")
    data = []

    logger.info("Step 1: Fetching metadata")
    metadata = get_metadata_from_op_api(text_id)
    logger.info(f"Metadata retrieved: title={metadata['title']}, language={metadata['language']}")
    
    logger.info("Step 2: Fetching annotations")
    annotations = get_annotations_from_op_api(annotation_id)
    logger.info(f"Retrieved {len(annotations)} annotation IDs")
    
    #remove the last element for testing 
    logger.info("Step 3: Fetching annotations content")
    annotations_content = get_annotations_content_from_op_api(instance_id, annotations)
    logger.info(f"Retrieved {len(annotations_content)} annotation content entries")
    
    logger.info("Step 4: Processing annotation content and building result data")
    for idx, annotation in enumerate(annotations_content):
        content = annotation["content"]
        segment_id = annotation["segment_id"]
        logger.info(f"Processing annotation {idx + 1}/{len(annotations_content)}: segment_id={segment_id}")
        data.append({
            "segment_id": segment_id,
            "content": content,
            "title": metadata["title"],
            "language": metadata["language"],
        })
    
    logger.info(f"Completed processing. Returning {len(data)} segments")
    return data


#print(get_text_from_op_api(text_id="Tl23YzDgsVYp1OjyjZp8i",instance_id="EAIsZOeAQ8sSPqA3P1gqM",annotation_id="QIQMdDBnfncEsc8YTeCXi"))