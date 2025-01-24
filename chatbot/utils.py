import cohere
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import PyPDF2
import json
import re
from io import BytesIO
from django.conf import settings
from .models import Book, BookChunk

def get_pinecone_client():
    return Pinecone(api_key=settings.PINECONE_API_KEY)

def get_cohere_client():
    return cohere.Client(settings.COHERE_API_KEY)

def initialize_pinecone_index(index_name, dimension):
    pc = get_pinecone_client()
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws',
                region=settings.PINECONE_ENVIRONMENT
            )
        )
    return pc.Index(index_name)

def preprocess_and_embed_book(book):
    co = get_cohere_client()
    pc = get_pinecone_client()
    index_name = "books-index"
    dimension = 1024
    batch_size = 100  # Adjust this value as needed

    # Initialize Pinecone index if it doesn't exist
    index = initialize_pinecone_index(index_name, dimension)

    # Preprocess the PDF content
    chunks = preprocess_pdf(book.file_path)
    
    # Generate embeddings using the new model and input_type
    embeddings = co.embed(
        texts=chunks, 
        model='embed-english-v3.0',
        input_type="search_document"
    ).embeddings
    
    # Prepare vectors for upserting
    vectors = [
        {
            "id": f"{book.id}-{i}",
            "values": embedding,
            "metadata": {"chunk_id": i, "book_id": book.id}
        }
        for i, embedding in enumerate(embeddings)
    ]
    try:
        # Upsert vectors to Pinecone in batches
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            index.upsert(vectors=batch)
    except Exception as e:
        print(f"Error upserting vectors for book {book.id}: {str(e)}")
        raise
    
    # Store chunks in the database
    for i, chunk in enumerate(chunks):
        book.chunks.create(chunk_id=i, content=chunk)
    
    # Update the book's embedding_id
    book.embedding_id = f"{book.id}"
    book.save()

def preprocess_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    # Clean the text
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    
    # Split into smaller chunks
    chunk_size = 500  # Reduced from 1000
    overlap = 100  # Reduced from 200
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    
    return chunks


def get_relevant_text_chunks(book_id, chunk_ids):
    book_chunks = BookChunk.objects.filter(book_id=book_id, chunk_id__in=chunk_ids)
    return [chunk.content for chunk in book_chunks]
