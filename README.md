# Markdown Conversion API

This project exposes a small HTTP API that turns uploaded documents into Markdown. The intent of this README is to lock in the functional requirements and the high-level design so the implementation team can build the service consistently.

## Functional Requirements
- User uploads a supported document (e.g., DOCX, HTML, plain text) and receives a job identifier.
- User polls for the Markdown conversion status by job identifier.
- User retrieves the converted Markdown content once the job finishes successfully.

## High-Level Architecture
- The service provides a REST API under `/api/v1`.
- Uploaded files are stored in object storage (local disk in development) and queued for conversion.
- A background worker performs the actual conversion and persists results.
- Status and content queries read from the job store to report state and return Markdown output.

## API Surface

### 1. Upload Document
- **Endpoint**: `POST /api/v1/files/upload`
- **Purpose**: Accept a document upload and create a conversion job.
- **Request**: `multipart/form-data` with a single `file` field containing the document.
- **Response**:
  - `202 Accepted` with JSON body `{ "job_id": "<uuid>", "status": "queued" }` when the file is accepted for processing.
  - `400 Bad Request` for missing or unsupported files.
- **Notes**:
  - The server validates file size and type before enqueuing conversion.
  - The uploaded file is stored with a unique identifier tied to the job.

### 2. Check Conversion Status
- **Endpoint**: `GET /api/v1/files/status/{job_id}`
- **Purpose**: Report the current state of a conversion job.
- **Response**:
  - `200 OK` with JSON body `{ "job_id": "<uuid>", "status": "queued|processing|succeeded|failed", "detail": "<optional message>" }`.
  - `404 Not Found` if the job identifier does not exist.
- **Notes**:
  - `status` reflects the most recent state persisted by the worker.
  - When `status` is `failed`, `detail` conveys the failure reason.

### 3. Download Markdown Content
- **Endpoint**: `GET /api/v1/files/content/{job_id}`
- **Purpose**: Return the Markdown result for a completed job.
- **Response**:
  - `200 OK` with `text/markdown` body containing the converted document when the job succeeded.
  - `409 Conflict` if the job is not yet complete.
  - `404 Not Found` if the job identifier does not exist.
- **Notes**:
  - The API may include caching headers to reduce repeat downloads.
  - For failed jobs, clients must consult the status endpoint to learn the failure cause.

## Data Model Sketch
- **Job**
  - `id`: UUID generated at upload.
  - `original_filename`: Original user-supplied filename.
  - `storage_path`: Location of the uploaded binary.
  - `status`: Enum (`queued`, `processing`, `succeeded`, `failed`).
  - `error_detail`: Optional string populated on failure.
  - `markdown_path`: Path or blob reference to the generated Markdown.
  - `created_at` / `updated_at`: Timestamps for traceability.

## Processing Flow
1. Client posts a file to the upload endpoint.
2. API stores the file, records a new job in the job store, and enqueues a conversion task.
3. Worker converts the file to Markdown, updates the job status, and stores the output.
4. Client polls the status endpoint until `status` is `succeeded` or `failed`.
5. On success, client downloads the Markdown via the content endpoint.

This design document should be kept current as the implementation evolves.
