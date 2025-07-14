from flask import Flask, render_template, request
import cv2
import os
import uuid
import boto3
import openpyxl

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

AWS_ACCESS_KEY = "AKIAX2QPHVOFIH55RZ7Y"
AWS_SECRET_KEY = "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"
BUCKET_NAME = "face-attendance-bhargav1"

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name="ap-south-1"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        return "Failed to capture image"

    # Save webcam image
    filename = f"scanned_{uuid.uuid4()}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    cv2.imwrite(filepath, frame)
    cap.release()

    # Upload to S3
    try:
        s3.upload_file(filepath, BUCKET_NAME, f"scanned_faces/{filename}")
    except Exception as e:
        return f"❌ S3 Upload failed: {e}"

    # Initialize Rekognition client
    rekognition = boto3.client(
        "rekognition",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name="ap-south-1"
    )

    matched_name = None

    # Make sure local students folder exists
    student_folder = "students"
    if not os.path.exists(student_folder):
        return "❌ Local 'students' folder not found. Create and add student images."

    for student_file in os.listdir(student_folder):
        student_name = student_file.rsplit(".", 1)[0]
        try:
            response = rekognition.compare_faces(
                SourceImage={'S3Object': {'Bucket': BUCKET_NAME, 'Name': f"students_db/{student_file}"}},
                TargetImage={'S3Object': {'Bucket': BUCKET_NAME, 'Name': f"scanned_faces/{filename}"}},
                SimilarityThreshold=85
            )
            if response['FaceMatches']:
                matched_name = student_name
                break
        except Exception as e:
            print(f"Error comparing {student_file}: {e}")

    # Update attendance file
    if matched_name:
        try:
            wb = openpyxl.load_workbook("attendance.xlsx")
            sheet = wb.active
            for row in sheet.iter_rows(min_row=2):
                if row[0].value == matched_name:
                    row[1].value = "Present"
                    break
            wb.save("attendance.xlsx")
        except Exception as e:
            return f"✅ Match found: {matched_name}, but attendance file error: {e}"

        return render_template("success.html", image_url=filepath, name=matched_name)
    else:
        return "No match found"

if __name__ == "__main__":
    app.run(debug=True)
