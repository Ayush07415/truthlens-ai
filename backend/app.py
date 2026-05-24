from flask import (
    Flask,
    request,
    jsonify
)

from flask_cors import CORS

from src.predict import predict_news
from src.scraper import extract_text_from_url

# ====================================
# 🔥 FLASK APP
# ====================================

app = Flask(__name__)

# ====================================
# 🔥 ENABLE CORS
# ====================================

CORS(
    app,

    resources={
        r"/*": {
            "origins": "*"
        }
    }
)

# ====================================
# 🔥 HOME ROUTE
# ====================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "status": "online",

        "message":
            "TruthLens API Running"
    })

# ====================================
# 🔥 MAIN PREDICTION API
# ====================================

@app.route(
    "/api/predict",
    methods=["POST"]
)

def api_predict():

    try:

        # ====================================
        # GET REQUEST DATA
        # ====================================

        data = request.get_json()

        if not data:

            return jsonify({

                "error":
                    "No JSON received"
            }), 400

        # ====================================
        # INPUTS
        # ====================================

        text = data.get("text")

        url = data.get("url")

        # ====================================
        # 🔥 EXTENSION FAST MODE
        # ====================================

        extension_mode = data.get(
            "extension_mode",
            False
        )

        # ====================================
        # URL SCRAPING
        # ====================================

        if url:

            try:

                scraped_text =extract_text_from_url(
                        url
                    )

                if (
                    scraped_text and
                    len(scraped_text) > 100
                ):

                    text = scraped_text

            except Exception:

                pass

        # ====================================
        # EMPTY CONTENT
        # ====================================

        if not text:

            return jsonify({

                "error":
                    "No valid content"
            }), 400

        # ====================================
        # 🔥 FAST EXTENSION TEXT LIMIT
        # ====================================

        if extension_mode:

            text = text[:800]

        # ====================================
        # 🔥 MAIN PREDICTION
        # ====================================

        result = predict_news(

            text,

            extension_mode
        )

        return jsonify(result)

    # ====================================
    # 🔥 GLOBAL ERROR
    # ====================================

    except Exception as e:

        return jsonify({

            "error":
                str(e)
        }), 500

# ====================================
# 🔥 RUN SERVER
# ====================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False,

        use_reloader=False,

        threaded=True
    )