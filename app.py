from flask import Flask, jsonify, request
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Flask app and Sentiment Analyzer
app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

# List of event-related keywords
event_keywords = [
    "travel", "transport", "bus", "flight", "accommodation", "stay", "hotel", 
    "hostel", "lodging", "contact", "person", "reach", "point of contact"
]

def analyze_messages(messages):
    keyword_counts = {"issues": Counter(), "questions": Counter(), "satisfied": Counter()}

    for message in messages:
        sentiment_scores = analyzer.polarity_scores(message)
        compound_score = sentiment_scores["compound"]

        if compound_score >= 0.05:
            sentiment = "satisfied"
        elif compound_score <= -0.05:
            sentiment = "issues"
        else:
            sentiment = "questions" if "?" in message else "neutral"

        found_topics = set()
        for keyword in event_keywords:
            if keyword in message.lower():
                found_topics.add(keyword)

        for topic in found_topics:
            if sentiment in keyword_counts:
                keyword_counts[sentiment][topic] += 1

    sorted_results = {
        "issues": [(k, v) for k, v in keyword_counts["issues"].most_common()],
        "questions": [(k, v) for k, v in keyword_counts["questions"].most_common()],
        "satisfied": [(k, v) for k, v in keyword_counts["satisfied"].most_common()],
    }

    return sorted_results


@app.route('/analyze', methods=['POST'])
def analyze_chats():
    try:
        # Example messages (you can replace this with data from your MongoDB or other source)
        data = request.get_json()  # Parse the JSON data
        print(data)

        messages_contents = [
            "Is transportation arranged for the event?",
            "Is there transportation?",
            "Looking forward to the stay at the hotel!",
            "I like the event!",
            "Who should we contact if there’s an issue?",
            "Transportation arrangements are terrible.",
            "Accommodation will be great, right?",
            "Does the venue have Wi-Fi?",
            "Not happy with the hotel arrangements.",
        ]

        # Analyze messages using the defined function
        sorted_results = analyze_messages(messages_contents)

        # Print results to console
        print(sorted_results)

        # Return results as JSON response
        return jsonify({"status": 200, "data": sorted_results})

    except Exception as e:
        return jsonify({"status": 500, "error": "An error occurred while analyzing chats.", "details": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
