from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {"message": "Welcome to Health and Wellness API"}


# ---------------- USERS DATA ----------------

users = [
    {
        "id": 1,
        "name": "Meghana",
        "age": 21,
        "water": 2,
        "sleep": 7,
        "workout": 30,
        "food": ["Rice"],
        "calories": 200
    },
    {
        "id": 2,
        "name": "Rahul",
        "age": 22,
        "water": 1.5,
        "sleep": 6,
        "workout": 20,
        "food": ["Egg"],
        "calories": 78
    },
    {
        "id": 3,
        "name": "Ananya",
        "age": 20,
        "water": 2.5,
        "sleep": 8,
        "workout": 45,
        "food": ["Apple"],
        "calories": 95
    }
]


# ---------------- POST: ADD USER + HEALTH DATA ----------------

class HealthRequest(BaseModel):
    name: str
    age: int
    water: float
    sleep: float
    workout: int
    food: str
    calories: int


@app.post("/add-user")
def add_user(request: HealthRequest):

    new_id = len(users) + 1

    new_user = {
        "id": new_id,
        "name": request.name,
        "age": request.age,
        "water": request.water,
        "sleep": request.sleep,
        "workout": request.workout,
        "food": [request.food],
        "calories": request.calories
    }

    users.append(new_user)

    return {
        "message": "User added successfully",
        "user": new_user
    }


# ---------------- GET: ALL USERS ----------------

@app.get("/users")
def get_users():
    return users


# ---------------- GET: ONE USER ----------------

@app.get("/user/{user_id}")
def get_user(user_id: int):

    for user in users:

        if user["id"] == user_id:
            return user

    return {"message": "User not found"}


# ---------------- PUT: UPDATE SLEEP ----------------

class SleepRequest(BaseModel):
    user_id: int
    hours: float


@app.put("/update-sleep")
def update_sleep(request: SleepRequest):

    for user in users:

        if user["id"] == request.user_id:

            user["sleep"] = request.hours

            return {
                "message": "Sleep updated successfully",
                "user_id": user["id"],
                "sleep_hours": user["sleep"]
            }

    return {"message": "User not found"}


# ---------------- GET: HEALTH SUMMARY ----------------

@app.get("/health-summary/{user_id}")
def health_summary(user_id: int):

    for user in users:

        if user["id"] == user_id:

            if (
                user["water"] >= 2
                and user["sleep"] >= 7
                and user["workout"] >= 30
                and user["calories"] > 0
            ):
                status = "Good"
            else:
                status = "Needs Improvement"

            return {
                "name": user["name"],
                "age": user["age"],
                "water": user["water"],
                "sleep": user["sleep"],
                "workout": user["workout"],
                "food": user["food"],
                "calories": user["calories"],
                "health_status": status
            }

    return {"message": "User not found"}