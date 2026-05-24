// ======================================
// 🔥 CREATE FLOATING RESULT BOX
// ======================================

function createFloatingBox() {

    let existing =
        document.getElementById(
            "fake-news-box"
        );

    if(existing){

        existing.remove();
    }

    let box =
        document.createElement("div");

    box.id = "fake-news-box";

    box.style.position = "fixed";
    box.style.bottom = "20px";
    box.style.right = "20px";
    box.style.width = "320px";

    box.style.background =
        "rgba(15,15,25,0.95)";

    box.style.backdropFilter =
        "blur(12px)";

    box.style.color = "white";

    box.style.padding = "18px";

    box.style.borderRadius = "16px";

    box.style.zIndex = "999999999";

    box.style.boxShadow =
        "0 10px 35px rgba(0,0,0,0.4)";

    box.style.fontFamily =
        "Arial, sans-serif";

    box.style.transition =
        "all 0.4s ease";

    box.style.border =
        "1px solid rgba(255,255,255,0.08)";

    box.innerHTML = `

        <div
            id="fake-news-loading"
            style="
                display:flex;
                align-items:center;
                gap:10px;
                font-size:15px;
            "
        >

            <div
                style="
                    width:14px;
                    height:14px;
                    border-radius:50%;
                    border:3px solid #00d2ff;
                    border-top-color:transparent;
                    animation:spin 1s linear infinite;
                "
            ></div>

            <span>
                Analyzing content...
            </span>

        </div>

        <style>

            @keyframes spin {

                from{
                    transform:rotate(0deg);
                }

                to{
                    transform:rotate(360deg);
                }
            }

        </style>
    `;

    document.body.appendChild(box);

    return box;
}

// ======================================
// 🔥 FAST SOCIAL MEDIA EXTRACTION
// ======================================

function getSocialMediaText() {

    // ==================================
    // INSTAGRAM
    // ==================================

    let article =
        document.querySelector(
            "article"
        );

    if(article){

        return article.innerText
            .slice(0, 2000);
    }

    // ==================================
    // FACEBOOK
    // ==================================

    let fbPost =
        document.querySelector(
            '[data-ad-preview="message"]'
        );

    if(fbPost){

        return fbPost.innerText
            .slice(0, 2000);
    }

    // ==================================
    // TWITTER/X
    // ==================================

    let tweet =
        document.querySelector(
            '[data-testid="tweetText"]'
        );

    if(tweet){

        return tweet.innerText
            .slice(0, 2000);
    }

    // ==================================
    // FALLBACK
    // ==================================

    return (
    document.querySelector("article")
    ?.innerText ||

    document.body.innerText
)
        .slice(0, 800);
}

// ======================================
// 🔥 CLEAN TEXT
// ======================================

function cleanText(text){

    return text

        .replace(/@\w+/g, "")
        .replace(/#\w+/g, "")
        .replace(/[^\w\s]/g, " ")
        .replace(/\s+/g, " ")

        .trim();
}

// ======================================
// 🔥 SAFE HIGHLIGHT
// ======================================

function highlightFakeWords(words){

    if(
        !words ||
        words.length === 0
    ){

        return;
    }

    const walker =
        document.createTreeWalker(

            document.body,

            NodeFilter.SHOW_TEXT,

            null,

            false
        );

    let nodes = [];

    while(walker.nextNode()){

        nodes.push(
            walker.currentNode
        );
    }

    nodes.forEach(node => {

        let text =
            node.nodeValue;

        words.forEach(word => {

            let regex =
                new RegExp(
                    `\\b(${word})\\b`,
                    "gi"
                );

            if(regex.test(text)){

                let span =
                    document.createElement(
                        "span"
                    );

                span.innerHTML =
                    text.replace(

                        regex,

                        `<mark style="
                            background:#ff3b30;
                            color:white;
                            padding:2px 4px;
                            border-radius:4px;
                        ">$1</mark>`
                    );

                node.parentNode.replaceChild(
                    span,
                    node
                );
            }
        });
    });
}

// ======================================
// 🔥 ANALYZE PAGE
// ======================================

async function analyzePage() {

    const box =
        createFloatingBox();

    try {

        // ==================================
        // FAST TEXT EXTRACTION
        // ==================================

        let text =
            getSocialMediaText();

        text = cleanText(text);

        // ==================================
        // EMPTY CHECK
        // ==================================

        if(
            !text ||
            text.length < 30
        ){

            box.innerHTML = `

                <div style="
                    color:#ff7675;
                    font-size:15px;
                ">
                    ⚠️ No readable content found
                </div>
            `;

            return;
        }

        // ==================================
        // SEND TO BACKEND
        // ==================================

        const response =
            await fetch(

            "https://truthlens-ai-msqz.onrender.com/api/predict",

            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    text: text,

                    extension_mode: true
                })
            }
        );

        const data =
            await response.json();

        console.log(
            "Extension Result:",
            data
        );

        // ==================================
        // HIGHLIGHT WORDS
        // ==================================

        highlightFakeWords(
            data.suspicious_words
        );

        // ==================================
        // VERDICT COLOR
        // ==================================

        let verdictColor =
            "#2ecc71";

        let verdictIcon =
            "✅";

        if(
            data.prediction === "FAKE"
        ){

            verdictColor =
                "#ff3b30";

            verdictIcon =
                "❌";
        }

        // ==================================
        // UPDATE UI
        // ==================================

        box.innerHTML = `

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin-bottom:12px;
            ">

                <div style="
                    font-size:20px;
                    font-weight:bold;
                    color:${verdictColor};
                ">

                    ${verdictIcon}
                    ${data.prediction}

                </div>

                <div style="
                    font-size:12px;
                    opacity:0.7;
                ">

                    AI Scan

                </div>

            </div>

            <div style="
                margin-bottom:10px;
                font-size:14px;
            ">

                Confidence:
                <b>${data.confidence}%</b>

            </div>

            <div style="
                margin-bottom:10px;
                font-size:14px;
            ">

                Credibility:
                <b>
                    ${data.credibility_score}%
                </b>

            </div>

            <div style="
                margin-bottom:10px;
                font-size:13px;
                color:#ddd;
            ">

                ${data.level}

            </div>

            <div style="
                width:100%;
                height:8px;
                border-radius:20px;
                background:#2d3436;
                overflow:hidden;
                margin-top:12px;
            ">

                <div style="
                    width:${data.confidence}%;
                    height:100%;
                    background:${verdictColor};
                    transition:1s;
                "></div>

            </div>
        `;

        // ==================================
        // AUTO REMOVE
        // ==================================

        setTimeout(() => {

            box.style.opacity = "0";

            setTimeout(() => {

                box.remove();

            }, 400);

        }, 7000);

    }

    // ======================================
    // ERROR
    // ======================================

    catch(err){

        console.error(err);

        box.innerHTML = `

            <div style="
                color:#ff7675;
                font-size:15px;
            ">

                ❌ Backend Connection Failed

            </div>
        `;
    }
}

// ======================================
// 🔥 MESSAGE LISTENER
// ======================================

chrome.runtime.onMessage.addListener(

    (request, sender, sendResponse) => {

        if(
            request.action === "analyze"
        ){

            analyzePage();

            sendResponse({
                status: "ok"
            });

            return true;
        }
    }
);