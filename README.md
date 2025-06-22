# Image Processing API

This project provides a FastAPI-based web service for processing and visualizing image data from a CSV file. It loads image frames from a CSV, processes them (resizing and applying a custom colormap), stores them in a SQLite database, and serves combined image slices via a REST API.

## Features
- Loads image frames from a CSV file on startup
- Resizes and colorizes each frame using a custom blue-to-red colormap
- Stores processed images in a SQLite database
- Provides an API to retrieve a vertical stack of frames within a specified depth range as a PNG image
- Containerized with Docker for easy deployment

## Data Format
- The input CSV file (e.g., `data/images.csv`) should have the following structure:
  - The first column: `depth` (float)
  - The next 200 columns: pixel values for a single row of the image (named `col1`, `col2`, ..., `col200`)
- Each row represents a 1x200 grayscale image at a specific depth.

## API Usage

### Get Combined Image Frames
- **Endpoint:** `GET /frames/`
- **Query Parameters:**
  - `depth_min` (float): Minimum depth (inclusive)
  - `depth_max` (float): Maximum depth (inclusive)
- **Response:**
  - Returns a PNG image that is a vertical stack of all frames within the specified depth range.
  - If no frames are found, returns a 404 error.

**Example request:**
```
GET /frames/?depth_min=100.0&depth_max=200.0
```

## Running with Docker

### Build the Docker image
```sh
docker build -t image-processing .
```

### Run the container
Replace the path to `images.csv` as needed:
```sh
docker run -p 8000:8000 \
  -v /Users/omaratef/Dropbox/TEMP/AIQ_Assignment/Assignment2/image-processing/data/images.csv:/app/data/images.csv \
  image-processing
```
- The API will be available at [http://localhost:8000](http://localhost:8000)
- The container expects the CSV file to be mounted at `/app/data/images.csv`

## Local Development

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the API:
   ```sh
   uvicorn app.main:app --reload
   ```

## Dependencies
- fastapi
- uvicorn
- pandas
- numpy
- opencv-python
- Pillow
- python-multipart
- sqlalchemy

See `requirements.txt` for exact versions.

## Project Structure
```
image-processing/
├── app/
│   ├── main.py         # FastAPI app and endpoints
│   ├── processing.py   # Image processing functions
│   ├── database.py     # Database models and setup
│   └── schemas.py      # Pydantic schemas
├── data/
│   └── images.csv      # Input data (not included in repo)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker setup
└── README.md           # Project documentation
```

## Notes
- The database (`image_data.db`) is created in the container or local directory on first run.
- The API only supports reading frames; uploading or modifying data is not implemented.
- For large CSV files, initial startup may take some time as images are processed and loaded into the database.
