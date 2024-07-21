from flask import Flask, Response, request, render_template, jsonify
import cv2
from cvzone.PoseModule import PoseDetector

app = Flask(__name__)

# Global variables for pose detection
cap_pose = cv2.VideoCapture(0)
detector_pose = PoseDetector(staticMode=False, modelComplexity=1, smoothLandmarks=True,
                             enableSegmentation=False, smoothSegmentation=True, detectionCon=0.5, trackCon=0.5)
tpose_detected = False
camera_running_pose = True

def TPose_detector():
    global tpose_detected, camera_running_pose
    while camera_running_pose:
        success, img = cap_pose.read()
        if not success:
            break

        img = detector_pose.findPose(img)
        lmList, bboxInfo = detector_pose.findPosition(img, draw=True, bboxWithHands=False)

        if lmList:
            center = bboxInfo["center"]
            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
            
            length, img, info = detector_pose.findDistance(lmList[11][0:2], lmList[15][0:2], img=img, color=(255, 0, 0), scale=10)
            angle1, img = detector_pose.findAngle(lmList[12][0:2], lmList[11][0:2], lmList[15][0:2], img=img, color=(255, 0, 255), scale=5)
            angle2, img = detector_pose.findAngle(lmList[11][0:2], lmList[12][0:2], lmList[16][0:2], color=(255, 0, 255), img=img, scale=5)

            rightisCloseAngle180 = detector_pose.angleCheck(myAngle=angle1, targetAngle=180, offset=10)
            leftisCloseAngle180 = detector_pose.angleCheck(myAngle=angle2, targetAngle=180, offset=10)

            if rightisCloseAngle180 and leftisCloseAngle180:
                tpose_detected = True
                cv2.putText(img, 'T-pose', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4)
            else:
                tpose_detected = False

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', img)[1].tobytes() + b'\r\n')

@app.route('/pose')
def pose_index():
    return render_template('index2.html')

@app.route('/pose_video_feed')
def pose_video_feed():
    global camera_running_pose
    camera_running_pose = True
    return Response(TPose_detector(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_camera_pose')
def stop_camera_pose():
    global camera_running_pose
    camera_running_pose = False
    cap_pose.release()
    return jsonify({'status': 'Camera stopped'})

@app.route('/tpose_status')
def tpose_status():
    global tpose_detected
    return jsonify({'tpose_detected': tpose_detected})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
