import os.path

import pandas as pd
from qdrant_client import QdrantClient, models
from tqdm import tqdm

from qdrant.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, EMBEDDINGS_MODEL
from sentence_transformers import SentenceTransformer

csv_file_path = os.path.join(DATA_DIR, "articles_compiled.csv")


def get_data():
    df = pd.read_csv(csv_file_path)
    documents = df['teaser'].tolist()
    df.drop(columns=['p_date'], inplace=True)
    metadata = df.to_dict('records')
    return documents, metadata


def upload_vectors(client: QdrantClient, encoder: SentenceTransformer, metadata):
    client.upload_records(
        collection_name=COLLECTION_NAME,
        records=[
            models.Record(
                id=idx, vector=encoder.encode(doc['teaser']).tolist(), payload=doc
            )
            for idx, doc in enumerate(tqdm(metadata))
        ],
    )


def add_docs(client: QdrantClient, documents, metadata):
    client.add(
        collection_name=COLLECTION_NAME,
        documents=documents,
        metadata=metadata,
        ids=tqdm(range(len(documents))),
        # usage of parallel leads to fork safety issue in OSX, therefore None
        parallel=None,
    )


def create_document_fastembed(client: QdrantClient):
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=client.get_fastembed_vector_params(on_disk=True),
        # Quantization for reducing the memory usage, 8-bit
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True
            )
        )
    )


def create_document_multi_lang(client: QdrantClient, encoder: SentenceTransformer):
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=encoder.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE,
            on_disk=True
        ),
        # Quantization for reducing the memory usage, 8-bit
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True
            )
        )
    )


def init_custom_embed(client: QdrantClient, metadata):
    encoder = SentenceTransformer(EMBEDDINGS_MODEL)
    create_document_multi_lang(client, encoder)
    upload_vectors(client, encoder, metadata)


def init_fastembed(client: QdrantClient, documents, metadata):
    client.set_model(EMBEDDINGS_MODEL)
    create_document_fastembed(client)
    add_docs(client, documents, metadata)


def populate_qdrant():
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

    documents, metadata = get_data()
    init_custom_embed(client, metadata)
    # init_fastembed(client, documents, metadata)


if __name__ == '__main__':
    populate_qdrant()
