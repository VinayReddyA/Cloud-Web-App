from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('display.html')

    if request.method == "POST":
        filename = request.form['tlf']
        try:
            with open(filename, "r") as file:
                total_time = 0
                for line in file:
                    if line.find("Time Log:") == 0:
                        continue
                    if 'am' not in line.lower() and 'pm' not in line.lower():
                        continue
                    start_time = datetime.strptime(line.split('-')[0].strip()[-7:].lower().strip(), '%I:%M%p')
                    end_time = datetime.strptime(line.split('-')[1][1:8].lower().strip(), '%I:%M%p')
                    time_spend = end_time - start_time
                    total_time = total_time + (time_spend.seconds / 60)
               
                return render_template('display.html',
                                    filename = filename.split('.')[0],
                                    result='{:02d} hours {:02d} minutes'.format(*divmod(int(total_time), 60)))
        except FileNotFoundError:
            return render_template('display.html', file_not_found = "Sorry, Select file.")

if __name__ == '__main__':
    app.run(debug=True)
