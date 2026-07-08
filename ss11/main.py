from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from model import ParkingSlot
from schemas import ParkingSlotCreate, StandardResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
Base.metadata.create_all(bind=engine)
app = FastAPI()
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_msg = exc.errors()[0]["msg"] if exc.errors() else "Dữ liệu không hợp lệ"
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "statusCode": 400,
            "message": f"Dữ liệu đầu vào không hợp lệ: {error_msg}",
            "error": "Bad Request",
            "data": None,
            "path": request.url.path,
            "timestamp": StandardResponse.__fields__["timestamp"].default_factory(),
        },
    )
@app.post(
    "/parking-slots",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_parking_slot(
    payload: ParkingSlotCreate, request: Request, db: Session = Depends(get_db)
):
    new_slot = ParkingSlot(
        slot_code=payload.slot_code,
        zone_name=payload.zone_name,
        max_weight=payload.max_weight,
    )

    try:
        db.add(new_slot)
        db.commit() 
        db.refresh(new_slot)
        return {
            "statusCode": 201,
            "message": "Thêm vị trí đỗ xe thành công",
            "error": None,
            "data": new_slot.to_dict(),
            "path": request.url.path,
        }
    except IntegrityError:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "statusCode": 400,
                "message": f"Mã vị trí đỗ xe '{payload.slot_code}' đã tồn tại trên hệ thống.",
                "error": "Conflict / Bad Request",
                "data": None,
                "path": request.url.path,
                "timestamp": StandardResponse.__fields__[
                    "timestamp"
                ].default_factory(),
            },
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "statusCode": 500,
                "message": "Hệ thống xảy ra sự cố đột xuất. Vui lòng thử lại sau.",
                "error": str(e),
                "data": None,
                "path": request.url.path,
                "timestamp": StandardResponse.__fields__[
                    "timestamp"
                ].default_factory(),
            },
        )
@app.get("/parking-slots", response_model=StandardResponse)
def get_all_parking_slots(request: Request, db: Session = Depends(get_db)):
    slots = db.query(ParkingSlot).all()
    data_list = [slot.to_dict() for slot in slots]

    return {
        "statusCode": 200,
        "message": "Lấy danh sách vị trí đỗ xe thành công",
        "error": None,
        "data": data_list,
        "path": request.url.path,
    }
@app.get("/parking-slots/{slot_id}", response_model=StandardResponse)
def get_parking_slot_detail(slot_id: int, request: Request, db: Session = Depends(get_db)):
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
    if not slot:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "statusCode": 404,
                "message": "Parking slot not found",
                "error": "Not Found",
                "data": None,
                "path": request.url.path,
                "timestamp": StandardResponse.__fields__["timestamp"].default_factory(),
            },
        )
    return {
        "statusCode": 200,
        "message": "Lấy thông tin chi tiết vị trí đỗ xe thành công",
        "error": None,
        "data": slot.to_dict(),
        "path": request.url.path,
    }