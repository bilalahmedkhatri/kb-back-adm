import os
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from pydantic.networks import EmailStr

from app.common.email import generate_test_email, send_email
from app.modules.auth.deps import CurrentUser, get_current_active_superuser
from app.modules.auth.models import Message

router = APIRouter(prefix="/utils", tags=["utils"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static", "uploads")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}


class UploadResponse(BaseModel):
    url: str
    filename: str


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")


@router.get("/health-check/")
async def health_check() -> bool:
    return True


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    current_user: CurrentUser,
    file: UploadFile = File(...),
) -> UploadResponse:
    """
    Upload an image or asset file. Returns local static URL.
    (Note: Can be integrated with Cloudflare R2 / Object Storage in production).
    """
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension '{ext}'. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    return UploadResponse(
        url=f"/static/uploads/{unique_filename}",
        filename=unique_filename,
    )
