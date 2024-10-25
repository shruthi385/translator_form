from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# LibreTranslate API endpoint
TRANSLATE_API_URL = 'https://libretranslate.com/translate'

@app.route('/')
def form_page():
    return render_template('form.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text')
    target_language = data.get('language')

    # Request translation from LibreTranslate
    payload = {
        'q': text,
        'source': 'en',
        'target': target_language,
        'format': 'text'
    }
    
    try:
        response = requests.post(TRANSLATE_API_URL, data=payload)
        response.raise_for_status()  # Check for HTTP errors

        result = response.json()
        translated_text = result['translatedText']
    except Exception as e:
        print(f"Error during translation: {e}")  # Log error
        translated_text = text  # Return original text if translation fails

    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
