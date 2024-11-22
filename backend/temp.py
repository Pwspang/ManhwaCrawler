from ultralytics import YOLO
from PIL import Image, ImageDraw
import cv2
# from transformers import AutoImageProcessor, AutoModelForObjectDetection
from transformers import pipeline   

def main():
    model = YOLO("backend/model_weights/best.pt")
    image = cv2.imread("backend/4.webp")
    h, w, c = image.shape

    results = model(
        image,
        # dimensions required to be multiple of 32
        imgsz=[(h // 32) * 32, (w // 32) * 32],
        conf=0.6,
    )[0]
    # save the image with bounding boxes
    #results.save("output.jpg")
    
    images = [image[int(y1):int(y2),int(x1):int(x2)] for x1, y1, x2, y2 in results.boxes.xyxy]
    
    # Load model directly
    pipe = pipeline("image-to-text", model="kha-white/manga-ocr-base")
    
    print(pipe(Image.fromarray(images[0])))
    
if __name__ == "__main__":
    main()

