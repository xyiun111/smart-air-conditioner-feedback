import streamlit as st
import math

# 初始化 session_state
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'last_temp' not in st.session_state:
    st.session_state.last_temp = None
if 'last_people' not in st.session_state:
    st.session_state.last_people = None
if 'selected_feedback' not in st.session_state:
    st.session_state.selected_feedback = "剛好"

# 標題
st.title("互動式節能空調系統模擬")

# 手動輸入溫度與人數
temp = st.number_input("請輸入目前教室溫度（°C）：", min_value=10.0, max_value=40.0, value=25.0, step=0.1)
people = st.number_input("請輸入目前教室內人數：", min_value=0, max_value=100, value=30, step=1)

# 溫度或人數變動則重置分數與回饋
if temp != st.session_state.last_temp or people != st.session_state.last_people:
    st.session_state.points = 0
    st.session_state.selected_feedback = "剛好"
    st.write("📌 已重設積分與回饋（因為更改了溫度或人數）")

st.session_state.last_temp = temp
st.session_state.last_people = people

# 顯示目前狀態
st.write(f"目前教室溫度：🌡️ {temp:.1f}°C")
st.write(f"目前人數：👥 {int(people)}人")

# 選擇回饋（但不會立即送出）
selected = st.radio("你覺得現在的溫度如何？", ["太冷", "剛好", "太熱"],
                    index=["太冷", "剛好", "太熱"].index(st.session_state.selected_feedback))

# 根據人數計算溫度調整度數 (每15人調整1.5度)
adjustment_per_15 = 0.8
adjustment_factor = math.floor(people / 15) * adjustment_per_15

# 按下按鈕才送出回饋（不論是否與上次相同）
if st.button("送出回饋"):
    st.session_state.selected_feedback = selected

    if selected == "太冷":
        st.session_state.points += 5
        recommended = temp + adjustment_factor
        st.balloons()
        st.write("❄️ 感謝回饋，已加 5 分")
    elif selected == "太熱":
        st.session_state.points -= 2
        recommended = temp - adjustment_factor
        st.write("🔥 感謝回饋，已扣 2 分")
    else:  # 剛好
        recommended = temp
        st.write("😊 感謝回饋，目前為剛好，未變動分數")

    # 限制建議溫度範圍
    if recommended < 16:
        recommended = 16
        st.warning("再低北極熊會死翹翹 🐻‍❄️")
    elif recommended > 28:
        recommended = 28
        st.warning("你還去曬太陽好了!")

    st.success(f"系統建議設定溫度為：{recommended:.1f}°C")

# 顯示目前分數
st.write(f"你的綠點積分：🌱 {st.session_state.points} 點")
