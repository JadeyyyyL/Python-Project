from flask import Flask, render_template, request, jsonify, session, redirect
import nlp_mood
import spotify
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
            normalized_input = nlp_mood.normalize_repeated_characters(user_input)
            checked_input = nlp_mood.spellcheck(normalized_input)
            analyzed_input = nlp_mood.sentiment_analysis(checked_input)
            categorized_emotions = nlp_mood.categorize_mood(analyzed_input)
            if categorized_emotions:
                playlist = "Today's Top Hits"
                playlist_id = spotify.search_playlist_id(playlist)
                top_hits_tracks = spotify.get_playlist_tracks(playlist_id)
                for track in top_hits_tracks:
                    track['audio_features'] = spotify.search_audio_features(track['id'])
                categorized_songs = spotify.categorize_songs_by_emotion(top_hits_tracks)
                selected_songs = categorized_songs.get(categorized_emotions, [])
                if selected_songs:
                    random_song = random.choice(selected_songs)
                    return render_template("results.html", random_song=random_song)
                else:
                    return render_template("error_page.html", error_message=f'No songs found for the {categorized_emotions} emotion.'), 404
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
