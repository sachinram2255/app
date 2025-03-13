function uploadFile() {
    let fileInput = document.getElementById("fileInput");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select a file!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            document.getElementById("textOutput").value = data.text;
        }
    })
    .catch(error => {
        console.error("Upload Error:", error);
    });
}

function convertToSpeech() {
    let text = document.getElementById("textOutput").value;

    if (!text) {
        alert("No text available for conversion!");
        return;
    }

    fetch("/convert_to_speech", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            document.getElementById("audioPlayer").src = data.audio_url;
        }
    })
    .catch(error => {
        console.error("Speech Conversion Error:", error);
    });
}
