document.getElementById("churnForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    let formData = new FormData(this);
    let data = {};
    formData.forEach((value, key) => data[key] = value);

    try {
        let response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error("Server error: " + response.statusText);
        }

        let result = await response.json();

        // Color logic: Red if churn, green if no churn
        let predictionText = result.prediction === 1
        ? `<span style="color:red; font-weight:bold;"> Churn</span>`
        : `<span style="color:green; font-weight:bold;">No Churn</span>`



        // you can use this color logic as well inside innerHTML
        // <p><b>Prediction:</b> 
        //         <span style="color:${result.prediction === 1 ? 'red' : 'green'}; font-weight:bold;">
        //             ${result.prediction === 1 ? "Churn" : "No Churn"}
        //         </span>
        //     </p>


        document.getElementById("result").innerHTML = `
            <p><b>Prediction:</b> ${predictionText}</p>
            <p><b>Churn Probability:</b> ${result.probability}%</p>
            <p><b>Suggested Discount:</b> ${result.suggested_discount}%</p>
        `;
    } catch (err) {
        console.error("Error:", err);
        document.getElementById("result").innerHTML = `
            <p style="color:red;">❌ Something went wrong: ${err.message}</p>
        `;
    }
});
