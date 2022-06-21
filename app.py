from flask import Flask, render_template, request, redirect
import pickle
import pandas as pd

app = Flask(__name__)

filename = "model/model.sav"
model = pickle.load(open(filename, "rb"))

@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/agreement")
def agreement():
    return render_template("form1.html")

@app.route("/screening", methods=['GET', 'POST'])
def screening():
    agreement = "disagree"
    if request.method == "POST":
        agreement = request.form.get("agreement")
        if agreement == "agree":
            return render_template("form2.html")
        else:
            return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def home():
    df = pd.DataFrame(columns=['Contact', 'Confirmed', 'Symptomps',
            'Allergy','Serious_Illness','Asm_Ep_Dia','Pregnant','Elderly_Physical',
            'Elderly_Disease'])

    if request.method == "POST":
        name = request.form["name"]
        contact = request.form["contact"]
        confirmed = request.form["confirmed"]
        symtopms = request.form["symtopms"]
        allergy = request.form["allergy"]
        ilness = request.form["ilness"]
        asm_ep_dia = request.form["asm_ep_dia"]
        pregnant = request.form["pregnant"]
        elderly_physical = request.form["elderly_physical"]
        elderly_disease = request.form["elderly_disease"]

        df = df.append({'Contact': contact,'Confirmed': confirmed, 'Symptomps': symtopms,
        'Allergy': allergy,'Serious_Illness': ilness,
        'Asm_Ep_Dia': asm_ep_dia,'Pregnant': pregnant,'Elderly_Physical': elderly_physical,
        'Elderly_Disease': elderly_disease}, ignore_index=True)
        
    pred = model.predict(df)
    return render_template('result.html', pred=pred, name=name)

if __name__ == "__main__":
    app.debug=True
    app.run()