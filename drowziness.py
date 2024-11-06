import google.generativeai as genai
import os, cv2, asyncio

class DrowsinessCheck:
    def __init__(self):
        GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)
        self.is_checking = False  # Flag to prevent multiple calls

    async def g_vision(self, image):
        if self.is_checking:
            print('Drowsiness check already in progress, skipping...')
            return 'In Progress'

        self.is_checking = True  # Lock the check to prevent multiple calls
        temp_path = "temp_image.jpg"
        
        try:
            # Write the image to a temporary file asynchronously
            cv2.imwrite(temp_path, image)
            
            # Upload the temporary file asynchronously
            sample_file = await asyncio.to_thread(genai.upload_file, path=temp_path, display_name="image")
            print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
            
            # Retrieve the file details asynchronously
            file = await asyncio.to_thread(genai.get_file, name=sample_file.name)
            print(f"Retrieved file '{file.display_name}' as: {file.uri}")
            
            # Analyze the image using the Gemini model asynchronously
            model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
            response = await asyncio.to_thread(
                model.generate_content,
                [sample_file, "Your task is to understand the image and tell whether the person who is meditating in the image is feeling drowsy or not. Remember the person is meditating maybe his/her eyes are closed or open.If the head of the person is facing downwards then also you can consider the person is Drowsy.Don't include any special characters. Your output should only be 'Drowsy' or 'Not Drowsy' only. Do not include special charaters like *,@,# or any such charactes it should be a plain text only."]
            )
            print(response.text)
            return str(response.text)
        
        except Exception as e:
            print(f'Error encountered: {e}')
            return 'error'
        
        finally:
            self.is_checking = False  # Unlock after the check is complete
