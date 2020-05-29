def calculate_bmi(height_cm, weight_kg):
    """
    Calculates BMI given height (in kg), and weight (in cm)
    BMI Formula: kg / m^2
    Output is BMI, rounded to one decimal digit
    """
    # Input height is in cm, so we divide by 100 to convert to metres
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

def interpreter_bmi(bmi):
    if bmi < 18.5:
        return "Ваша вага нижче норми!"
    elif 18.5 <= bmi < 25:
        return "Ви маєте нормальну вагу"
    elif 25 <= bmi < 30:
        return "Ви маєте надлишкову вага"
    elif 25 <= bmi < 30:
        return "У вас ожиріння 1 ступеню"
    elif 35 <= bmi < 40:
        return "У вас ожиріння 2 ступеню"
    elif 40 <= bmi:
        return "У вас ожиріння 3 ступеню"

def interpreter_sf(sf):
    if sf < 30:
        return "Ви маєте дуже поганий загальний рівень здоров'я."
    elif 30 <= sf < 60:
        return "Ви маєте поганий загальний рівень здоров'я."
    elif 60 <= sf < 80:
        return "Ви маєте досить загальний добрий рівень здоров'я."
    elif 80 <= sf <= 100:
        return "Ви маєте добрий загальний рівень здоров'я."

def interpreter_emotional(sf):
    if sf < 30:
        return "Ви маєте дуже поганий психічного здоров'я."
    elif 30 <= sf < 60:
        return "Ви маєте поганий рівень психічного здоров'я."
    elif 60 <= sf < 80:
        return "Ви маєте досить добрий рівень психічного здоров'я."
    elif 80 <= sf <= 100:
        return "Ви маєте добрий рівень психічного здоров'я."

def interpreter_physic(sf):
    if sf < 30:
        return "Ви маєте дуже поганий рівень фізичного здоров'я."
    elif 30 <= sf < 60:
        return "Ви маєте поганий рівень фізичного здоров'я."
    elif 60 <= sf < 80:
        return "Ви маєте досить добрий фізичного рівень здоров'я."
    elif 80 <= sf <= 100:
        return "Ви маєте добрий рівень фізичного здоров'я."
    
def check_general_param(temp, pulse, bp_systolic, bp_diastolic):
    
    if (temp < 36 or temp > 37):
        return "no"
    elif (pulse < 60 or pulse > 120):
        return "no"
    elif (bp_systolic < 115 or bp_systolic > 130):
        return "no"
    elif (bp_diastolic < 60 or bp_diastolic > 90):
        return "no"
    else:
        return "normal"

def recomendation(sf, bmi):
    if ((70 <= sf < 100) and (18.5 <= bmi < 30)):
        return "normal"
    elif ((40 <= sf < 70) or (30 <= bmi < 40)):
        return "easy"
    else:
        return "no"

def respiratory_danger(respiratory_diseases):
    try:
        if len(respiratory_diseases)>=3:
            return "no"
        elif (len(respiratory_diseases)==2):
            return "easy"
        else: return "normal"
    except TypeError:
        return "normal"


def rewrite_health_param(new_value, health):
    if ((health == 'easy') and (new_value == 'normal')):
        return health
    elif ((health == 'no') and ( (new_value == 'easy') or (new_value == 'normal'))):
        return health
    else:
        return new_value


def average(lst): 
    return sum(lst) / len(lst) 

"""     SF-36  
Показатели каждой шкалы составлены таким образом, что чем выше значение показателя (от 0 до 100), 
тем лучше оценка по избранной шкале. """

"""Інтенсивність болі (Bodily pain — BP);"""
def bodily_pain(params):
    """ get 2 slider params return pain score ex.[] 
    if emotional < 60 -> трохи погано  
    if emotional < 30 -> зовсім погано  """

    score = average(params)
    return score  

"""ролевое функционирование, обусловленное эмоциональным состоянием (Role-Emotional — RE);"""
def role_emotional(data):
    """get 3 binary param from checkbox return emotional characteristic ex. [0,1,0]"""
    """ if emotional < 60 -> трохи погано  """
    """ if emotional < 30 -> зовсім погано  """
    if data == 1:
        return 66
    elif data == 2:
        return 33 
    elif data == 3:
        return 0 


def physical_convert(data):
    if data == 1:
        return 0
    elif data == 2:
        return 50
    elif data == 3:
        return 100

"""физическое функционирование (Physical Functioning — PF);"""
def physical_functioning(params):
    """get 10 parameters in array return physical score. ex: [2,3,1,2,3,2,2,3,2,3]
    Так, сильно обмежує = 1 = 0
    Так, трохи обмежує = 2 = 50
    Ні, зовсім не обмежує = 3 = 100
    if emotional < 60 -> трохи погано  
    if emotional < 30 -> зовсім погано  """

    in_data = []
    for param in params:
        in_data.append(physical_convert(param))

    score = average(in_data)
    return score 
