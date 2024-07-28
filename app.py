from flask import Flask, request, render_template, send_file, make_response
from PIL import Image
from rembg import remove
import io
import os

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def upload_files():
    #check request types
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file found'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            input_image = Image.open(file.stream) 
            output_image = remove(input_image)
            img_byte_arr = io.BytesIO() #initialize empty image buffer
            output_image.save(img_byte_arr, format='PNG') #save image data into ima_byte_arr
            img_byte_arr.seek(0)

            #define new file name
            original_filename = os.path.splitext(file.filename)[0] #omit the extension
            new_name = f"{original_filename}_processed_image.png"

            #prepare to make response
            response = make_response(send_file(img_byte_arr, mimetype='image/png'))
            response.headers['Content-Disposition'] = f'attachment; filename="{new_name}"'
            return response
    return render_template('upload.html')

if __name__ == '__main__':
    print("Server starting...")
    app.run(debug=True)

