from calculate import *
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
@app.route("/home")
def home():
    return render_template("index.html")
@app.route('/result',methods=['POST','GET'])
def calc():
    convection=request.form["convection"]
    velocity=request.form["velocity"]
    typeht=request.form["typeht"]
    shape=request.form["shape"]
    length=request.form["length"]
    breadth=request.form["breadth"]
    thickness=request.form["thickness"]
    surftemp=request.form["surftemp"]
    surrtemp=request.form["surrtemp"]
    name=display(convection,velocity,typeht,shape,length,breadth,thickness,surftemp,surrtemp)
    return render_template("index.html",name=name)
if __name__=="__main__":
    app.run(debug=True)
