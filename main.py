from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
import os

# Initialize Groq API
llm_resto = ChatGroq(
    api_key=os.getenv("API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.0
)

# Age-based workouts mapping
AGE_WORKOUTS = {
    (1, 2): [],  # No workouts
    (3, 5): ["Roping", "Stretching", "Yoga"],
    (5, 20): ["Jogging", "Sports", "Skipping", "Calisthenics", "Yoga"],
    (20, 35): ["Strength training", "Running", "HIIT", "Swimming", "Yoga"],
    (35, 50): ["Cardio", "Light strength", "Cycling", "Swimming", "Yoga"],
    (50, 65): ["Walking", "Stretching", "Light yoga", "Balance exercises", "Breathing exercises"],
    (65, 80): ["Chair yoga", "Stretching", "Slow walking", "Breathing exercises", "Light aerobics"],
    (80, 95): ["Chair exercises", "Slow stretching", "Breathing exercises", "Light mobility exercises"],
    (95, 100): ["Chair exercises", "Breathing exercises", "Slow stretching", "Light mobility"]
}

def get_workouts(age):
    for (start, end), workouts in AGE_WORKOUTS.items():
        if start <= age <= end:
            return workouts
    return []

# Age-based diet recommendations (simplified, you can expand)
AGE_FOODS = {
    (1, 2): ["Milk", "Soft mashed fruits"],
    (3, 5): ["Rice", "Boiled vegetables", "Soft fruits"],
    (6, 15): ["Rice", "Dal", "Vegetables", "Fruits", "Eggs/Chicken for non-veg"],
    (16, 30): ["Balanced meals with carbs, protein, veggies, fruits"],
    (31, 50): ["Low fat meals, veggies, protein rich diet"],
    (51, 70): ["Easily digestible meals, porridge, soups, fruits"],
    (71, 100): ["Soft foods, soups, easy digestible meals, fruits"]
}

def get_foods(age):
    for (start, end), foods in AGE_FOODS.items():
        if start <= age <= end:
            return foods
    return ["Balanced diet"]
