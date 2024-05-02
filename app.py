from flask import Flask, render_template, request, jsonify, session, redirect
from nlp_mood import categorize_mood
from spotify import categorize_songs_by_emotion, get_top_hits_features
import random

app = Flask(__name__, template_folder = "template")
app.secret_key = 'SpoTiFy2772'

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Handling form submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        if request.method == "POST":
            user_input = request.form['user_input']
            session['user_input'] = user_input
            return redirect('/results')

    except Exception as e:
        return render_template("error_page.html", error_message=str(e))

    return render_template("index.html")

# Next page
@app.route('/results')
def generate_song():
    try:
        user_input = session.get('user_input')
        if user_input:
            categorized_emotions = categorize_mood(user_input)
            primary_emotion = categorized_emotions[0] if categorized_emotions else None
            if primary_emotion:
                top_hits_tracks = get_top_hits_features()
                categorized_songs = categorize_songs_by_emotion(top_hits_tracks)
                selected_songs = categorized_songs.get(primary_emotion, [])
                if selected_songs:
                    random_song = random.choice(selected_songs)
                    return render_template("results.html", random_song=random_song)
                else:
                    return render_template("error_page.html", error_message=f'No songs found for the {primary_emotion} emotion.'), 404
            else:
                return render_template("error_page.html", error_message='Unable to determine user emotion.'), 400
        else:
            return render_template("error_page.html", error_message='No user input provided.')

    except Exception as e:
        return render_template("error_page.html", error_message=str(e)), 500


#Error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_page.html", error_message="Page not found."), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error_page.html", error_message="Internal server error."), 500

if __name__ == '__main__':
    app.run(debug=True)
