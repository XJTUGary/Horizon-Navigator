import cv2
import mediapipe as mp
import time
from djitellopy import tello



class PoseTracking:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_draw = mp.solutions.drawing_utils
        self.drone = tello.Tello()

    def process_pose(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)
        if results.pose_landmarks:
            self.mp_draw.draw_landmarks(img, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark
            return img, self.detect_posture(landmarks)
        return img, []

    def detect_posture(self, landmarks):
        detected_postures = []
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE]

        reference_width = abs(left_shoulder.x - right_shoulder.x)
        reference_height = abs((left_shoulder.y + right_shoulder.y) / 2 - (left_hip.y + right_hip.y) / 2)

        # Detect squatting or standing
        if (left_knee.y + right_knee.y) / 2 - (left_hip.y + right_hip.y) / 2 > 0.3 * reference_height:
            print("检测到站立姿态")
            detected_postures.append("stand")
        else:
            print("检测到下蹲姿态")
            detected_postures.append("squat")

        # Detect right arm raised
        if right_shoulder.x - right_wrist.x > 0.5 * reference_width:
            print("检测到右手侧平举")
            detected_postures.append("right_arm_raised")

        # Detect left arm raised
        if left_wrist.x - left_shoulder.x > 0.5 * reference_width:
            print("检测到左手侧平举")
            detected_postures.append("left_arm_raised")

        return detected_postures

    def tracking_posture(self, action):
        if not action:
            return

        # Check the first action in the list
        if action[0] == "squat":
            print("Detected squat - descending 20 units")
            self.drone.send_rc_control(0, 0, -20, 0)  # Descend 20 units
            time.sleep(2)
            self.drone.send_rc_control(0, 0, 20, 0)  # Ascend 20 units
            print("Ascending back to original height")

        # Check the second action in the list, if available
        if len(action) > 1:
            if action[1] == "right_arm_raised":
                print("Detected right arm raised - moving right")
                self.drone.send_rc_control(20, 0, 0, 0)  # Move right by 20 units
                time.sleep(1)

            elif action[1] == "left_arm_raised":
                print("Detected left arm raised - moving left")
                self.drone.send_rc_control(-20, 0, 0, 0)  # Move left by 20 units
                time.sleep(1)

if __name__ == "__main__":
    w, h = 360, 240
    pose_tracker = PoseTracking()
    pose_tracker.drone.connect()

    # print out battery percentage
    print(pose_tracker.drone.get_battery())

    # Get Stream
    pose_tracker.drone.streamon()
    pose_tracker.drone.takeoff()
    pose_tracker.drone.send_rc_control(0, 0, 30, 0)
    time.sleep(2.2)
    while True:
        # Capture frame from the Tello drone
        img = pose_tracker.drone.get_frame_read().frame
        img = cv2.resize(img, (w, h))

        # Process pose and get the image with landmarks and detected actions
        img, actions = pose_tracker.process_pose(img)

        # Display the image
        cv2.imshow("Pose Tracking", img)

        # Act based on the detected actions
        pose_tracker.tracking_posture(actions)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pose_tracker.drone.land()
            break
    cv2.destroyAllWindows()