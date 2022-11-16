from flask import Flask, request,render_template
import joblib

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Enter Your API-Key"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route('/')
def predict():
    return render_template('Manual_predict.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
     #  reading the inputs given by the user
     distance = request.form["distance"]
     speed = request.form["speed"]
     temp_inside = request.form["temp_inside"]
     temp_outside = request.form["temp_outside"]
     AC = request.form["AC"]
     rain= request.form["rain"]
     sun = request.form["sun"]
     E10 = request.form["E10"]
     SP98 = request.form["SP98"]
     
     t = [[int(distance),int(speed),int(temp_inside),int(temp_outside),int(AC),int(rain),int(sun),int(E10),int(SP98)]]
     
     payload_scoring = {"input_data": [{"field": [['distance','speed','temp_inside','temp_outside','AC','rain',
                                                   'sun','E10','SP98']], "values": t}]}

     response_scoring = requests.post('Enter Your Scoring End Point', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
     print("Scoring response")
     predictions = response_scoring.json()
     pred = predictions[predictions][0]['values'][0][0]
     print("Final prediction :",pred)
     
     return render_template('Manual_predict.html', \
                           prediction_text=('Car fuel Consumption(L/100km) \
                                            : ',pred))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
