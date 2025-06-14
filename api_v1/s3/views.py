from fastapi import APIRouter, File, UploadFile
from .s3_config import s3_client


router = APIRouter(tags=["s3_media"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    object_name = file.filename
    file_content = await file.read()
    async with s3_client.get_client() as client:
        await client.put_object(
            Bucket=s3_client.bucket_name,
            Key=object_name,
            Body=file_content
        )
    return {"message": f"Файл '{object_name}' успешно загружен в бакет 'test'"}