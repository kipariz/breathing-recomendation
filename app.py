from flask import Flask, render_template, jsonify, request
from werkzeug.exceptions import HTTPException
import traceback
import io

from logic import *

app = Flask(__name__)


@app.route('/')
def form():

    return render_template('form.html')
    

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/process_form', methods=["POST"])
def process_form():
    
    values = {
        # 'temp': int(request.form['temp']),
        # 'pulse': int(request.form['pulse']),
        # 'bp_systolic': int(request.form['bp_systolic']),
        # 'bp_diastolic': int(request.form['bp_diastolic']),
        'weight': float(request.form['weight']),
        'height': float(request.form['height'])
    }

    phys_value_get = {
        'phys_funct1' : int(request.form['phys_funct1']),
        'phys_funct2' : int(request.form['phys_funct2']),
        'phys_funct3' : int(request.form['phys_funct3'])
    }
    
    phys_value_arr = []
    
    print(phys_value_get)

    for i in phys_value_get.values():
        phys_value_arr.append(i)

    print(physical_functioning(phys_value_arr))

    if request.method == 'POST':
        if request.form.get('emotional') == None:
            print("emotional =", 100)
        else:
            print("emotional =", role_emotional(len(request.form.getlist('emotional'))))

    bmi = calculate_bmi(values['height'], values['weight'])

    print(bodily_pain([int(request.form['pain_slider1']),int(request.form['pain_slider2'])] ) )

    input_values = {
        "BMI": bmi,
        "bmi_result": interpreter_bmi(bmi),
        "Step 3": 3,
        "Step 4": 4,
        "Step 5": 5
    }

    return render_template('results.html', input_values=input_values)

if __name__ == "__main__":
    print("* Starting Flask server..."
          "please wait until server has fully started")
    app.run(host='0.0.0.0', debug=True)