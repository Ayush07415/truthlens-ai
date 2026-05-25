// ======================================
// 🔥 CLEAR OLD RESULTS
// ======================================

function clearOldResults() {

    // ==================================
    // VERDICT RESET
    // ==================================

    document.getElementById(
        "verdictLabel"
    ).innerText = "Scanning...";

    document.getElementById(
        "verdictSublabel"
    ).innerText =
        "Analyzing content...";

    // ==================================
    // RESET VERDICT ICON
    // ==================================

    const verdictIcon =
        document.getElementById(
            "verdictIcon"
        );

    if(verdictIcon){

        verdictIcon.innerHTML = "⏳";
    }

    // ==================================
    // RESET BARS
    // ==================================

    const bars = [

        "confidenceFill",
        "credibilityFill",
        "factFill",
        "clickbaitFill",
        "biasFill",
        "sentimentFill",
        "readFill"

    ];

    bars.forEach(id => {

        const el =
            document.getElementById(id);

        if(el){

            el.style.width = "0%";
        }
    });

    // ==================================
    // RESET VALUES
    // ==================================

    const fields = [

        "confidenceVal",
        "credibilityVal",
        "factVal",
        "clickbaitVal",
        "biasVal",
        "sentimentVal",
        "sourceName",
        "sourceDomain",
        "sourceCategory",
        "wordCount",
        "sentenceCount",
        "uniqueWords",
        "avgSentLen",
        "readVal"

    ];

    fields.forEach(id => {

        const el =
            document.getElementById(id);

        if(el){

            el.innerText = "--";
        }
    });

    // ==================================
    // CLEAR FLAGS
    // ==================================

    const flags =
        document.getElementById(
            "flagsList"
        );

    if(flags){

        flags.innerHTML = "";
    }

    // ==================================
    // CLEAR KEYWORDS
    // ==================================

    const keywords =
        document.getElementById(
            "keywordsList"
        );

    if(keywords){

        keywords.innerHTML = "";
    }

    // ==================================
    // CLEAR EXPLANATIONS
    // ==================================

    const explanations =
        document.getElementById(
            "explanationList"
        );

    if(explanations){

        explanations.innerHTML =
            "Generating AI explanation...";
    }
}

// ======================================
// 🔥 MAIN ANALYSIS FUNCTION
// ======================================

async function analyzeNews() {

    // ==================================
    // PREVENT MULTIPLE SCANS
    // ==================================

    if(window.isScanning){
        return;
    }

    window.isScanning = true;

    // ==================================
    // CLEAR OLD RESULTS
    // ==================================

    clearOldResults();

    // ==================================
    // DISABLE BUTTON
    // ==================================

    const scanBtn =
        document.getElementById(
            "scanBtn"
        );

    if(scanBtn){

        scanBtn.disabled = true;

        scanBtn.style.opacity =
            "0.6";

        const btnText =
    scanBtn.querySelector(
        ".scan-btn-text"
    );

if(btnText){

    btnText.innerText =
        "Scanning...";
}
    }

    try {

        // ==================================
        // SHOW RESULTS SECTION
        // ==================================

        const resultsGrid =
            document.getElementById(
                "resultsGrid"
            );

        if(resultsGrid){

            resultsGrid.style.display =
                "grid";

            resultsGrid.style.visibility =
                "visible";

            resultsGrid.style.opacity =
                "1";
        }

        // ==================================
        // GET INPUTS
        // ==================================

        let payload = {};

        const textInput =
    document.getElementById(
        "newsInput"
    );

const urlInput =
    document.getElementById(
        "urlInput"
    );

const textValue =
    textInput.value.trim();

const urlValue =
    urlInput.value.trim();

        // ==================================
        // TEXT MODE
        // ==================================

        if(textValue.trim() !== ""){

           payload = {
    text: textValue,
    url: null,
    timestamp: Date.now()
};
        }

        // ==================================
        // URL MODE
        // ==================================

        else if(urlValue.trim() !== ""){

            payload = {
    url: urlValue,
    text: null,
    timestamp: Date.now()
};
        }

        // ==================================
        // EMPTY INPUT
        // ==================================

        else{

            alert(
                "Enter text or URL"
            );

            window.isScanning = false;

            if(scanBtn){

                scanBtn.disabled = false;

                scanBtn.style.opacity =
                    "1";

                const btnText =
    scanBtn.querySelector(
        ".scan-btn-text"
    );

if(btnText){

    btnText.innerText =
        "Analyze Content";
}
            }

            return;
        }

        console.log(
            "PAYLOAD:",
            payload
        );

        // ==================================
        // CONNECT BACKEND
        // ==================================

        const response = await fetch(

            "http://127.0.0.1:5000/api/predict",

            {
                method: "POST",
                cache: "no-cache",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    payload
                )
            }
        );

        // ==================================
        // HANDLE SERVER ERROR
        // ==================================

        if(!response.ok){

            throw new Error(
                "Server Error"
            );
        }

        const data =
            await response.json();

        console.log(
            "Backend:",
            data
        );

        // ==================================
        // 🔥 VERDICT
        // ==================================

        document.getElementById(
            "verdictLabel"
        ).innerText =
            data.prediction;

        document.getElementById(
            "verdictSublabel"
        ).innerText =
            data.level;

        // ==================================
        // 🔥 TIMESTAMP
        // ==================================

        const time =
            new Date()
            .toLocaleTimeString();

        document.getElementById(
            "scanTimestamp"
        ).innerText =
            "Scanned at " + time;

        // ==================================
        // 🔥 DYNAMIC VERDICT ICON
        // ==================================

        const verdictIcon =
            document.getElementById(
                "verdictIcon"
            );

        if(verdictIcon){

            // REAL

            if(
                data.prediction === "REAL" &&
                data.confidence < 40
            ){

                verdictIcon.innerHTML =
                    "🟢";
            }

            // STRONG REAL

            else if(
                data.prediction === "REAL"
            ){

                verdictIcon.innerHTML =
                    "✅";
            }

            // MODERATE FAKE

            else if(
                data.prediction === "FAKE" &&
                data.confidence < 80
            ){

                verdictIcon.innerHTML =
                    "⚠️";
            }

            // STRONG FAKE

            else{

                verdictIcon.innerHTML =
                    "❌";
            }
        }

        // ==================================
        // 🔥 CONFIDENCE
        // ==================================

        document.getElementById(
            "confidenceVal"
        ).innerText =
            data.confidence + "%";

        document.getElementById(
            "confidenceFill"
        ).style.width =
            data.confidence + "%";

        // ==================================
        // 🔥 CREDIBILITY
        // ==================================

        document.getElementById(
            "credibilityVal"
        ).innerText =
            data.credibility_score + "%";

        document.getElementById(
            "credibilityFill"
        ).style.width =
            data.credibility_score + "%";

        // ==================================
        // 🔥 CLAIM ANALYSIS
        // ==================================

        document.getElementById(
            "factVal"
        ).innerText =
            data.factual_accuracy + "%";

        document.getElementById(
            "factFill"
        ).style.width =
            data.factual_accuracy + "%";

        document.getElementById(
            "clickbaitVal"
        ).innerText =
            data.clickbait_score + "%";

        document.getElementById(
            "clickbaitFill"
        ).style.width =
            data.clickbait_score + "%";

        // ==================================
        // 🔥 SOURCE ANALYSIS
        // ==================================

        document.getElementById(
            "biasVal"
        ).innerText =
            data.bias_score + "%";

        document.getElementById(
            "biasFill"
        ).style.width =
            data.bias_score + "%";

        document.getElementById(
            "sentimentVal"
        ).innerText =
            data.emotion_score + "%";

        document.getElementById(
            "sentimentFill"
        ).style.width =
            data.emotion_score + "%";

        document.getElementById(
            "sourceName"
        ).innerText =
            data.source_name;

        document.getElementById(
            "sourceDomain"
        ).innerText =
            data.domain;

        document.getElementById(
            "sourceCategory"
        ).innerText =
            data.category;

        // ==================================
        // 🔥 LINGUISTIC PATTERNS
        // ==================================

        document.getElementById(
            "wordCount"
        ).innerText =
            data.word_count;

        document.getElementById(
            "sentenceCount"
        ).innerText =
            data.sentence_count;

        document.getElementById(
            "uniqueWords"
        ).innerText =
            data.unique_words;

        document.getElementById(
            "avgSentLen"
        ).innerText =
            data.avg_sentence;

        // ==================================
        // 🔥 READABILITY INDEX
        // ==================================

        document.getElementById(
            "readVal"
        ).innerText =
            data.readability;

        document.getElementById(
            "readFill"
        ).style.width =
            data.readability + "%";

        // ==================================
        // 🔥 SUSPICIOUS WORDS
        // ==================================

        const flagsList =
            document.getElementById(
                "flagsList"
            );

        flagsList.innerHTML = "";

        if(

            data.suspicious_words &&
            data.suspicious_words.length > 0

        ){

            data.suspicious_words.forEach(
                word => {

                const div =
                    document.createElement(
                        "div"
                    );

                div.className =
                    "flag-item";

                div.innerText =
                    word;

                flagsList.appendChild(
                    div
                );
            });
        }

        else{

            flagsList.innerHTML =
                "<div>No suspicious words</div>";
        }

        // ==================================
        // 🔥 KEYWORDS
        // ==================================

        const keywordsList =
            document.getElementById(
                "keywordsList"
            );

        keywordsList.innerHTML = "";

        if(

            data.keywords &&
            data.keywords.length > 0

        ){

            data.keywords.forEach(
                word => {

                const span =
                    document.createElement(
                        "span"
                    );

                span.className =
                    "keyword";

                span.innerText =
                    word;

                keywordsList.appendChild(
                    span
                );
            });
        }

        // ==================================
        // 🔥 AI EXPLANATION
        // ==================================

        const explanationBox =
            document.getElementById(
                "explanationList"
            );

        if(explanationBox){

            explanationBox.innerHTML =
                "";

            if(
                data.explanations &&
                data.explanations.length > 0
            ){

                data.explanations.forEach(
                    reason => {

                    const div =
                        document.createElement(
                            "div"
                        );

                    div.className =
                        "flag-item";

                    div.innerText =
                        "• " + reason;

                    explanationBox
                    .appendChild(div);
                });

            }else{

                explanationBox.innerHTML =
                    "No AI explanation available";
            }
        }

        // ==================================
        // 🔥 NEWS VERIFICATION
        // ==================================

        console.log(
            "NEWS CHECK:",
            data.news_verification
        );

    }

    // ==================================
    // 🔥 ERROR HANDLING
    // ==================================

    catch(err){

        console.log(err);

        alert(
            "Backend connection failed"
        );
    }
    // ==================================
// RESET BUTTON AFTER RESULT
// ==================================

window.isScanning = false;

if(scanBtn){

    scanBtn.disabled = false;

    scanBtn.style.opacity = "1";

    const btnText =
        scanBtn.querySelector(
            ".scan-btn-text"
        );

    if(btnText){

        btnText.innerText =
            "Analyze Page";
    }
}
}
    "Analyze Content";
    
POST 