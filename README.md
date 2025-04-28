# Symptom Recommendation API (Agnos Candidate Assignment)

✅ FastAPI-based API for recommending additional symptoms based on patient profile and selected symptoms.

## Installation

```bash
git clone <your_repo_url>
cd <your_repo_folder>
pip install -r requirements.txt
```

or with Docker:

```bash
docker build -t agnos-symptom-recommender .
docker run -p 8000:8000 agnos-symptom-recommender
```

## Running the API

```bash
uvicorn app:app --reload
```

Access Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Example API Call

```json
POST /recommend
{
  "gender": "male",
  "age": 29,
  "symptoms": ["ไอ", "น้ำมูกไหล"]
}
```

## Testing

```bash
python test_app.py
```

✅ Should print `Test passed!`

## Author
Peeranut Aimcharoen