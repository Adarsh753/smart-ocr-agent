async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const statusElement = document.getElementById("status");
    const resultElement = document.getElementById("result");
    const file = fileInput.files[0];

    // Clear previous results
    statusElement.innerText = "";
    resultElement.innerText = "";

    if (!file) {
        statusElement.innerText = "❌ Please select a file.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        statusElement.innerText = "📤 Uploading file...";

        // Add a timeout for upload (10 seconds)
        const uploadController = new AbortController();
        const uploadTimeout = setTimeout(() => {
            uploadController.abort();
        }, 100000);

        const response = await fetch("http://127.0.0.1:8000/api/v1/upload/", {
            method: "POST",
            body: formData,
            signal: uploadController.signal
        });

        clearTimeout(uploadTimeout);

        if (!response.ok) {
            const errorData = await response.json();
            statusElement.innerText = `❌ Upload failed: ${errorData.error || "Unknown error"}`;
            return;
        }

        const data = await response.json();
        const taskId = data.task_id;
        statusElement.innerText = "✅ File uploaded! Processing OCR...";

        // Wait a few seconds to simulate processing time
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Fetch OCR result with timeout (10 seconds)
        const resultController = new AbortController();
        const resultTimeout = setTimeout(() => {
            resultController.abort();
        }, 10000);

        const resultResponse = await fetch(`http://127.0.0.1:8000/api/v1/result/${taskId}/`, {
            signal: resultController.signal
        });

        clearTimeout(resultTimeout);

        if (!resultResponse.ok) {
            const errorData = await resultResponse.json();
            statusElement.innerText = `❌ Failed to fetch OCR result: ${errorData.error || "Unknown error"}`;
            return;
        }

        const resultData = await resultResponse.json();
        resultElement.innerText = resultData.ocr_text;
        statusElement.innerText = "✅ OCR processing completed!";
    } catch (error) {
        console.error(error);
        if (error.name === "AbortError") {
            statusElement.innerText = "⏱️ Request timed out. Please try again.";
        } else {
            statusElement.innerText = "❌ An error occurred while uploading or fetching the result.";
        }
    }
}
