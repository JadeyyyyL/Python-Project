from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Handling form submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        if request.method == "POST":
            # Get user input from the form
            user_input = request.form['user_input']
            # Redirect to the next page with the user input as a URL parameter
            return render_template("results.html", user_input = user_input)

    except Exception as e:
        return render_template("error_page.html", error_message=str(e))

    return render_template("index.html")

# Next page
@app.route('/results/<user_input>')
def generate_song(user_input):
    recommendation = recommended_song()
    return render_template("results.html", user_input=user_input, recommendation = recommendation)


#Error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_page.html", error_message="Page not found."), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error_page.html", error_message="Internal server error."), 500

if __name__ == '__main__':
    app.run(debug=True)
