from experta import *
from flask import Flask, render_template, jsonify, request
from werkzeug.exceptions import HTTPException
import traceback
import io
import json

from logic import *

app = Flask(__name__)


expert_prediction = ""
diseases_list = []
diseases_symptoms = []
d_desc_map = {}
symptom_map = {}
match = True


def preprocess():
    global diseases_list, diseases_symptoms, symptom_map, d_desc_map
    diseases = open("diseases.txt")
    diseases_t = diseases.read()
    diseases_list = diseases_t.split("\n")
    diseases.close()
    
    for disease in diseases_list:
        disease_s_file = open("Disease symptoms/" + disease + ".txt")
        disease_s_data = disease_s_file.read()
        s_list = disease_s_data.split("\n")
        diseases_symptoms.append(s_list)
        symptom_map[str(s_list)] = disease
        disease_s_file.close()

        with open("Disease descriptions/" + disease + ".json", "r", encoding="utf8") as disease_s_file:
            disease_s_data = json.load(disease_s_file)
        d_desc_map[disease] = disease_s_data
        disease_s_file.close()


def identify_disease(*arguments):
    symptom_list = []
    for symptom in arguments:
        symptom_list.append(symptom)
    # Handle key error
    return symptom_map[str(symptom_list)]


def get_details(disease):
    
    return d_desc_map[disease]


@app.route('/')
def form():

    return render_template('form.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/process_form', methods=["POST"])
def process_form():
    #air diseases
    respiratory_diseases = None
    if request.method == 'POST':
        if request.form.get('air') != None:
            respiratory_diseases = request.form.getlist('air')

    general_values = {
        'temp': float(request.form['temp']),
        'pulse': int(request.form['pulse']),
        'bp_systolic': int(request.form['bp_systolic']),#not req
        'bp_diastolic': int(request.form['bp_diastolic']),#not req
        'weight': float(request.form['weight']),
        'height': float(request.form['height'])
    }

    phys_value_get = {
        'phys_funct1': int(request.form['phys_funct1']),
        'phys_funct2': int(request.form['phys_funct2']),
        'phys_funct3': int(request.form['phys_funct3']),
        'phys_funct4': int(request.form['phys_funct4']),
        'phys_funct5': int(request.form['phys_funct5']),
        'phys_funct6': int(request.form['phys_funct6']),
        'phys_funct7': int(request.form['phys_funct7']),
        'phys_funct8': int(request.form['phys_funct8']),
        'phys_funct9': int(request.form['phys_funct9']),
        'phys_funct10': int(request.form['phys_funct10'])
    }

    phys_value_arr = []

    for i in phys_value_get.values():
        phys_value_arr.append(i)

    #physical functioning value
    physical_functioning(phys_value_arr)

    #emotional 
    emotional_value = None
    if request.method == 'POST':
        if request.form.get('emotional') == None:
            emotional_value = 100
        else:
            emotional_value = role_emotional(
                len(request.form.getlist('emotional')))

    bmi = calculate_bmi(general_values['height'], general_values['weight'])

    #bodily pain value
    bodily_pain([int(request.form['pain_slider1']),
                       int(request.form['pain_slider2'])])
    
   
    #alert for air diseases
    def respiratory_danger(respiratory_diseases):
        if (len(respiratory_diseases)>=2):
            return True
        else:
            return False
    
    # print("cough" in respiratory_diseases)
    def data_for_expert():
        pass

    output_values = {
        "BMI": bmi,
        "bmi_result": interpreter_bmi(bmi)
    }

    class Greetings(KnowledgeEngine):

        @DefFacts()
        def _initial_action(self):

            yield Fact(action="find_disease")

        @Rule(Fact(action='find_disease'), NOT(Fact(headache=W())), salience=1)
        def symptom_0(self):
            # self.declare(Fact(headache=input("headache: "))) int(request.form['expert_input']
            self.declare(Fact(headache="yes"))

        @Rule(Fact(action='find_disease'), NOT(Fact(back_pain=W())), salience=1)
        def symptom_1(self):
            self.declare(Fact(back_pain="yes"))

        @Rule(Fact(action='find_disease'), NOT(Fact(chest_pain=W())), salience=1)
        def symptom_2(self):
            self.declare(Fact(chest_pain="yes"))

        @Rule(Fact(action='find_disease'), NOT(Fact(cough=W())), salience=1)
        def symptom_3(self):
            self.declare(Fact(cough="no"))

        @Rule(Fact(action='find_disease'), NOT(Fact(fainting=W())), salience=1)
        def symptom_4(self):
            self.declare(Fact(fainting="no"))

        @Rule(Fact(action='find_disease'), NOT(Fact(fatigue=W())), salience=1)
        def symptom_5(self):
            self.declare(Fact(fatigue="no"))

        @Rule(Fact(action='find_disease'), NOT(Fact(sunken_eyes=W())), salience=1)
        def symptom_6(self):
            self.declare(Fact(sunken_eyes="no"))

        @Rule(Fact(action='find_disease'), NOT(Fact(low_body_temp=W())), salience=1)
        def symptom_7(self):
            self.declare(Fact(low_body_temp="no"))

        @Rule(Fact(action='find_disease'), NOT(Fact(restlessness=W())), salience=1)
        def symptom_8(self):
            self.declare(Fact(restlessness="no"))

        @Rule(Fact(action='find_disease'), NOT(Fact(sore_throat=W())), salience=1)
        def symptom_9(self):
            self.declare(Fact(sore_throat="no"))

        @Rule(Fact(action='find_disease'), NOT(Fact(fever=W())), salience=1)
        def symptom_10(self):
            self.declare(Fact(fever="no"))

        @Rule(Fact(action='find_disease'), NOT(Fact(nausea=W())), salience=1)
        def symptom_11(self):
            self.declare(Fact(nausea="no"))

        @Rule(Fact(action='find_disease'), NOT(Fact(blurred_vision=W())), salience=1)
        def symptom_12(self):
            self.declare(Fact(blurred_vision="no"))

        @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"), Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="yes"), Fact(restlessness="no"), Fact(low_body_temp="no"), Fact(fever="yes"), Fact(sunken_eyes="no"), Fact(nausea="yes"), Fact(blurred_vision="no"))
        def disease_0(self):
            self.declare(Fact(disease="Jaundice"))

        @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"), Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="yes"), Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="no"), Fact(blurred_vision="no"))
        def disease_1(self):
            self.declare(Fact(disease="Alzheimers"))

        @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="yes"), Fact(chest_pain="no"), Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="yes"), Fact(restlessness="no"), Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="no"), Fact(blurred_vision="no"))
        def disease_2(self):
            self.declare(Fact(disease="Arthritis"))

        @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="yes"), Fact(cough="yes"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="no"), Fact(low_body_temp="no"), Fact(fever="yes"), Fact(sunken_eyes="no"), Fact(nausea="no"), Fact(blurred_vision="no"))
        def disease_3(self):
            self.declare(Fact(disease="Tuberculosis"))

        @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="yes"), Fact(cough="yes"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="yes"), Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="no"), Fact(blurred_vision="no"))
        def disease_4(self):
            self.declare(Fact(disease="Asthma"))

        @Rule(Fact(action='find_disease'), Fact(headache="yes"), Fact(back_pain="no"), Fact(chest_pain="no"), Fact(cough="yes"), Fact(fainting="no"), Fact(sore_throat="yes"), Fact(fatigue="no"), Fact(restlessness="no"), Fact(low_body_temp="no"), Fact(fever="yes"), Fact(sunken_eyes="no"), Fact(nausea="no"), Fact(blurred_vision="no"))
        def disease_5(self):
            self.declare(Fact(disease="Sinusitis"))

        @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"), Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="yes"), Fact(restlessness="no"), Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="no"), Fact(blurred_vision="no"))
        def disease_6(self):
            self.declare(Fact(disease="Epilepsy"))

        @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="yes"), Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="no"), Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="yes"), Fact(blurred_vision="no"))
        def disease_7(self):
            self.declare(Fact(disease="Heart Disease"))

        @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"), Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="yes"), Fact(restlessness="no"), Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="yes"), Fact(blurred_vision="yes"))
        def disease_8(self):
            self.declare(Fact(disease="Diabetes"))

        @Rule(Fact(action='find_disease'), Fact(headache="yes"), Fact(back_pain="no"), Fact(chest_pain="no"), Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="no"), Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="yes"), Fact(blurred_vision="yes"))
        def disease_9(self):
            self.declare(Fact(disease="Glaucoma"))

        @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"), Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="yes"), Fact(restlessness="no"), Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="yes"), Fact(blurred_vision="no"))
        def disease_10(self):
            self.declare(Fact(disease="Hyperthyroidism"))

        @Rule(Fact(action='find_disease'), Fact(headache="yes"), Fact(back_pain="no"), Fact(chest_pain="no"), Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="no"), Fact(low_body_temp="no"), Fact(fever="yes"), Fact(sunken_eyes="no"), Fact(nausea="yes"), Fact(blurred_vision="no"))
        def disease_11(self):
            self.declare(Fact(disease="Heat Stroke"))

        @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"), Fact(cough="no"), Fact(fainting="yes"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="no"), Fact(low_body_temp="yes"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="no"), Fact(blurred_vision="no"))
        def disease_12(self):
            self.declare(Fact(disease="Hypothermia"))

        @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"), Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="no"), Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="no"), Fact(blurred_vision="no"))
        def disease_13(self):
            self.declare(Fact(disease="no-disease"))

        @Rule(Fact(action='find_disease'), Fact(disease=MATCH.disease), salience=-998)
        def disease(self, disease):
            global expert_prediction 

            id_disease = disease
            disease_details = get_details(id_disease)

            expert_prediction = disease_details 

        @Rule(Fact(action='find_disease'),
            Fact(headache=MATCH.headache),
            Fact(back_pain=MATCH.back_pain),
            Fact(chest_pain=MATCH.chest_pain),
            Fact(cough=MATCH.cough),
            Fact(fainting=MATCH.fainting),
            Fact(sore_throat=MATCH.sore_throat),
            Fact(fatigue=MATCH.fatigue),
            Fact(low_body_temp=MATCH.low_body_temp),
            Fact(restlessness=MATCH.restlessness),
            Fact(fever=MATCH.fever),
            Fact(sunken_eyes=MATCH.sunken_eyes),
            Fact(nausea=MATCH.nausea),
            Fact(blurred_vision=MATCH.blurred_vision), NOT(Fact(disease=MATCH.disease)), salience=-999)
       
        def not_matched(self, headache, back_pain, chest_pain, cough, fainting, sore_throat, fatigue, restlessness, low_body_temp, fever, sunken_eyes, nausea, blurred_vision):
            global match
            match = False

            lis = [headache, back_pain, chest_pain, cough, fainting, sore_throat, fatigue,
                restlessness, low_body_temp, fever, sunken_eyes, nausea, blurred_vision]
            max_count = 0
            max_disease = ""
            for key, val in symptom_map.items():
                count = 0
                temp_list = eval(key)
                for j in range(0, len(lis)):
                    if(temp_list[j] == lis[j] and lis[j] == "yes"):
                        count = count + 1
                if count > max_count:
                    max_count = count
                    max_disease = val
            self.disease(max_disease)

    preprocess()
    engine = Greetings()
    engine.reset()
    engine.run()


    return render_template('results.html', output_values=output_values, expert_prediction=expert_prediction, match=match)


if __name__ == "__main__":
    print("* Starting Flask server..."
          "please wait until server has fully started")
    app.run(host='0.0.0.0', debug=True)
