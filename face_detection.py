import cv2
import mediapipe as mp
import numpy as np
import time

# -------- CONFIG --------
EAR_THRESHOLD = 0.22
SLEEPING_TIME = 1  # seconds
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
MAX_TRACK_DIST = 50
# ------------------------

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=5)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def calculate_EAR(landmarks, eye_indices, w, h):
    points = [(int(landmarks[idx].x * w), int(landmarks[idx].y * h)) for idx in eye_indices]
    A = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
    B = np.linalg.norm(np.array(points[2]) - np.array(points[4]))
    C = np.linalg.norm(np.array(points[0]) - np.array(points[3]))
    return (A + B) / (2.0 * C)

# Shared state for frontend
detection_state = {
    "people_count": 0,
    "sleeping_count": 0,
    "any_sleeping": False
}

def generate_frames():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    next_face_id = 0
    faces_data = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        people_count = 0
        current_faces = []

        if results.multi_face_landmarks:
            people_count = len(results.multi_face_landmarks)
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                x_coords = [int(lm.x * w) for lm in landmarks]
                y_coords = [int(lm.y * h) for lm in landmarks]
                x_min, x_max = min(x_coords), max(x_coords)
                y_min, y_max = min(y_coords), max(y_coords)
                centroid = ((x_min + x_max) // 2, (y_min + y_max) // 2)
                current_faces.append({
                    "landmarks": landmarks,
                    "bbox": (x_min, y_min, x_max, y_max),
                    "centroid": centroid
                })

        # Match current faces to existing IDs
        unmatched_current = []
        matched_ids = set()
        for face in current_faces:
            cX, cY = face["centroid"]
            min_dist = float("inf")
            matched_id = None
            for fid, data in faces_data.items():
                if fid in matched_ids:
                    continue
                prev_cX, prev_cY = data["centroid"]
                dist = np.linalg.norm(np.array([cX, cY]) - np.array([prev_cX, prev_cY]))
                if dist < min_dist and dist < MAX_TRACK_DIST:
                    min_dist = dist
                    matched_id = fid
            if matched_id is not None:
                faces_data[matched_id]["centroid"] = face["centroid"]
                faces_data[matched_id]["bbox"] = face["bbox"]
                face["id"] = matched_id
                matched_ids.add(matched_id)
            else:
                unmatched_current.append(face)

        for face in unmatched_current:
            face["id"] = next_face_id
            faces_data[next_face_id] = {
                "centroid": face["centroid"],
                "eyes_closed_start": None,
                "bbox": face["bbox"]
            }
            next_face_id += 1

        current_ids = [face["id"] for face in current_faces]
        for fid in list(faces_data.keys()):
            if fid not in current_ids:
                del faces_data[fid]

        # Process EAR & sleeping detection
        sleeping_any = False
        sleeping_count = 0

        for face in current_faces:
            fid = face["id"]
            landmarks = face["landmarks"]
            x_min, y_min, x_max, y_max = face["bbox"]

            left_ear = calculate_EAR(landmarks, LEFT_EYE, w, h)
            right_ear = calculate_EAR(landmarks, RIGHT_EYE, w, h)
            avg_ear = (left_ear + right_ear) / 2

            sleeping = False
            if avg_ear < EAR_THRESHOLD:
                if faces_data[fid]["eyes_closed_start"] is None:
                    faces_data[fid]["eyes_closed_start"] = time.time()
                else:
                    elapsed = time.time() - faces_data[fid]["eyes_closed_start"]
                    if elapsed >= SLEEPING_TIME:
                        sleeping = True
                        sleeping_any = True
                        sleeping_count += 1
            else:
                faces_data[fid]["eyes_closed_start"] = None

            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
            cv2.putText(frame, f"ID:{fid}", (x_min, y_min - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, f"EAR:{avg_ear:.2f}", (x_min, y_min - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if sleeping:
                cv2.putText(frame, "SLEEPING!", (x_min, y_max + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.putText(frame, f"People: {people_count}", (30, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Update shared state
        detection_state["people_count"] = people_count
        detection_state["sleeping_count"] = sleeping_count
        detection_state["any_sleeping"] = sleeping_any

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()