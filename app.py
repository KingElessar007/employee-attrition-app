
import flask
import pickle
import pandas as pd
import os

my_model=pickle.load(open('full_pipeline.pkl','rb'))

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        OverTime = flask.request.form['OverTime']
        MaritalStatus = flask.request.form['MaritalStatus']
        Gender = flask.request.form['Gender']
        Age = flask.request.form['Age']
        StockOptionLevel = flask.request.form['StockOptionLevel']
        MonthlyIncome = flask.request.form['MonthlyIncome']
        YearsAtCompany = flask.request.form['YearsAtCompany']
        DistanceFromHome = flask.request.form['DistanceFromHome']


        # Make DataFrame for model
        test = pd.DataFrame([[OverTime,MaritalStatus,Gender,Age,StockOptionLevel,MonthlyIncome,YearsAtCompany,DistanceFromHome]],
                                       columns=['OverTime','MaritalStatus','Gender','Age','StockOptionLevel','MonthlyIncome','YearsAtCompany','DistanceFromHome'])

       

        prediction=my_model.predict(test)[0]
        
        
        
    
        
        return flask.render_template('main.html',
                                     original_input={'OverTime':OverTime,
                                                     'MaritalStatus':MaritalStatus,
                                                     'Gender':Gender,
                                                     'Age':Age,
                                                     'StockOptionLevel':StockOptionLevel,
                                                     'MonthlyIncome':MonthlyIncome,
                                                     'YearsAtCompany':YearsAtCompany,
                                                     'DistanceFromHome':DistanceFromHome},
                                     result=prediction,
                                     )

# if __name__ == '__main__':
#     app.run()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000)) #Define port so we can map container port to localhost
    app.run(host='0.0.0.0', port=port)  #Define 0.0.0.0 for Docker
