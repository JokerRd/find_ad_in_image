import enum
import editdistance
import re


class AdDefinitionStatus(enum.Enum):
    ad = 1
    no_ad = 0
    may_be_ad = 2


ad_keywords = ['erid', 'реклама']


def find_ad(text_from_image: [str]) -> AdDefinitionStatus:
    ads_statuses = list(map(handle_text_ad, text_from_image))
    ad_statuses = map(lambda status: status == AdDefinitionStatus.ad,
                      ads_statuses)
    may_be_ad_statuses = map(
        lambda status: status == AdDefinitionStatus.may_be_ad, ads_statuses)
    is_ad_status = any(ad_statuses)
    if is_ad_status:
        return AdDefinitionStatus.ad
    is_may_be_ad_status = any(may_be_ad_statuses)
    if is_may_be_ad_status:
        return AdDefinitionStatus.may_be_ad
    return AdDefinitionStatus.no_ad


def handle_text_ad(text: str):
    print(text)
    cleaned_text = cleanup_text(text)
    print(cleaned_text)
    if is_ad_keyword_substring(cleaned_text):
        return AdDefinitionStatus.ad
    distance_iter = map(
        lambda keyword: calc_distance_ad(cleaned_text, keyword), ad_keywords)
    min_distance = min(distance_iter)
    if min_distance == 0:
        return AdDefinitionStatus.ad
    if min_distance == 1:
        return AdDefinitionStatus.may_be_ad
    return AdDefinitionStatus.no_ad


def is_ad_keyword_substring(cleaned_text: str) -> bool:
    return any(map(lambda keyword: keyword in cleaned_text, ad_keywords))


def cleanup_text(text: str) -> str:
    return re.sub(r'[\W0-9]', '', text).lower()


def calc_distance_ad(text: str, keyword: str) -> float:
    return editdistance.eval(text, keyword)
