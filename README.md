# DocuBrain

DocuBrain is an end-to-end AI system that transforms PDF documents into an interactive knowledge base: upload documents, chunk them, store in MongoDB, and (later) answer questions with context-aware responses. The backend is built with FastAPI and MongoDB.

---

## What’s Built So Far

- **API**: FastAPI app with versioned routes (`/api/v1/`).
- **Projects**: Create/get projects by `project_id`; projects own uploads and chunks.
- **Upload**: Validate and save files (PDF, TXT) under `src/assets/files/{project_id}/`.
- **Processing**: Chunk documents with LangChain (RecursiveCharacterTextSplitter), optional reset; store chunks in MongoDB with metadata and order.
- **Database**: MongoDB collections `projects` and `chunks` with indexes; Motor (async) client.
- **Config**: Settings via `.env` and Pydantic Settings; Docker Compose for MongoDB.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI (main.py)                        │
│  Startup: Motor client → db_client; Shutdown: close connection   │
└─────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│ routes/base   │           │ routes/data   │           │ (future)      │
│ /api/v1/      │           │ /api/v1/data/ │           │               │
│ welcome       │           │ upload,       │           │               │
│               │           │ process       │           │               │
└───────┬───────┘           └───────┬───────┘           └───────────────┘
        │                           │
        │ Depends(get_settings)     │ Request → app.db_client
        ▼                           ▼
┌───────────────┐           ┌───────────────────────────────────────┐
│ helper/config │           │ Controllers                            │
│ Setting,      │           │ DataController, ProjectController,     │
│ get_settings  │           │ ProcessController                      │
└───────────────┘           └───────────────────┬───────────────────┘
                                                │
                    ┌───────────────────────────┼───────────────────────────┐
                    ▼                           ▼                           ▼
            ┌───────────────┐           ┌───────────────┐           ┌───────────────┐
            │ ProjectModel  │           │ ChunkModel    │           │ File I/O      │
            │ (projects)    │           │ (chunks)      │           │ assets/files  │
            └───────┬───────┘           └───────┬───────┘           └───────────────┘
                    │                           │
                    ▼                           ▼
            ┌───────────────────────────────────────────────────────┐
            │ db_schemes (Pydantic): Project, DataChunk              │
            │ BaseDataModel → init_collection, indexes               │
            └───────────────────────────────────────────────────────┘
                    │
                    ▼
            ┌───────────────────────────────────────────────────────┐
            │ MongoDB (Motor AsyncIOMotorClient)                     │
            │ Collections: projects, chunks                         │
            └───────────────────────────────────────────────────────┘
```

- **Routes** handle HTTP, dependency-inject settings and `db_client`, call **controllers**.
- **Controllers** do validation, file paths, and processing (LangChain loaders + text splitter); they use **models** for DB access.
- **Models** (e.g. `ProjectModel`, `ChunkModel`) extend `BaseDataModel`, use **db_schemes** (Pydantic + indexes) and create collections/indexes on first use.
- **Config** is loaded from `src/.env` via Pydantic Settings.

---

## Project Structure

```
DocuBrain/
├── README.md
├── docker/
│   ├── docker-compose.yml   # MongoDB 7, port 27007, env for credentials
│   └── .env                 # MONGO_IDITDB_ROOT_USERNAME, MONGO_IDITDB_ROOT_PASSWORD
├── src/
│   ├── main.py              # FastAPI app, DB lifecycle, router includes
│   ├── .env                 # App config (see Configuration)
│   ├── requirements.txt
│   ├── helper/
│   │   └── config.py        # Setting (BaseSettings), get_settings()
│   ├── routes/
│   │   ├── base.py          # /api/v1/welcome
│   │   ├── data.py          # /api/v1/data/upload, /api/v1/data/process
│   │   └── schemes/
│   │       └── data.py      # ProcessRequest
│   ├── controllers/
│   │   ├── BaseController.py
│   │   ├── DataController.py
│   │   ├── ProjectController.py
│   │   └── ProcessController.py
│   ├── models/
│   │   ├── BaseDataModel.py
│   │   ├── ProjectModel.py
│   │   ├── ChunkModel.py
│   │   ├── db_schemes/
│   │   │   ├── project.py   # Project (Pydantic + get_indexes)
│   │   │   └── data_chunk.py
│   │   └── enums/
│   │       ├── DataBaseEnum.py   # collection names
│   │       ├── ResponseEnums.py  # ResponseStatus
│   │       └── ProcessEnums.py  # file extensions
│   └── assets/
│       └── files/           # Per-project uploads: {project_id}/{filename}
```

---

## Libraries & Tech Stack

| Package | Version | Purpose |
|--------|---------|--------|
| fastapi | 0.110.2 | Web framework, routing, dependency injection |
| uvicorn[standard] | 0.29.0 | ASGI server |
| python-multipart | 0.0.9 | File upload parsing |
| python-dotenv | 1.0.0 | Load `.env` (used with pydantic-settings) |
| pydantic-settings | 2.2.1 | `Setting` from env (config) |
| aiofiles | 23.2.1 | Async file write for uploads |
| motor | 3.4.0 | Async MongoDB driver |
| langchain | 0.1.20 | Document loaders, RecursiveCharacterTextSplitter |
| PyMuPDF | 1.24.3 | PDF loading (via LangChain) |

- **Database**: MongoDB 7 (Docker); app uses Motor and creates collections/indexes on demand.
- **Python**: 3.x compatible with the above (typically 3.10+).

---

## Configuration

### Application (`src/.env`)

Create `src/.env` with:

| Variable | Description |
|----------|-------------|
| `APP_NAME` | Application name (e.g. DocuBrain) |
| `APP_VERSION` | Version string (e.g. 1.0.0) |
| `FILE_ALLOWED_TYPE` | Allowed content types list (e.g. `["application/pdf","text/plain"]`) |
| `FILE_MAX_SIZE` | Max upload size in bytes |
| `FILE_DEFAULT_CHUNK_SIZE` | Chunk size in bytes for streaming upload write |
| `MONGO_URI` | MongoDB URI (e.g. `mongodb://localhost:27007` for Docker) |
| `MONGO_DATABASE` | Database name |

### Docker (`docker/.env`)

For MongoDB via Docker Compose, create `docker/.env` with:

| Variable | Description |
|----------|-------------|
| `MONGO_IDITDB_ROOT_USERNAME` | MongoDB root username |
| `MONGO_IDITDB_ROOT_PASSWORD` | MongoDB root password |

MongoDB is exposed on **port 27007**. Use the same host/port (and credentials if required) in `MONGO_URI` in `src/.env`.

---

## Prerequisites

- Python 3.10+
- Docker & Docker Compose (for MongoDB)
- (Optional) Virtual environment recommended

---

## Getting Started

1. **Clone and enter project**
   ```bash
   cd DocuBrain
   ```

2. **Start MongoDB**
   ```bash
   cd docker && docker compose up -d && cd ..
   ```

3. **Create `src/.env`**  
   Copy the variables from the Configuration table above and set values. For a quick local test with Docker MongoDB:
   - `MONGO_URI=mongodb://localhost:27007`
   - `MONGO_DATABASE=docubrain`
   - Set `APP_NAME`, `APP_VERSION`, `FILE_ALLOWED_TYPE`, `FILE_MAX_SIZE`, `FILE_DEFAULT_CHUNK_SIZE` as needed.

4. **Install dependencies and run**
   ```bash
   cd src
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

5. **Check**
   - Welcome: `GET http://localhost:8000/api/v1/welcome`
   - Upload: `POST http://localhost:8000/api/v1/data/upload/{project_id}` with form file
   - Process: `POST http://localhost:8000/api/v1/data/process/{project_id}` with JSON body `{"file_id": "...", "chunk_size": 100, "overlap_size": 20, "do_reset": 0}`

---

## API Endpoints (Current)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/welcome` | Returns welcome message using `APP_NAME` and `APP_VERSION` |
| POST | `/api/v1/data/upload/{project_id}` | Validate and upload file; returns `file_id` and status |
| POST | `/api/v1/data/process/{project_id}` | Chunk file by `file_id`, optionally reset project chunks; store in DB |

Process body: `file_id` (required), `chunk_size`, `overlap_size`, `do_reset` (see `ProcessRequest` in `routes/schemes/data.py`).

---

This README reflects the current state of the project: architecture, configuration, libraries, and how to run and use it.
