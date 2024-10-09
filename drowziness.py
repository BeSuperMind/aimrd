import google.generativeai as genai
import os, cv2

class DrowsinessCheck:
    def __init__(self):
        GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)

    async def g_vision(self, image):
        temp_path = "temp_image.jpg"
        cv2.imwrite(temp_path, image)
        # Upload the temporary file
        sample_file = genai.upload_file(path=temp_path, display_name="image")
        print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
        file = genai.get_file(name=sample_file.name)
        print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")
        # Analyze the image using the Gemini model
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        try:
            response = model.generate_content([sample_file, "Your task is to understand the image and tell whether the person who is meditating in the image is feeling drowzy or not. Remember the person is meditating maybe his/her eyes are closed or open. Don't include any special characters. Your output should only be 'Drowsy' or 'Not Drowsy' only.Do not include special charaters like *,@,# or any such charactes it should be a plain text only."]).text
            print(response)
            return str(response)
        except Exception as e:
            print(f'Error encountered in detecting drowsiness: {e}')
            return 'False'
        