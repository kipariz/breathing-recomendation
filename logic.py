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
