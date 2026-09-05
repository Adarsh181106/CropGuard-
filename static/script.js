const fileInput = document.getElementById("fileInput");
const dropzone = document.getElementById("dropzone");
const dropzoneEmpty = document.getElementById("dropzoneEmpty");
const previewImage = document.getElementById("previewImage");
const scanButton = document.getElementById("scanButton");
const languageSelect = document.getElementById("languageSelect");

const loadingCard = document.getElementById("loadingCard");
const errorCard = document.getElementById("errorCard");
const errorText = document.getElementById("errorText");
const resultCard = document.getElementById("resultCard");

const diseaseName = document.getElementById("diseaseName");
const confidenceValue = document.getElementById("confidenceValue");
const severityBadge = document.getElementById("severityBadge");
const severityValue = document.getElementById("severityValue");
const treatmentText = document.getElementById("treatmentText");
const heatmapImage = document.getElementById("heatmapImage");

const retryButton = document.getElementById("retryButton");
const scanAgainButton = document.getElementById("scanAgainButton");

let selectedFile = null;

// --- Click dropzone to open file picker ---
dropzone.addEventListener("click", () => fileInput.click());

// --- Drag and drop support ---
dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.style.borderColor = "#8BC34A";
});
dropzone.addEventListener("dragleave", () => {
  dropzone.style.borderColor = "";
});
dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.style.borderColor = "";
  if (e.dataTransfer.files.length > 0) {
    handleFileSelected(e.dataTransfer.files[0]);
  }
});

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    handleFileSelected(fileInput.files[0]);
  }
});

function handleFileSelected(file) {
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.src = e.target.result;
    previewImage.hidden = false;
    dropzoneEmpty.hidden = true;
  };
  reader.readAsDataURL(file);
  scanButton.disabled = false;
}

// --- Submit to backend ---
scanButton.addEventListener("click", async () => {
  if (!selectedFile) return;

  showState("loading");

  const formData = new FormData();
  formData.append("image", selectedFile);
  formData.append("language", languageSelect.value);

  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Server returned an error");
    }

    const data = await response.json();
    displayResult(data);
  } catch (err) {
    errorText.textContent = "Could not analyze the photo. Check your connection and try again.";
    showState("error");
  }
});

function displayResult(data) {
  diseaseName.textContent = data.disease;
  confidenceValue.textContent = `${data.confidence}%`;
  severityValue.textContent = `${data.severity}%`;
  treatmentText.textContent = data.treatment;
  heatmapImage.src = data.heatmap;

  severityBadge.classList.remove("severity-low", "severity-medium", "severity-high");
  if (data.severity < 25) {
    severityBadge.classList.add("severity-low");
  } else if (data.severity < 60) {
    severityBadge.classList.add("severity-medium");
  } else {
    severityBadge.classList.add("severity-high");
  }

  showState("result");
}

retryButton.addEventListener("click", () => showState("upload"));
scanAgainButton.addEventListener("click", resetToUpload);

function resetToUpload() {
  selectedFile = null;
  fileInput.value = "";
  previewImage.hidden = true;
  dropzoneEmpty.hidden = false;
  scanButton.hidden = false;
  scanButton.disabled = true;
  showState("upload");
}

// The upload card (with the photo preview) stays visible in every state now,
// so the left column never goes empty after scanning.
function showState(state) {
  loadingCard.hidden = state !== "loading";
  errorCard.hidden = state !== "error";
  resultCard.hidden = state !== "result";

  // Only show the "Scan Leaf" button when we're not already loading/showing a result.
  scanButton.hidden = (state === "loading" || state === "result");
}
