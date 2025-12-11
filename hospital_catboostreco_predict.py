import pandas as pd
from catboost import CatBoostRegressor

# 1. 모델 파일 경로 설정
MODEL_PATH = 'catboost_model.bin'

# 2. CatBoost 모델 로드
# CatBoostRegressor 클래스를 사용하여 모델을 로드합니다.
try:
    model = CatBoostRegressor()
    model.load_model(MODEL_PATH)
    print(f"✅ CatBoost 모델을 '{MODEL_PATH}'에서 성공적으로 로드했습니다.")
except Exception as e:
    print(f"❌ 모델 로드 중 오류 발생: {e}")
    print("모델 파일이 현재 디렉토리에 있는지, 파일 이름이 'catboost_model.bin'이 맞는지 확인해 주세요.")
    exit()

# 3. 예측에 사용할 새로운 데이터 준비
# 학습 시 사용했던 특성 순서와 개수를 맞춰야 합니다: ['distance_m', 'rating', 'congestion_level']
# 예시 데이터:
# - 첫 번째 병원: 거리 500m, 평점 4.5, 혼잡도 2 (낮음)
# - 두 번째 병원: 거리 3000m, 평점 3.8, 혼잡도 5 (높음)
# - 세 번째 병원: 거리 800m, 평점 4.9, 혼잡도 3 (보통)
new_data = pd.DataFrame({
    'distance_m': [500, 3000, 800],
    'rating': [4.5, 3.8, 4.9],
    'congestion_level': [3, 1, 1]
})

# 4. 예측 수행
# model.predict() 함수를 사용하여 예측합니다.
predictions = model.predict(new_data)

# 5. 결과 출력
new_data['predicted_recommendation_score'] = predictions

print("\n--- 예측 결과 ---")
print(predictions)
print("\n가장 높은 예측 점수(추천 점수)를 가진 병원:")
# 가장 높은 예측 점수를 가진 행을 찾아서 출력
most_recommended = new_data.loc[new_data['predicted_recommendation_score'].idxmax()]
print(most_recommended)