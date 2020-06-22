import PyPDF2 as pdfre
from summarizer import Summarizer
from flask import Flask , request , render_template , flash,redirect, url_for
from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docs'}
def get_info(path):
    list_txt = []
    with open(path,'rb' ) as f:
        read = pdfre.PdfFileReader(f)
        info=read.getDocumentInfo()

        for i in range(read.getNumPages()):
            txt = read.getPage(i).extractText()
            summ = model(txt)
            txt = ''.join(summ)
            list_txt.append((i+1,summ))
    os.unlink(path)
    return list_txt



UPLOAD_FOLDER = os.path.join(os.getcwd(),'uploads')
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route("/")
def hello():

    return render_template('home.html')


@app.route("/predict" , methods = ['POST'])
def predict():
    if request.method == 'POST':

        file = request.files['upload']

        if file.filename == '':
            flash('NO selected file')
            return redirect('/')

        if file.filename.split(".")[1] not in ALLOWED_EXTENSIONS:
            return redirect("/")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'] , filename).replace("\\" , "/")
            file.save(path)
            full = get_info(path)



    return render_template('predict.html' , dict_pages = full)

@app.route("/predict2" , methods = ['POST'])
def predict2():
    if request.method == 'POST':
        lst = []
        message = request.form['message']
        data = [message][0]
        if str(data) == ' ':
            return redirect("/")
        summ = model(data)
        txt = ''.join(summ)
        lst.append((1,summ))

    return render_template('predict.html' , dict_pages = lst)


if __name__ == '__main__':
    model = Summarizer()
    print('MODEL LOADED SUCCESS')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug = True)
