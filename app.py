from flask import Flask, render_template, request
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
import re
from main import llm_resto, get_workouts, get_foods

# Load .env
load_dotenv()

app = Flask(__name__)

# Prompt template
prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'allergics', 'foodtype', 'workouts', 'foods'],
    template=(
        "Diet Recommendation System:\n"
        "Use the input criteria to give output in the format:\n\n"
        "Restaurants:\n"
        "- name1\n- name2\n- name3\n- name4\n- name5\n- name6\n\n"
        "Breakfast:\n"
        "{foods}\n\n"
        "Dinner:\n"
        "{foods}\n\n"
        "Workouts:\n"
        "{workouts}\n\n"
        "Criteria:\n"
        "Age: {age}, Gender: {gender}, Weight: {weight} kg, Height: {height} m, "
        "Vegetarian: {veg_or_nonveg}, Disease: {disease}, Region: {region}, "
        "Allergics: {allergics}, Food Preference: {foodtype}.\n"
    )
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    age = int(request.form['age'])
    gender = request.form['gender']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    veg_or_nonveg = request.form['veg_or_nonveg']
    disease = request.form['disease']
    region = request.form['region']
    allergics = request.form['allergics']
    foodtype = request.form['foodtype']

    # Age-based workouts and foods
    workouts_for_age = get_workouts(age)
    foods_for_age = get_foods(age)

    # Only suggest restaurants for age >=3
    restaurants_placeholder = ["- Restaurant1", "- Restaurant2", "- Restaurant3", "- Restaurant4", "- Restaurant5", "- Restaurant6"] if age >= 3 else []

    # Prepare inputs for LLM
    input_data = {
        'age': age,
        'gender': gender,
        'weight': weight,
        'height': height,
        'veg_or_nonveg': veg_or_nonveg,
        'disease': disease,
        'region': region,
        'allergics': allergics,
        'foodtype': foodtype,
        'workouts': "\n".join(f"- {w}" for w in workouts_for_age) if workouts_for_age else "- None",
        'foods': "\n".join(f"- {f}" for f in foods_for_age)
    }

    # Run Groq LLM
    from langchain.chains import LLMChain
    chain = LLMChain(llm=llm_resto, prompt=prompt_template_resto)
    results = chain.run(input_data)

    # Regex extraction
    def extract_list(section):
        match = re.search(rf'{section}:\s*(.*?)\n(?:\w+:|$)', results, re.DOTALL)
        return [line.strip("- ") for line in match.group(1).split("\n") if line.strip()] if match else []

    restaurant_names = extract_list('Restaurants') if age >= 3 else []
    breakfast_names = extract_list('Breakfast')
    dinner_names = extract_list('Dinner')
    workout_names = extract_list('Workouts')

    return render_template(
        'result.html',
        restaurant_names=restaurant_names,
        breakfast_names=breakfast_names,
        dinner_names=dinner_names,
        workout_names=workout_names
    )

if __name__ == "__main__":
    app.run(debug=True)
