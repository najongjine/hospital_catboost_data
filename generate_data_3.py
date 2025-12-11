import json
import random

def generate_recommendation_data(num_entries=1000): # Changed num_entries to 1000
    data = []
    for _ in range(num_entries):
        distance_m = random.randint(0, 2000)
        rating = random.randint(1, 5)
        congestion_level = random.randint(1, 3)

        # Normalize values to 0-1 range
        norm_dist = (2000 - distance_m) / 2000
        norm_rating = (rating - 1) / 4
        norm_congestion = (3 - congestion_level) / 2

        # Calculate recommendation score with weights
        # Higher weights for distance and rating, lower for congestion
        recommendation_score = (
            0.4 * norm_dist +
            0.4 * norm_rating +
            0.2 * norm_congestion
        )

        # Ensure score is within 0-1 range and round to 2 decimal places
        recommendation_score = round(max(0.0, min(1.0, recommendation_score)), 4)

        entry = {
            "distance_m": distance_m,
            "rating": float(rating), # Ensure rating is a float as in example
            "congestion_level": congestion_level,
            "recommendation_score": recommendation_score
        }
        data.append(entry)
    return {"recommendation_data": data}

if __name__ == "__main__":
    generated_data = generate_recommendation_data()
    file_path = "hospital_catboost_traindata3.json" # Changed output file name
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(generated_data, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(generated_data['recommendation_data'])} entries and saved to {file_path}")
