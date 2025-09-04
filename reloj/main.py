import streamlit as st
import time
from datetime import datetime
import math
 
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }
    .clock-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100vw;
        position: fixed;
        top: 0;
        left: 0;
    }
    .clock {
        width: 300px;
        height: 300px;
        background: #f0f2f6;
        border-radius: 50%;
        box-shadow: 8px 8px 16px #d1d3d8, -8px -8px 16px #ffffff;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .number {
        position: absolute;
        font-size: 1.2em;
        color: #333;
        transform: translate(-50%, -50%);
    }
    .hand {
        position: absolute;
        bottom: 50%;
        transform-origin: bottom;
        background: #333;
        border-radius: 4px;
    }
    .hour-hand {
        width: 6px;
        height: 80px;
    }
    .minute-hand {
        width: 4px;
        height: 100px;
    }
    .second-hand {
        width: 2px;
        height: 120px;
        background: #ff4d4d;
    }
    .center-dot {
        width: 12px;
        height: 12px;
        background: #333;
        border-radius: 50%;
        position: absolute;
    }
    @media (max-width: 600px) {
        .clock {
            width: 200px;
            height: 200px;
        }
        .number {
            font-size: 1em;
        }
        .hour-hand {
            height: 60px;
        }
        .minute-hand {
            height: 80px;
        }
        .second-hand {
            height: 90px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app
def main():
    st.title("")  # Empty title to avoid extra spacing
    clock_placeholder = st.empty()

    while True:
        current_time = datetime.now()
        hours = current_time.hour % 12
        minutes = current_time.minute
        seconds = current_time.second

        # Calculate angles for clock hands
        hour_angle = (hours * 30) + (minutes / 2)
        minute_angle = minutes * 6
        second_angle = seconds * 6

        # Generate numbers HTML
        numbers_html = ""
        for i in range(1, 13):
            angle_deg = (i % 12) * 30
            angle_rad = math.radians(angle_deg)
            delta_left = 40 * math.sin(angle_rad)
            delta_top = 40 * -math.cos(angle_rad)
            numbers_html += f'<div class="number" style="left: calc(50% + {delta_left:.2f}%); top: calc(50% + {delta_top:.2f}%);">{i}</div>'

        # HTML for the clock
        clock_html = f"""
        <div class="clock-container">
            <div class="clock">
                {numbers_html}
                <div class="hand hour-hand" style="transform: rotate({hour_angle}deg);"></div>
                <div class="hand minute-hand" style="transform: rotate({minute_angle}deg);"></div>
                <div class="hand second-hand" style="transform: rotate({second_angle}deg);"></div>
                <div class="center-dot"></div>
            </div>
        </div>
        """
        clock_placeholder.markdown(clock_html, unsafe_allow_html=True)
        time.sleep(1)

if __name__ == "__main__":
    main()