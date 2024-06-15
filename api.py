from fastapi import FastAPI, Request, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse
from ocr_model import OCRModel
from find_ad_service import FindAdService, ResearchedImage

app = FastAPI()

ru_model = OCRModel(lang='ru')
en_model = OCRModel(lang='en')


class AdsInImageAnalyzeResult(BaseModel):
    image_name: str
    status: int


class AdsResultAnalyze(BaseModel):
    result: list[AdsInImageAnalyzeResult]


@app.post("/image/ads/analyze")
def find_ads_in_images(files: list[UploadFile]):
    service = FindAdService(ru_model, en_model)
    researched_images = list(map(convert_to_researched_images, files))
    results = service.find_ad_in_list_image(researched_images)
    return results


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,
                                       exc: RequestValidationError):
    custom_error_message = list(map(create_custom_error_message, exc.errors()))
    error_response = create_error_response(custom_error_message, exc.body)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(error_response),
    )


def create_custom_error_message(error):
    return {"field": error['loc'][-1], "message": error['msg']}


def create_error_response(error_message, body):
    return {"validation_errors": error_message, "body": body}


def convert_to_researched_images(file: UploadFile):
    return ResearchedImage(filename=file.filename, content=file.file.read())
