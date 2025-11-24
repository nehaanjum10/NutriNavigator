from flask import Flask, render_template, request
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os
import re

# Load .env file for local API key
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Groq LLM with API key from environment
llm_resto = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.0
)

# Prompt template
prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'allergics', 'foodtype'],
    template=(
        "Diet Recommendation System:\n"
        "I want you to provide output in the following format using the input criteria:\n\n"
        "Restaurants:\n"
        "- name1\n- name2\n- name3\n- name4\n- name5\n- name6\n\n"
        "Breakfast:\n"
        "- item1\n- item2\n- item3\n- item4\n- item5\n- item6\n\n"
        "Dinner:\n"
        "- item1\n- item2\n- item3\n- item4\n- item5\n\n"
        "Workouts:\n"
        "- workout1\n- workout2\n- workout3\n- workout4\n- workout5\n- workout6\n\n"
        "Criteria:\n"
        "Age: {age}, Gender: {gender}, Weight: {weight} kg, Height: {height} ft, "
        "Vegetarian: {veg_or_nonveg}, Disease: {disease}, Region: {region}, "
        "Allergics: {allergics}, Food Preference: {foodtype}.\n"
    )
)

# Home route
@app.route('/')
def index():
    return render_template("index.html")

# Recommendation route
@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == "POST":
        # Collect form data
        age = int(request.form['age'])
        gender = request.form['gender']  # fixed trailing comma
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        veg_or_nonveg = request.form['veg_or_nonveg']
        disease = request.form['disease']
        region = request.form['region']
        allergics = request.form['allergics']
        foodtype = request.form['foodtype']

        # Initialize LLMChain
        chain = LLMChain(llm=llm_resto, prompt=prompt_template_resto)

        input_data = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'veg_or_nonveg': veg_or_nonveg,
            'disease': disease,
            'region': region,
            'allergics': allergics,
            'foodtype': foodtype
        }

        # Run the chain
        results = chain.run(input_data)

        # Extract lists using regex
        def extract_list(section):
            match = re.search(rf'{section}:\s*(.*?)\n(?:\w+:|$)', results, re.DOTALL)
            return [line.strip("- ") for line in match.group(1).split("\n") if line.strip()] if match else []

        restaurant_names = extract_list('Restaurants')
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

    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
