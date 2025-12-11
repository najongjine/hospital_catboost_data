from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import pandas as pd
from catboost import CatBoostRegressor
import os

router = APIRouter(prefix="/hospital", tags=["Hospital Prediction"])

# --- 모델 로드 로직 (기존과 동일) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'catboost_model.bin')

model = CatBoostRegressor()
if os.path.exists(MODEL_PATH):
    try:
        model.load_model(MODEL_PATH)
        print(f"✅ [Router] 모델 로드 완료: {MODEL_PATH}")
    except Exception as e:
        print(f"❌ [Router] 모델 로드 실패: {e}")
else:
    print(f"⚠️ [Router] 경고: 모델 파일 없음")


# 1. 입력 데이터 모델 정의 (단일 병원 객체)
class HospitalInput(BaseModel):
    id: int               # 병원 ID (필수)
    distance_m: float
    rating: float
    congestion_level: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 101,
                "distance_m": 500,
                "rating": 4.5,
                "congestion_level": 2
            }
        }

# 2. 예측 엔드포인트 정의
# List[HospitalInput]을 사용하여 여러 병원 데이터를 리스트로 받습니다.
@router.post("/predict")
async def predict_score(hospital_list: List[HospitalInput]):
    # 모델 로드 상태 확인
    if model.tree_count_ is None:
        return {
            "success": False,
            "data": None,
            "msg": "AI Server Error: Model is not loaded."
        }

    try:
        # 입력 데이터가 비어있는지 확인
        if not hospital_list:
            return {
                "success": True,
                "data": [],
                "msg": "No hospital data provided."
            }

        # 1. 리스트를 DataFrame으로 변환 (한 번에 예측하기 위함)
        # Pydantic 모델 리스트를 dict 리스트로 변환
        input_data_list = [h.dict() for h in hospital_list]
        df = pd.DataFrame(input_data_list)

        # 2. 예측에 필요한 특성(Feature)만 선택
        # 학습할 때 사용한 특성 순서를 맞춰줍니다.
        X_features = df[['distance_m', 'rating', 'congestion_level']]

        # 3. 일괄 예측 수행 (Batch Prediction)
        predictions = model.predict(X_features)

        # 4. 결과 매핑 및 구조화
        hospital_rank_data = []
        
        # DataFrame의 각 행과 예측 결과를 합칩니다.
        for idx, row in df.iterrows():
            hospital_rank_data.append({
                "id": int(row['id']),
                "predicted_recommendation_score": float(predictions[idx])
            })

        # 5. 점수 기준 내림차순 정렬 (Rank)
        hospital_rank_data.sort(key=lambda x: x['predicted_recommendation_score'], reverse=True)

        # 6. 최종 결과 반환
        return {
            "success": True,
            "data": hospital_rank_data,
            "msg": ""
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "msg": f"AI Server Error: Prediction Error: {str(e)}"
        }