import streamlit as st
import numpy as np
import cv2
from PIL import Image

# --- App Configuration ---
st.set_page_config(page_title="Crokinole Score Pro", layout="centered")
st.title("🥏 Crokinole Vision Scorer")

# Initialize Session State for game tracking
if 'game_data' not in st.session_state:
    st.session_state.game_data = {
        'set': 1,
        'scores': {1: [0, 0], 2: [0, 0], 3: [0, 0]},
        'history': []
    }

def calculate_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# --- Sidebar: Game Progress ---
st.sidebar.header(f"Current Game: Set {st.session_state.game_data['set']}")
for s in range(1, 4):
    p1, p2 = st.session_state.game_data['scores'][s]
    st.sidebar.write(f"**Set {s}:** P1: {p1} | P2: {p2}")

# --- Step 1: Manual 20-Point Entry ---
st.subheader("1. Enter 20s (Removed Pucks)")
col1, col2 = st.columns(2)
with col1:
    p1_20s = st.number_input("Player 1 (Light) 20s", min_value=0, step=1)
with col2:
    p2_20s = st.number_input("Player 2 (Dark) 20s", min_value=0, step=1)

# --- Step 2: Image Capture ---
st.subheader("2. Capture Board")
img_file = st.camera_input("Take a photo of the board at the end of the round")

if img_file:
    # Convert to OpenCV format
    image = Image.open(img_file)
    img_array = np.array(image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    st.info("Visual analysis running... (Simulating detection)")
    
    # Simple Logic Simulation:
    # In a production environment, we use HoughCircles or YOLOv8 here.
    # For this prototype, we'll allow a 'Process' button to generate counts.
    
    if st.button("Calculate Board Score"):
        # Placeholder for CV Detection Logic
        # In practice, this detects circles and checks distance from center
        board_p1 = 35 # Example detected points
        board_p2 = 20 # Example detected points
        
        total_p1 = board_p1 + (p1_20s * 20)
        total_p2 = board_p2 + (p2_20s * 20)
        
        curr_set = st.session_state.game_data['set']
        st.session_state.game_data['scores'][curr_set] = [total_p1, total_p2]
        
        st.success(f"Set {curr_set} Results: P1: {total_p1} | P2: {total_p2}")

# --- Step 3: Advance Game ---
if st.button("Finish Set & Move to Next"):
    if st.session_state.game_data['set'] < 3:
        st.session_state.game_data['set'] += 1
        st.rerun()
    else:
        st.balloons()
        st.header("🏆 Final Results")
        total_p1 = sum(s[0] for s in st.session_state.game_data['scores'].values())
        total_p2 = sum(s[1] for s in st.session_state.game_data['scores'].values())
        st.write(f"**Final Score - Player 1:** {total_p1}")
        st.write(f"**Final Score - Player 2:** {total_p2}")
        
        if st.button("Reset Game"):
            st.session_state.game_data = {
                'set': 1,
                'scores': {1: [0, 0], 2: [0, 0], 3: [0, 0]},
                'history': []
            }
            st.rerun()
