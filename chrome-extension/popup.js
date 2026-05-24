document
.getElementById("check")
.addEventListener(

    "click",

    async () => {

    const result =
        document.getElementById(
            "result"
        );

    result.innerHTML =
        "🔍 Starting AI Scan...";

    try {

        // =================================
        // GET ACTIVE TAB
        // =================================

        let [tab] =
            await chrome.tabs.query({

                active: true,

                currentWindow: true
            });

        // =================================
        // INJECT CONTENT SCRIPT
        // =================================

        await chrome.scripting.executeScript({

            target: {
                tabId: tab.id
            },

            files: ["content.js"]
        });

        // =================================
        // RUN ANALYSIS
        // =================================

        chrome.tabs.sendMessage(

            tab.id,

            {
                action: "analyze"
            },

            (response) => {

                // =================================
                // ERROR
                // =================================

                if(
                    chrome.runtime.lastError
                ){

                    console.log(
                        chrome.runtime.lastError
                    );

                    result.innerHTML =

                        "❌ Injection Failed";

                    return;
                }

                // =================================
                // SUCCESS
                // =================================

                result.innerHTML =

                    "✅ AI Scan Started";
            }
        );

    }

    catch(err){

        console.log(err);

        result.innerHTML =

            "❌ Extension Error";
    }
});