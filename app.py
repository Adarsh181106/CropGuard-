import gradio as gr
from predict import predict

demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil", label="Upload a leaf photo"),
    outputs=[
        gr.Textbox(label="Disease"),
        gr.Textbox(label="Confidence"),
        gr.Textbox(label="Severity"),
        gr.Textbox(label="Recommended Action"),
    ],
    title="🌿 CropGuard — AI Crop Disease Detector",
    description="Upload a photo of a plant leaf to detect disease, estimate severity, and get a treatment recommendation.",
)

if __name__ == "__main__":
    demo.launch()