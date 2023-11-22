from flask import Flask, render_template , request , jsonify
from flask_cors import CORS
from chat import get_response
from chat import voice_search_apna


app= Flask(__name__)
CORS(app)

#@app.get("/")
#def index_get():
 #   return render_template("base.html")


@app.post("/predict")
def predict():
    text=request.get_json().get("message")

    response = get_response(text)
    #response= voice_search_apna()
    #response=get_response(response)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
