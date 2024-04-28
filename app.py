from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Handling form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get user input from the form
    user_input = request.form['user_input']
    # Redirect to the next page with the user input as a URL parameter
    return redirect(url_for('results', user_input=user_input))

# Next page
@app.route('/results/<user_input>')
def generate_song(user_input):
    return f'<h1></h1>'

if __name__ == '__main__':
    app.run(debug=True)
