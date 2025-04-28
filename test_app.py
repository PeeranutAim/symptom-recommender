import requests

def test_recommend_api():
    url = "http://localhost:8000/recommend"
    payload = {
        "gender": "male",
        "age": 29,
        "symptoms": ["ไอ", "น้ำมูกไหล"]
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert "recommendations" in response.json()

if __name__ == "__main__":
    test_recommend_api()
    print("✅ Test passed!")