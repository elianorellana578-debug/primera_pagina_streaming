
def user_model(user) -> dict:
    return {
        "id": str(user["_id"]),
        "title": user["title"],
        "description": user["description"],
        "genres": user["genres"],
        "year": user["year"],
        "video_url": user["video_url"],
        "is_premium": user["is_premium"]
    }
    
def user_model_all(list_movies):
    return [user_model(movie) for movie in list_movies]

def usuario_model(user) -> dict:
    return {
        "id": user.get("_id"),
        "username": user.get("username"),
        "email": user.get("email"),
        "password": user.get("password")
    }
    
def usuario_model(user):
    return {
        "id": str(user.get("_id")),
        "username": user.get("username"),
        "email": user.get("email"),
        "password": user.get("password")
    }
    
def usuario_model_all(list_user):
    return [usuario_model(user) for user in list_user]