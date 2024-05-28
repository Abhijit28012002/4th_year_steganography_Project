from flask import Flask,render_template,request,Response,send_from_directory,redirect
from PIL import Image
import os
from encodeAndDecodeImage import encode_image,decode_image
from encodeAndDecodeVideo import encode_text,decode_text


app=Flask(__name__)

# Save Image Formater
ALLOWED_EXTENSIONS_Images = {'png', 'jpg', 'jpeg'}

#make  directory to save picture and videos
directory_list=['./static/images','./static/images/encode_Images','./static/images/encode_Videos','./static/images/Download','./static/images/decodeImages']

for i in directory_list:
    try:
        os.mkdir(i)
    except OSError as error:
        pass

# Save Images Directory variable
save_directory = './static/images/encode_Images/'

# Specify directory to download from . . .
DOWNLOAD_DIRECTORY = "./static/images/Download/"

# Save Videos Variables
app.config['UPLOAD_FOLDER'] = './static/images/encode_Videos/'
app.config['ALLOWED_EXTENSIONS_Videos'] = {'mp4', 'avi', 'mkv', 'mov'}  # Add more file extensions as needed

accept_image={'png'}
def allowed_file_accept_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in accept_image

# Allow Videos File Allow Function
def allowed_file_Videos(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS_Videos']


# Home Page for steganography Project
@app.route("/")
def Home():
    return render_template("home.html")

# About Page for steganography Project
@app.route("/about")
def about():
    return render_template("about.html")

# Allow Images File Function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_Images


@app.route('/shareFile')
def shareFile():
    return render_template('shareFile.html')

@app.route('/shareFile',methods=['POST'])
def shareFileRequest():
    sharefile = request.form['sendprocess']
    return render_template('shareFile.html',sendprocess=sharefile)

########### Encode Image & Video Page ############################
@app.route('/localImage')
def localImage():
    return render_template('localImage.html')

################### Encode Images and Videos Functions#############

@app.route('/localImage',methods=['POST'])
def encode_Upload_file():
    try:
        file= request.files['imagefile']
        key = int(request.form['secretKey'])
        text = request.form['secretData']
    except Exception  as e:
        return render_template('localImage.html',warning='Enter')

    if file and allowed_file_Videos(file.filename) and text and key:
        save_path_video=app.config['UPLOAD_FOLDER']+file.filename
        # Save the file to the specified upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        filename = os.path.splitext(file.filename)[0] + '.png'
        save_video_image = DOWNLOAD_DIRECTORY + filename
        encode_text(save_path_video,text,save_video_image,key)
        return render_template('localImage.html', encodeVideo=filename)

    if file and allowed_file(file.filename) and text and key:
        save_path_image = save_directory + file.filename
        # Save the image to the specified directory
        file.save(os.path.join(save_directory, file.filename))
        if file and allowed_file_accept_image(file.filename):
            encode_image(save_path_image, text, file.filename,key)
            return render_template('localImage.html', encodeImage=file.filename)
        filename = os.path.splitext(file.filename)[0] + '.png'
        encode_image(save_path_image,text,filename,key)
        return render_template('localImage.html',encodeImage= filename)
    return render_template('localImage.html',warning='Enter')

################ Download Image From Download Folder ##################

@app.route('/get-files/<path:path>',methods = ['GET','POST'])
def get_files(path):

    """Download a file."""
    try:
        return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)
    except FileNotFoundError:
        return render_template('404.html'),404


############################# Decode Images and Videos Function ##################

@app.route('/decodeuploadfile',methods = ['GET','POST'])
def decode_Upload_file():
    try:
        file = request.files['imagefile']
        value = request.form['decodeprocess']
        key = int(request.form['secretKey'])
    except Exception as e:
        return render_template('localDecode.html',warning="Enter")
    result=''
    if value=='Image Decoding' and file and key:
        save_path_image = "./static/images/decodeImages/" + file.filename
        file.save(os.path.join('./static/images/decodeImages/', file.filename))
        result = decode_image(save_path_image,key)
    elif value=='Video Decoding' and file and key:
        save_path_image = "./static/images/decodeImages/" + file.filename
        file.save(os.path.join('./static/images/decodeImages/', file.filename))
        result = decode_text(save_path_image,key)
    else:
        return render_template('localImage.html',warning='Enter')

    return render_template('localDecode.html',result_vlaue=result)




################ Decode Image & Video Page ##################
@app.route("/localDecode")
def localVideo():
    return render_template('localDecode.html')




# Create Custom Error Page
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Run the code 
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)



