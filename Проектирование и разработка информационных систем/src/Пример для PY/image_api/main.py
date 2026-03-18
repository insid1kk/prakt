from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from PIL import Image
import datetime
import os

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./images.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ImageModel(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    file_path = Column(String)
    size_bytes = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    file_type = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/image/add")
async def add_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        raise HTTPException(status_code=400, detail="Можно загружать только изображения")
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    content = await file.read()
    
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    with Image.open(file_path) as img:
        width, height = img.size
    
    file_size = os.path.getsize(file_path)
    file_type = file.filename.split('.')[-1].lower()
    
    db_image = ImageModel(
        name=file.filename,
        file_path=file_path,
        size_bytes=file_size,
        width=width,
        height=height,
        file_type=file_type
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    
    return {
        "success": True,
        "message": "Изображение успешно добавлено",
        "image": {
            "id": db_image.id,
            "name": db_image.name,
            "size_bytes": db_image.size_bytes,
            "width": db_image.width,
            "height": db_image.height,
            "type": db_image.file_type,
            "created_at": db_image.created_at,
            "path": db_image.file_path
        }
    }

@app.put("/api/image/change/size")
async def change_size(
    image_path: str = Form(...),
    new_width: int = Form(...),
    new_height: int = Form(...),
    db: Session = Depends(get_db)
):
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    base, ext = os.path.splitext(image_path)
    new_path = f"{base}_{new_width}x{new_height}{ext}"
    
    with Image.open(image_path) as img:
        resized = img.resize((new_width, new_height))
        resized.save(new_path)
    
    with Image.open(new_path) as img:
        width, height = img.size
    
    db_image = ImageModel(
        name=os.path.basename(new_path),
        file_path=new_path,
        size_bytes=os.path.getsize(new_path),
        width=width,
        height=height,
        file_type=ext[1:].lower()
    )
    db.add(db_image)
    db.commit()
    
    return {
        "success": True,
        "message": "Размер изображения изменен",
        "new_file": new_path,
        "new_size": f"{new_width}x{new_height}"
    }

@app.put("/api/image/change/rotate")
async def rotate_image(
    image_path: str = Form(...),
    degrees: int = Form(90),
    db: Session = Depends(get_db)
):
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    base, ext = os.path.splitext(image_path)
    new_path = f"{base}_rotated_{degrees}{ext}"
    
    with Image.open(image_path) as img:
        rotated = img.rotate(degrees, expand=True)
        rotated.save(new_path)
    
    with Image.open(new_path) as img:
        width, height = img.size
    
    db_image = ImageModel(
        name=os.path.basename(new_path),
        file_path=new_path,
        size_bytes=os.path.getsize(new_path),
        width=width,
        height=height,
        file_type=ext[1:].lower()
    )
    db.add(db_image)
    db.commit()
    
    return {
        "success": True,
        "message": f"Изображение повернуто на {degrees} градусов",
        "new_file": new_path
    }

@app.get("/api/image")
async def get_all_images(db: Session = Depends(get_db)):
    images = db.query(ImageModel).all()
    
    result = []
    for img in images:
        result.append({
            "id": img.id,
            "name": img.name,
            "size_bytes": img.size_bytes,
            "width": img.width,
            "height": img.height,
            "type": img.file_type,
            "created_at": img.created_at,
            "file_path": img.file_path
        })
    
    return {
        "total": len(result),
        "images": result
    }

@app.get("/")
async def root():
    return {
        "message": "Image Processing API - Вариант 1",
        "methods": [
            "POST /api/image/add - Добавить изображение",
            "PUT /api/image/change/size - Изменить размер",
            "PUT /api/image/change/rotate - Повернуть изображение",
            "GET /api/image - Получить все изображения"
        ],
        "docs": "/docs"
    }