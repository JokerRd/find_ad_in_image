from ocr_model import OCRModel
from dataclasses import dataclass
from ad_finder import find_ad, AdDefinitionStatus


@dataclass
class ResearchedImage:
    filename: str
    content: bytes


@dataclass
class FindResult:
    filename: str
    status: int


def _find_ad_in_image(image: ResearchedImage,
                      model: OCRModel) -> AdDefinitionStatus:
    image_content = image.content
    texts = model.image_to_text(image_content)
    return find_ad(texts)


class FindAdService:

    def __init__(self, ru_ocr_model: OCRModel, en_ocr_model: OCRModel):
        self.ru_ocr_model = ru_ocr_model
        self.en_ocr_model = en_ocr_model

    def find_ad_in_list_image(self,
                              images: [ResearchedImage]) -> dict[str, int]:
        result: dict[str, int] = {}
        for image in images:
            status_from_en_model = _find_ad_in_image(image,
                                                     self.en_ocr_model)
            if status_from_en_model != AdDefinitionStatus.ad:
                status_from_ru_model = _find_ad_in_image(image,
                                                         self.ru_ocr_model)
                if status_from_ru_model == AdDefinitionStatus.ad:
                    result[image.filename] = status_from_ru_model.value
                elif (status_from_en_model == AdDefinitionStatus.may_be_ad
                      or status_from_ru_model == AdDefinitionStatus.may_be_ad):
                    result[image.filename] = AdDefinitionStatus.may_be_ad.value
                else:
                    result[image.filename] = AdDefinitionStatus.no_ad.value
            else:
                result[image.filename] = status_from_en_model.value

        return result
