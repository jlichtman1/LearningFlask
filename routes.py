import os
from flask import Flask, render_template, request, flash, send_file
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:\cygwin64\home\jlichtman\learning-flask\static\input_files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/file-download/')
def file_download():
   return render_template('download.html')

@app.route('/return-file/')
def return_file():
   return send_file('C:\cygwin64\home\jlichtman\learning-flask\static\\20180504_SampleAccessionSpreadsheet.xlsx', attachment_filename='20180504_SampleAccessionSpreadsheet.xlsx')

@app.route('/upload')
def upload_file1():
   return render_template('upload.html')
  
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      if f.filename == '':
          return 'No File'
      if '.csv' not in f.filename:
          return 'Not a CSV file, I swear!'
      filename= secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      fin= open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      outfile= filename.split('.')[0]+'_output.csv'
      fout=open(os.path.join("C:\cygwin64\home\jlichtman\learning-flask\static\output_files",outfile),"w")
    
      first_line= next(fin)
      sample_list=first_line.strip().split(',')[1:]
              
      for line in fin:
          gene_symbol= line.split(',')[0]
          expression_list= line.strip().split(',')[1:]
          for i in range(0,len(sample_list)):
              fout.write(sample_list[i]+','+gene_symbol+','+str(expression_list[i])+'\n')
      fout.close()
      return send_file(os.path.join("C:\cygwin64\home\jlichtman\learning-flask\static\output_files",outfile), attachment_filename= outfile, as_attachment=True)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == "__main__":
  app.run(debug=True)