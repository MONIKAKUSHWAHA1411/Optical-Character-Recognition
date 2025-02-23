import os
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from PIL import Image
import pytesseract

# Load the Kivy UI from myocr.kv
Builder.load_file("myocr.kv")

class MyOCRApp(App):
    def build(self):
        self.root = Builder.load_file("myocr.kv")
        return self.root

    def start_camera(self):
        camera = self.root.ids.camera_widget
        camera.play = True

    def capture_image(self):
        camera = self.root.ids.camera_widget
        # Capture current frame and save it to a temporary file
        texture = camera.texture
        if texture:
            # Convert Kivy texture to PIL Image
            size = texture.size
            pixels = texture.pixels  # raw RGBA bytes
            image = Image.frombytes(mode="RGBA", size=size, data=pixels)
            
            # Save temporary image file
            temp_image_path = "captured_image.png"
            image.save(temp_image_path)
            
            # Process image with OCR
            extracted_text = self.extract_text(temp_image_path)
            self.root.ids.result_text.text = extracted_text
            
            # Optionally, remove the temporary file
            os.remove(temp_image_path)
        else:
            self.show_popup("Error", "No image captured!")

    def extract_text(self, image_path):
        try:
            # Open image using Pillow
            img = Image.open(image_path)
            # Convert image to string using pytesseract
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            return f"Error processing image: {e}"

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(None, None), size=(300, 200))
        popup.open()

if __name__ == "__main__":
    MyOCRApp().run()
