from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def calculate_final_marks(ipe_marks, eamcet_marks):
    max_ipe_marks = 600
    max_eamcet_marks = 160
    ipe_percentage = 0.25
    eamcet_percentage = 0.75

    normalized_ipe_marks = (ipe_marks / max_ipe_marks) * 100
    normalized_eamcet_marks = (eamcet_marks / max_eamcet_marks) * 100
    
    final_marks = (normalized_ipe_marks * ipe_percentage) + (normalized_eamcet_marks * eamcet_percentage)
    return round(final_marks)

def read_csv_and_find_rank(filename, final_marks):
    df = pd.read_csv(filename)
    matching_row = df[df['TMarks'] == final_marks]
    return matching_row.iloc[0]['TRank']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ipe_marks = float(request.form['ipe_marks'])
        eamcet_marks = float(request.form['eamcet_marks'])

        final_marks = calculate_final_marks(ipe_marks, eamcet_marks)
        filename = 'data.csv'
        rank = read_csv_and_find_rank(filename, final_marks)

        return render_template('results.html', final_marks=final_marks, rank=rank)

    return render_template('index.html',port=5000)

if __name__ == '__main__':
    app.run(debug=True)
