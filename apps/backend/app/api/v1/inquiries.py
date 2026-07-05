from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.inquiry import InquiryCreate, Inquiry
from app.services.inquiry_service import InquiryService
from app.api.dependencies.auth import get_current_active_user, OfficerOnly

router = APIRouter(
    prefix="/inquiries",
    tags=["Inquiries"],
)

inquiry_service = InquiryService()


@router.post(
    "/",
    response_model=Inquiry,
    status_code=201,
)
def create_inquiry(
    request: InquiryCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user),
):
    return inquiry_service.create_inquiry(
        db=db,
        inquiry=request,
    )


@router.get(
    "/",
    response_model=list[Inquiry],
)
def get_inquiries(
    db: Session = Depends(get_db),
    officer=Depends(OfficerOnly),
):
    return inquiry_service.get_inquiries(
        db=db,
    )