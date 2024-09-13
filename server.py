import os
import shutil
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from analysis_creator import create_results  # Assuming this is defined in your code.
from hashlib import sha256

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'  # Required for session and flash messages

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    if request.method == 'POST':
        # Recreate 'uploads' directory if it exists, else create it
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            shutil.rmtree(app.config['UPLOAD_FOLDER'])
        os.makedirs(app.config['UPLOAD_FOLDER'])

        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        passw = request.form['pw']

        passw = sha256(passw.encode('utf-8')).hexdigest()
        
        numid = request.form['id']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('upload_file', name="empty_file"))
        
        # Check if the file extension is allowed
        if not allowed_file(file.filename):
            flash('Invalid file type. Only ZIP files are allowed.')
            return redirect(url_for('upload_file', name="wrong_file_type"))

        # Save the file
        if file and allowed_file(file.filename) and passw == 'f3e055913a0b1eb0f07317896f9a1bc466b9a50db85a7f882f3ffde9ffb23aca':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Call your create_results function (this needs to create the 'result' file in 'uploads' directory)
            create_results(numid)  # Make sure this function is defined and generates the result file

            # Redirect to show results page
            return redirect(url_for('show_results'))

    # Recreate 'uploads' directory if it exists, else create it
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    os.makedirs(app.config['UPLOAD_FOLDER'])

    # HTML form for uploading a file
    return render_template('landing.html')
    

# Route to show results page and provide download link for the result file
@app.route('/results')
def show_results():
    
    images = os.listdir('uploads/result')
    
    log_file = [text_file for text_file in images if text_file.endswith('.txt')]

    log_text = ''

    with open(f'uploads/result/{log_file[0]}', 'r') as file:
        for i in file.readlines():
            log_text += i + '<br>'

    images = [image for image in images if image.endswith('.svg')]

    return f'''
    
    <!doctype html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="icon" type="image/x-icon" href="{ url_for('static', filename='favicon.ico') }">
    </head>
    <title>Results</title>
    
    <div class="container-fluid">
    
    <h1>Results</h1>

    {''.join(f'<li><img src="/uploads/result/{image}" class="rounded"></img></li>' for image in images)}
    
    </div>

    <div class="container-fluid">
    <p class="lead">Log file: {log_text}</p>
    </div>
    
    <div class="container-fluid">
    
    <h1>Download</h1>
    <p>Images:</p>
    <ul>
    {''.join(f'<li><a href="/uploads/result/{image}" download>{image}</a></li>' for image in images)}
    </ul>
    <p>Download all images as zip:</p>
    <a href="/uploads/result.zip" download>Download Results</a>
    </div>
    '''

# Route to serve the uploaded result file (adjust the filename if needed)
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploads/result/<filename>')
def download_result_file(filename):
    return send_from_directory('uploads/result', filename)

if __name__ == '__main__':
    app.run(debug=True)
