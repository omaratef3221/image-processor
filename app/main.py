from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
import os
from . import database, processing
from fastapi import Query
from PIL import Image
import io
from . import schemas, database, processing
from typing import List, Optional
import base64

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    db = next(get_db())

    if db.query(database.ImageFrame).first():
        return

    csv_path = "/app/data/images.csv"
    if not os.path.isfile(csv_path):
        print("CSV file not found:", csv_path)
        return

    df = pd.read_csv(csv_path)
    pixel_cols = [f'col{i}' for i in range(1, 201)]

    for idx, row in df.iterrows():
        depth = row.depth
        pixels = np.array(row[1:201], dtype=np.uint8).reshape(1, 200)

        resized = processing.resize_image(pixels)
        colored = processing.apply_custom_colormap(resized)
        image_bytes = processing.image_to_bytes(colored)

        db.add(database.ImageFrame(depth=depth, image_data=image_bytes))

    db.commit()

@app.get("/frames/")
def get_sub_image(depth_min: float, depth_max: float,db: Session = Depends(get_db)):
    frames = db.query(database.ImageFrame).filter(
        database.ImageFrame.depth >= depth_min,
        database.ImageFrame.depth <= depth_max
    ).order_by(database.ImageFrame.depth).all()

    if not frames:
        raise HTTPException(status_code=404, detail="No frames found in this depth range")

    # Convert each frame's binary to a NumPy array
    arrays = []
    for frame in frames:
        image = Image.open(io.BytesIO(frame.image_data))
        arrays.append(np.array(image))

    # Stack vertically
    combined = np.vstack(arrays)

    # Convert to image and return as streaming response
    result_img = Image.fromarray(combined)
    buffer = io.BytesIO()
    result_img.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")