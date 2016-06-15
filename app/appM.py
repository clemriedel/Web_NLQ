import os
import pandas as pd
import flask.views
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from test import clem_lda

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "bacon"

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/home')
def index():
    return render_template('indexM.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/ds4all_nlq_video')
def ds4all_nlq_video():
    return play('ds4all_nlq.mp4')




@app.route('/predict', methods=['POST'])
def predcit():
    file_name = request.form['file_name']
    files = os.listdir('uploads')
    if file_name not in files:
        return 'File does not exist'

    a = ('uploads/{}'.format(file_name))

    z = clem_lda(a)

    return str(z) #, str(df.head())




    


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        #return 1
        #redirect(url_for('uploaded_file', filename=filename))
        return redirect("/home")


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

class View(flask.views.MethodView):
    def get(self):
        return flask.render_template('indexM.html')

    def post(self):
        result = eval(flask.request.form['expression'])
        flask.flash(result)
        return self.get()
    
app.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])

app.debug = True
app.run()


