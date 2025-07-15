# SmartAttendance
# Smart Attendance System using Face Recognition (AWS-Based)

A smart, contactless attendance system built using **AWS Rekognition**, **S3**, and a **Python Flask** web interface to automate student attendance using face recognition.

## 👨‍💻 Project Members

- **Harshit Dumpa** (Intern ID: BV25-EM-154) - harshitreddydumpa@gmail.com  
- **P. Bhargav** (Intern ID: BV25-EM-156) - bhargavpallanti12345@gmail.com  
- **S Sampath Vinay** (Intern ID: BV25-EM-155) - ssampathvinayreddy@gmail.com  

---

## 🚀 Project Objective

To automate the attendance process in educational institutions using real-time face recognition technology. The system eliminates manual effort and enhances security and accuracy.

---

## 🧠 Features

- Real-time face recognition using webcam
- Comparison with reference images stored in **AWS S3**
- Face matching powered by **AWS Rekognition**
- Attendance automatically marked as “Present” in Excel
- User-friendly **Flask web app** interface
- Data privacy via **IAM key** access controls

---

## 🛠️ Technologies Used

| Category              | Tools/Services                      |
|-----------------------|--------------------------------------|
| Programming Language  | Python                              |
| Web Framework         | Flask                               |
| Cloud Platform        | Amazon Web Services (AWS)           |
| AWS Services          | Rekognition, S3, IAM                |
| Image Processing      | OpenCV                              |
| Data Handling         | openpyxl (Excel automation)         |
| IDE                   | VS Code / Jupyter Notebook          |

---

## 🔧 System Architecture

1. **Upload Phase**  
   Student images uploaded to S3 in `students_db/` folder.

2. **Initialization**  
   An Excel file (`attendance.xlsx`) is created with all students marked "Absent".

3. **Face Capture**  
   Clicking "Take Attendance" captures image via webcam.

4. **Face Recognition**  
   The image is compared with S3 images using AWS Rekognition.

5. **Attendance Update**  
   - If matched: Marked “Present” in Excel.
   - If not: Displayed as “Face Not Found”.

---

## 📂 Directory Structure


