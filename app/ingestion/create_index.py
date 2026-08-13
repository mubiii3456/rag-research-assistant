import sys 
import os
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "retrieval"))
 
from qdrant_client_setup import get_client, UPLOADS_COLLECTION
from qdrant_client.models import PayloadSchemaType
 
if __name__ == "__main__":
    client = get_client()
    client.create_payload_index(
        collection_name=UPLOADS_COLLECTION,
        field_name="session_id",
        field_schema=PayloadSchemaType.KEYWORD,
    )
    print(f"Index created on 'session_id' for collection '{UPLOADS_COLLECTION}'.")

    client.create_payload_index(
        collection_name=UPLOADS_COLLECTION,
        field_name="uploaded_at",
        field_schema=PayloadSchemaType.FLOAT,
    )
    print(f"Index created on 'uploaded_at' for collection '{UPLOADS_COLLECTION}'.")