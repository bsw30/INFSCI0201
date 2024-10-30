from flask import Flask, request, render_template
import segno
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    if request.method == 'POST': # Get the user input from the form
        data = request.form['data']
        qr = segno.make_qr(data) # Create the QRCode object
        buff = io.BytesIO() # Store the QR code in an in-memory binary buffer as SVG
        qr.save(buff, kind='svg', scale=3, dark='darkblue', nl=False)
        buff.seek(0)

        img_base64 = base64.b64encode(buff.getvalue()).decode('utf-8') # Encode the binary image blob to a base64 string
        img_data_uri = f"data:image/svg+xml;base64,{img_base64}"

        return render_template('qr_code.html', img_data_uri=img_data_uri) # Pass the data URI to the template


if __name__ == '__main__':
    app.run(debug=True)