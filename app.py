from flask import Flask,render_template,url_for,request,session,redirect,flash
from datetime import timedelta
import datetime 
import json
import pickle
import pandas as pd

model=pickle.load(open('xgb_best_model.pickle','rb'))

app=Flask(__name__)
app.secret_key="trupen"
app.permanent_session_lifetime=timedelta(days=5)

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/predict",methods=["POST","GET"])
def predict():
    if request.method=="POST":
        session.permanent=True
        data=request.form["jd"]
        # data1=request.form["d1"]
        # wd=request.form["wd"]
        print(type(data))
        d1=json.loads(data)
        d1.update((x,[y])for x, y in d1.items())
        data_df=pd.DataFrame.from_dict(d1)
        d1=model.predict(data_df)
        session["result"]=str(d1[0])
        # d1=json.loads(data)
        # print(d1)
        day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        # day = datetime(str(data), '%d-%m-%Y').weekday()
        # print(day_name[day])
        return redirect(url_for("result"))
    else:
        if "result" in session:
            return redirect(url_for("result"))
        return render_template("prediction.html")

@app.route('/result')
def result():
    if "result" in session:
        data=session["result"]
        # flash("Already entered a date")
        return render_template("result.html",val=data)
    else:
        flash("Already entered a date")
        return redirect(url_for("predict"))

@app.route('/next')
def next():
    if "result" in session:
        data=session["result"]
        flash("You have been logged out!","info")

    session.pop("result",None)
    return redirect(url_for("predict"))



if __name__ =="__main__":
    app.run(debug=True)
    