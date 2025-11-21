import cv2
import time
from paddleocr import PaddleOCR


def run_manual_ocr(image_path: str):
    """
    Manual OCR pipeline using PaddleOCR (native).
    Shows: manual model loading, slow startup, preprocessing,
           and non-abstracted OCR execution.
    """

    # ---- 1. Load Model (SLOW, Manual, Heavy) ----
    # WHY: paddleocr loads 3 models: detector, angle classifier, recognizer
    #      Also downloads weights on first run.
    start_load = time.time()

    ocr = PaddleOCR(
        use_angle_cls=True,
        lang='en',
        show_log=False
    )

    load_time = time.time() - start_load
    # print(f"[Manual OCR] Model loaded in {load_time:.2f} seconds.")

    # ---- 2. Read & Preprocess Image Manually ----
    # WHY: PaddleOCR doesn't abstract preprocessing.
    #      You must handle image loading + BGR → RGB conversion.
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Image not found or unable to read."}
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # ---- 3. Run OCR (Detector + Angle Classifier + Recognizer) ----
    start_infer = time.time()
    result = ocr.ocr(img, cls=True)
    infer_time = time.time() - start_infer
    # print(f"[Manual OCR] Inference completed in {infer_time:.2f} seconds.")

    # ---- 4. Extract Text & Confidence ----
    extracted = []
    for line in result:
        for box, text_info in line:
            text, confidence = text_info
            extracted.append({
                "text": text,
                "confidence": float(confidence)
            })
    return {
        "text_results": extracted,
        "load_time": load_time,
        "inference_time": infer_time    
    }

if __name__ == "__main__":
    out = run_manual_ocr("sample_images/sample1.png")
    print(out)