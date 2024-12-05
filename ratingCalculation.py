def calculate_rating(row, enemy_item):
    # Assign weights to each attribute
    health_weight = 1.5
    speed_weight = 1.2
    dps_weight = 2.0
    target_weight = 1.0
    respawn_weight = -1.0
    cost_weight = -0.5
    range_bonus = 3.0  # Additional bonus for range superiority
    type_bonus = 5.0  # Significant boost for matching types

    # Start with weighted attributes
    rating = (
            row['Health'] * health_weight +
            row['Speed'] * speed_weight +
            row['DPS'] * dps_weight +
            # row['Target'] * target_weight +
            row['Respawn'] * respawn_weight +
            row['Cost'] * cost_weight
    )

    # Add bonus for range superiority
    if row['Range'] > enemy_item['Range']:
        rating += range_bonus

    # Add bonus if types match
    matching_types = set(row['Types']).intersection(set(enemy_item['Types']))
    if matching_types:
        rating += type_bonus * len(matching_types)

    return rating



# Calculate the overall rating by considering all enemies
def calculate_overall_rating(row, enemy_frame):
    ratings = []
    for _, enemy_item in enemy_frame.iterrows():
        rating = calculate_rating(row, enemy_item)
        ratings.append(rating)
    return sum(ratings) / len(ratings)  # Average rating across all enemies