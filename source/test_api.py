from fastapi.testclient import TestClient

from .api import app

client = TestClient(app)

endpoint = "/image/ads/analyze"
path_to_source = "test_source"


def test_load_few_files():
    files = [("files", open(build_path_to_image("random_img.jpg"), "rb")),
             ("files", open(build_path_to_image("random_img_2.jpg"), "rb"))]
    response = client.post(endpoint, files=files)
    assert response.status_code == 200


def test_load_one_file():
    files = [("files", open(build_path_to_image("random_img.jpg"), "rb"))]
    response = client.post(endpoint, files=files)
    assert response.status_code == 200


def test_load_zero_files():
    files = []
    response = client.post(endpoint, files=files)
    assert response.status_code == 400


def test_load_null_files():
    response = client.post(endpoint, files=None)
    assert response.status_code == 400


def test_find_ad_by_erid():
    file_name = "with_erid.png"
    files = [("files", open(build_path_to_image(file_name), "rb"))]
    response = client.post(endpoint, files=files)
    result = response.json()
    assert response.status_code == 200
    assert result[file_name] == 1


def test_find_ad_by_rus_name_ads():
    file_name = "with_rus_name_ads.png"
    files = [("files", open(build_path_to_image(file_name), "rb"))]
    response = client.post(endpoint, files=files)
    result = response.json()
    assert response.status_code == 200
    assert result[file_name] == 1


def test_find_ad_when_exist_erid_and_rus_name_ads():
    file_name = "with_erid_and_rus_name_ads.png"
    files = [("files", open(build_path_to_image(file_name), "rb"))]
    response = client.post(endpoint, files=files)
    assert response.status_code == 200


def test_not_find_ad():
    file_name = "without_ads.jpg"
    files = [("files", open(build_path_to_image(file_name), "rb"))]
    response = client.post(endpoint, files=files)
    result = response.json()
    assert response.status_code == 200
    assert result[file_name] == 0


def test_not_find_ad_when_image_without_text():
    file_name = "without_text.jpg"
    files = [("files", open(build_path_to_image(file_name), "rb"))]
    response = client.post(endpoint, files=files)
    result = response.json()
    assert response.status_code == 200
    assert result[file_name] == 0


def build_path_to_image(image_name: str) -> str:
    return f"{path_to_source}/{image_name}"
