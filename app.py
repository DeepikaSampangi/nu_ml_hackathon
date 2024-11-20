from flask import Flask, render_template, request, jsonify
import os
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_videos():
    if 'videos' not in request.files:
        return jsonify({'error': 'No files provided!'}), 400
    
    files = request.files.getlist('videos')
    file_paths = []
    
    for file in files:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        file_paths.append(filepath)

    # Process videos
    video_data = process_videos(file_paths)
    
    return jsonify({'message': 'Videos uploaded and processed!', 'data': video_data}), 200

def process_videos(file_paths):
    video_info = []
    for path in file_paths:
        cap = cv2.VideoCapture(path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        video_info.append({
            'filename': os.path.basename(path),
            'frame_count': frame_count,
            'fps': fps
        })
        cap.release()
    return video_info

if __name__ == '__main__':
    app.run(debug=True)
