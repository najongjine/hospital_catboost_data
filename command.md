hospital_catboost_traindata3.json

- 파일을 생성.

- 데이터 형식은
  {
  "recommendation_data": [
  {
  "distance_m": 100,
  "rating": 5,
  "congestion_level": 1,
  "recommendation_score": 0.99
  },
  {
  "distance_m": 200,
  "rating": 4.0,
  "congestion_level": 2,
  "recommendation_score": 0.8
  },
  ...
  ]
  }

이런 형식으로 되야함.

- distance_m : 내 위치로부터 목적지 까지의 거리. 걸어가는 기준. 0~2000 까지. 가까울수록 좋은거임
- rating : 평점. 1~5 정수. 2이하 나쁨. 4 이상 좋음. 3 은 그냥 보통. 평점은 높을수록 좋은거임
- congestion_level : 혼잡도 레벨. 1 여유로움. 2 는 그냥 보통. 3은 손님 많음
- recommendation_score : 추천 점수. 점수가 높을수록 추천함

- 예제:
  distance_m 100, rating 4, congestion_level 1
  이러면 recommendation_score 점수를 높게 줘야함

distance_m 800, rating 3, congestion_level 2
이렇게 거리도 좀 멀고 평점도 보통이고 혼잡도도 보통이면 recommendation_score 를 어중간하게 줘야함

distance_m 100, rating 4, congestion_level 3
이렇게 거리도 가깝고 평점도 좋은데 congestion_level 이 혼잡이면
recommendation_score 를 어중간하게 줘야함

distance_m 100, rating 1, congestion_level 1
이렇게 거리도 가깝고 손님도 없는데 평점이 나쁘면 recommendation_score 를 낮게 줘야함

- 니가 목적지까지 걸어서 찾아가는 손님인데, distance_m, rating, congestion_level 를 종합적으로
  생각해서 recommendation_score 를 어떻게 줘야할지 전문가 처럼 생각해야해.

- 데이터 1000 개를 만들어줘.
