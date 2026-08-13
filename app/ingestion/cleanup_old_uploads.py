import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "retrieval"))

from qdrant_client_setup import get_client, UPLOADS_COLLECTION
from qdrant_client.models import Filter, FieldCondition, Range

MAX_AGE_SECONDS = 24 * 60 * 60


def delete_old_uploads():
    client = get_client()
    cutoff_time = time.time() - MAX_AGE_SECONDS

    result = client.delete(
        collection_name=UPLOADS_COLLECTION,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="uploaded_at",
                    range=Range(lt=cutoff_time),
                )
            ]
        ),
    )
    print(f"Deleted points older than 24 hours. Status: {result.status}")


if __name__ == "__main__":
    delete_old_uploads()