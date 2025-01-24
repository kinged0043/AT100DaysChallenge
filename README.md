# AT100DaysChallenge

A Django-based starter code that processes PDF books, generates embeddings using Cohere, and stores them in Pinecone for intelligent text retrieval RAG) and chat interactions.

## 🚀 Features

- PDF book processing and text extraction
- Text chunking with overlap for better context preservation
- Embedding generation using Cohere's embed-english-v3.0 model
- Vector storage and retrieval using Pinecone
- Django management commands for batch processing
- Efficient database storage of book chunks

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- Microsoft Visual C++ Build Tools (required for lz4 package installation)
- Git

### Installing Microsoft Visual C++ Build Tools

If you encounter the following error during installation:
```
ERROR: Failed building wheel for lz4
Failed to build lz4
ERROR: Failed to build installable wheels for some pyproject.toml based projects (lz4)
```

Follow these steps:
1. Download the [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Run the installer
3. Select "Desktop development with C++"
4. Install the selected components

## 🛠 Installation

1. Clone the repository:
```bash
git clone https://github.com/DonGuillotine/AT100DaysChallenge
cd AT100DaysChallenge
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix or MacOS
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install django cohere pinecone-client[grpc] PyPDF2
```

4. Set up your environment variables:
Create a `.env` file in the project root with the following:
```env
COHERE_API_KEY=your_cohere_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
```

5. Run database migrations:
```bash
python manage.py migrate
```

## 📚 Loading Books (We will later decide on which books to add)

1. Place your PDF books in the `chatbot/books` directory

2. Run the preprocessing command:
```bash
python manage.py preprocess_books
```

This command will:
- Scan the books directory for PDF files
- Process each book into chunks
- Generate embeddings using Cohere
- Store vectors in Pinecone
- Save book chunks in the database

## 🏗 Project Structure

- `chatbot/management/commands/preprocess_books.py`: Django command for batch processing books
- `chatbot/models.py`: Database models for Books and BookChunks
- `chatbot/utils.py`: Utility functions for processing, embedding, and vector operations
- `chatbot/views.py`: Web views for the chatbot interface

## 📝 Code Examples

### Processing a Single Book
```python
from chatbot.models import Book
from chatbot.utils import preprocess_and_embed_book

book = Book.objects.create(
    title="Sample Book",
    author="Author Name",
    file_name="sample.pdf"
)
preprocess_and_embed_book(book)
```

## ⚙️ Configuration

### Chunking Parameters
You can adjust the following parameters in `utils.py`:
- `chunk_size`: Number of characters per chunk (default: 500)
- `overlap`: Number of overlapping characters between chunks (default: 100)
- `batch_size`: Number of vectors to upsert at once (default: 100)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the [MIT License](LICENSE)

## 🆘 Troubleshooting

### Common Issues

1. **lz4 Installation Error**
   - Solution: Install Microsoft Visual C++ Build Tools as described in the Prerequisites section

2. **Pinecone Connection Issues**
   - Verify your API key and environment settings
   - Ensure you're using the correct Pinecone environment region

3. **PDF Processing Errors**
   - Make sure PDFs are not password-protected
   - Verify PDF file permissions

For additional help, please open an issue in the repository.
