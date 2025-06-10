from fastapi import APIRouter
from .clients.views import router as client_router
from .demo_auth.demo_jwt_auth import router as jwt_auth_router
from .s3.s3_config import s3_client
from .s3.views import router as upload_image_router

router = APIRouter()


router.include_router(router=client_router,prefix="/Clients")
router.include_router(router=jwt_auth_router)
router.include_router(router=upload_image_router,prefix="/S3")