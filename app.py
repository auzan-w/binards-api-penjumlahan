# Import library for Pandas
import pandas as pd

# Import library for Flask
from flask import Flask, jsonify
from flask import request

import sqlite3

app = Flask(__name__)

#Fungsi penjumlahan
def jumlah(input1,input2):
  return input1 + input2

#API Route process penjumlahan dari form input
@app.route('/add-processing', methods=['POST'])
def text_processing():

    # Get number file
    num1 = request.form.get('number1')
    num2 = request.form.get('number2')
    
    # Calculation Process
    result = jumlah(int(num1),int(num2))

    database_txt(num1, num2, result)
    # Define API response
    json_response = {
            'status_code': 200,
            'description': "sudah dilakukan penjumlahan dan ditambahkan ke database",
            'result': result,
            'number1': int(num1),
            'number2': int(num2),
        }

    response_data = jsonify(json_response)
    
    
    return response_data

# Define endpoint for "upload file CSV"
@app.route('/add-processing-file', methods=['POST'])
def text_processing_file():

    # Upladed file
    file = request.files['file']

    # Import file csv ke Pandas
    df = pd.read_csv(file,header=0)

    df['result'] = df.apply(lambda row : jumlah(row['input1'],row['input2']), axis = 1)
    
    # Get result from file in "List" format
    result = df.result.to_list()

    # Define API response
    json_response = {
        'status_code': 200,
        'description': "sudah dilakukan penjumlahan dan ditambahkan ke database",
        'data': result,
    }
    response_data = jsonify(json_response)
    
    database_csv(df)
    
    return response_data

def database_txt(kolom1, kolom2, kolom3):
    conn = sqlite3.connect("penjumlahan.db")
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS hasil_jumlah_input (input1, input2, result)""")
    cursor.execute("""INSERT INTO hasil_jumlah_input (input1, input2, result) VALUES (?,?,?)""",(kolom1, kolom2, kolom3))
    
    conn.commit()
    cursor.close()
    conn.close()
    
def database_csv(data):
    conn = sqlite3.connect("penjumlahan.db")
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS hasil_jumlah_input (input1, input2, result)""")
    
    data.to_sql('hasil_jumlah_input', conn, if_exists = 'append', index = False)
    

if __name__ == '__main__':
   app.run(debug=True)