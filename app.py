from flask import Flask, render_template, request, jsonify, session, redirect
from nlp_mood import categorize_mood
from spotify import categorize_songs_by_emotion, get_top_hits_features
import random

app = Flask(__name__, template_folder = "template")

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

    #recommendation = recommended_song()
    #spotify_preview = "https://open.spotify.com/embed/track/6rqhFgbbKwnb9MLmUQDhG6"
    #related_artists = [
    #     {"name": "Artist 1", "image": "artist1.jpg", "link": "https://example.com/artist1"},
    #     {"name": "Artist 2", "image": "artist2.jpg", "link": "https://example.com/artist2"},
    #     {"name": "Artist 3", "image": "artist3.jpg", "link": "https://example.com/artist3"},
    #     {"name": "Artist 4", "image": "artist4.jpg", "link": "https://example.com/artist4"},
    #     {"name": "Artist 5", "image": "artist5.jpg", "link": "https://example.com/artist5"}
    # ]
    #return render_template("results.html", user_input=user_input) #recommendation = recommendation, spotify_preview = spotify_preview, related_artists = related_artists


#Error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_page.html", error_message="Page not found."), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error_page.html", error_message="Internal server error."), 500

if __name__ == '__main__':
    app.run(debug=True)
