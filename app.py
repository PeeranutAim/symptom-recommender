from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------- Load and Prepare Data ---------------------

file_path = "ai_symptom_picker.csv"
df = pd.read_csv(file_path)

def parse_search_term(term):
    if pd.isna(term):
        return []
    return [x.strip() for x in str(term).split(",") if x.strip()]

df['symptoms_list'] = df['search_term'].apply(parse_search_term)
df['gender_encoded'] = df['gender'].map({'male': 0, 'female': 1})
df['age_bin'] = (df['age'] // 10) * 10
df['combined_features'] = df.apply(
    lambda x: f"{x['gender_encoded']} {x['age_bin']} " + " ".join(x['symptoms_list']), axis=1
)

vectorizer = CountVectorizer()
feature_matrix = vectorizer.fit_transform(df['combined_features'])

def recommend_symptoms_v2(input_gender, input_age, input_symptoms, top_k=5):
    age_bin = (input_age // 10) * 10
    input_text = f"{0 if input_gender=='male' else 1} {age_bin} " + " ".join(input_symptoms)
    input_vector = vectorizer.transform([input_text])
    similarities = cosine_similarity(input_vector, feature_matrix).flatten()
    top_indices = similarities.argsort()[-30:][::-1]
    recommended = []
    for idx in top_indices:
        recommended.extend(df.iloc[idx]['symptoms_list'])
    recommended = [s for s in recommended if s not in input_symptoms]
    symptom_counts = pd.Series(recommended).value_counts()
    if not symptom_counts.empty:
        return symptom_counts.head(top_k).index.tolist()
    else:
        demographic_group = df[
            (df['gender_encoded'] == (0 if input_gender=='male' else 1)) &
            (df['age_bin'] == age_bin)
        ]
        fallback_symptoms = demographic_group['symptoms_list'].explode()
        fallback_symptoms = fallback_symptoms[~fallback_symptoms.isin(input_symptoms)]
        fallback_counts = fallback_symptoms.value_counts()
        return fallback_counts.head(top_k).index.tolist()

# --------------------- FastAPI ---------------------

app = FastAPI()

class SymptomRequest(BaseModel):
    gender: str
    age: int
    symptoms: list

@app.post("/recommend")
def recommend_symptoms_api(request: SymptomRequest):
    recommendations = recommend_symptoms_v2(
        input_gender=request.gender,
        input_age=request.age,
        input_symptoms=request.symptoms,
        top_k=5
    )
    return {"recommendations": recommendations}