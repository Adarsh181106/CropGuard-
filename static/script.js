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

    if (data.error === "not_a_leaf") {
      errorText.textContent = data.message;
      showState("error");
      return;
    }

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
// --- Tab switching ---
const tabButtons = document.querySelectorAll(".tab-btn");
const tabPanels = {
  scan: document.getElementById("scanTab"),
  fertilizer: document.getElementById("fertilizerTab"),
  cultivation: document.getElementById("cultivationTab"),
  chat: document.getElementById("chatTab"),
};

tabButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    tabButtons.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");

    Object.values(tabPanels).forEach((panel) => panel.classList.remove("active"));
    tabPanels[btn.dataset.tab].classList.add("active");
  });
});
// --- Fertilizer Calculator ---
// General per-acre guidelines (kg) — approximate, for demo purposes.
// Real dosage should come from a soil test or local agri extension officer.
const FERTILIZER_GUIDELINES = {
  tomato:     { urea: 120, dap: 100, mop: 60 },
  potato:     { urea: 100, dap: 150, mop: 100 },
  corn:       { urea: 100, dap: 50,  mop: 40 },
  wheat:      { urea: 100, dap: 50,  mop: 25 },
  rice:       { urea: 120, dap: 50,  mop: 40 },
  grape:      { urea: 80,  dap: 60,  mop: 80 },
  soybean:    { urea: 20,  dap: 60,  mop: 40 },
  pepper:     { urea: 100, dap: 80,  mop: 60 },
  strawberry: { urea: 60,  dap: 80,  mop: 60 },
  other:      { urea: 100, dap: 60,  mop: 40 },
};

const cropSelect = document.getElementById("cropSelect");
const plotMinus = document.getElementById("plotMinus");
const plotPlus = document.getElementById("plotPlus");
const plotSizeValue = document.getElementById("plotSizeValue");
const calcFertilizerButton = document.getElementById("calcFertilizerButton");
const fertilizerResult = document.getElementById("fertilizerResult");
const ureaValue = document.getElementById("ureaValue");
const dapValue = document.getElementById("dapValue");
const mopValue = document.getElementById("mopValue");

let plotSize = 1;

plotMinus.addEventListener("click", () => {
  if (plotSize > 1) {
    plotSize--;
    plotSizeValue.textContent = plotSize;
  }
});

plotPlus.addEventListener("click", () => {
  plotSize++;
  plotSizeValue.textContent = plotSize;
});

function formatFertilizer(kgPerAcre, acres) {
  const totalKg = kgPerAcre * acres;
  const bags = (totalKg / 50).toFixed(1); // standard 50kg bag
  return `${totalKg} kg (${bags} bags)`;
}

calcFertilizerButton.addEventListener("click", () => {
  const crop = cropSelect.value;
  const guideline = FERTILIZER_GUIDELINES[crop];

  ureaValue.textContent = formatFertilizer(guideline.urea, plotSize);
  dapValue.textContent = formatFertilizer(guideline.dap, plotSize);
  mopValue.textContent = formatFertilizer(guideline.mop, plotSize);

  fertilizerResult.hidden = false;
});
// --- Cultivation Tips ---
const CULTIVATION_TIPS = {
  tomato: [
    { week: "Week 0", title: "Sowing", desc: "Sow seeds in trays or nursery beds. Keep soil moist and warm (20-25°C) for germination." },
    { week: "Week 2-3", title: "Transplanting", desc: "Move seedlings to the field once they have 4-6 true leaves. Space plants 45-60cm apart." },
    { week: "Week 4-6", title: "Vegetative growth", desc: "Stake or cage plants for support. Water regularly and watch for early blight symptoms." },
    { week: "Week 7-9", title: "Flowering", desc: "Reduce nitrogen, increase potassium. Ensure consistent watering to prevent blossom-end rot." },
    { week: "Week 10-12", title: "Fruiting", desc: "Support heavy branches. Watch for late blight in humid conditions." },
    { week: "Week 13+", title: "Harvest", desc: "Pick fruits when fully colored but still firm. Harvest every 2-3 days during peak season." },
  ],
  potato: [
    { week: "Week 0", title: "Planting", desc: "Plant seed potatoes 10-15cm deep, 30cm apart, in well-drained soil." },
    { week: "Week 2-4", title: "Emergence", desc: "Shoots emerge. Hill soil around stems as they grow to protect developing tubers." },
    { week: "Week 5-8", title: "Vegetative growth", desc: "Keep soil consistently moist. Watch for early blight on lower leaves." },
    { week: "Week 9-11", title: "Tuber formation", desc: "Critical watering period — irregular water causes cracked/misshapen tubers." },
    { week: "Week 12-14", title: "Maturation", desc: "Reduce watering as foliage yellows and dies back naturally." },
    { week: "Week 15+", title: "Harvest", desc: "Harvest once foliage has died back. Cure in a cool, dark place before storage." },
  ],
  corn: [
    { week: "Week 0", title: "Planting", desc: "Sow seeds 3-5cm deep after soil warms above 15°C. Space rows 60-75cm apart." },
    { week: "Week 2-3", title: "Emergence", desc: "Seedlings emerge. Thin to one plant every 20-25cm." },
    { week: "Week 4-7", title: "Vegetative growth", desc: "Rapid growth phase — apply nitrogen fertilizer. Watch for Northern Leaf Blight." },
    { week: "Week 8-9", title: "Tasseling & silking", desc: "Critical water period for pollination. Avoid drought stress during this window." },
    { week: "Week 10-13", title: "Grain fill", desc: "Kernels develop and fill. Maintain consistent moisture." },
    { week: "Week 14+", title: "Harvest", desc: "Harvest when kernels are firm and husks have dried and browned." },
  ],
  wheat: [
    { week: "Week 0", title: "Sowing", desc: "Sow seeds 3-5cm deep in well-prepared soil, ideally in cooler temperatures." },
    { week: "Week 2-4", title: "Germination & tillering", desc: "Multiple shoots emerge from each plant. Apply first nitrogen dose." },
    { week: "Week 5-8", title: "Stem extension", desc: "Rapid vertical growth. Second nitrogen application; monitor for rust diseases." },
    { week: "Week 9-11", title: "Heading & flowering", desc: "Grain heads emerge and flower. Critical water-sensitive period." },
    { week: "Week 12-15", title: "Grain fill", desc: "Grains develop and fill. Reduce watering as maturity approaches." },
    { week: "Week 16+", title: "Harvest", desc: "Harvest when grain is hard and straw has turned golden." },
  ],
  rice: [
    { week: "Week 0", title: "Nursery sowing", desc: "Sow seeds densely in a nursery bed for 3-4 weeks before transplanting." },
    { week: "Week 3-4", title: "Transplanting", desc: "Transplant seedlings into flooded, puddled fields, spaced 20x15cm apart." },
    { week: "Week 5-8", title: "Vegetative growth (tillering)", desc: "Maintain 2-5cm standing water. Apply nitrogen in split doses." },
    { week: "Week 9-11", title: "Panicle initiation & flowering", desc: "Most water-sensitive stage — avoid any drought stress." },
    { week: "Week 12-15", title: "Grain fill", desc: "Grains fill and ripen. Begin draining the field gradually." },
    { week: "Week 16+", title: "Harvest", desc: "Drain field fully 1-2 weeks before harvest. Harvest when 80-85% of grains turn golden." },
  ],
};

const cultivationCropSelect = document.getElementById("cultivationCropSelect");
const timelineContainer = document.getElementById("timelineContainer");

function renderCultivationTimeline(crop) {
  const stages = CULTIVATION_TIPS[crop];
  timelineContainer.innerHTML = stages.map(stage => `
    <div class="timeline-item">
      <div class="timeline-week">${stage.week}</div>
      <div class="timeline-body">
        <h3>${stage.title}</h3>
        <p>${stage.desc}</p>
      </div>
    </div>
  `).join("");
}

cultivationCropSelect.addEventListener("change", () => {
  renderCultivationTimeline(cultivationCropSelect.value);
});

// Show tomato's timeline by default when the page loads
renderCultivationTimeline("tomato");