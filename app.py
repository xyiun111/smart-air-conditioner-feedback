import streamlit as st
import pandas as pd

# 確保 session_state 初始化
if 'points' not in st.session_state:
    st.session_state.points = 0  # 初始積分為 0

# 初始化 `feedback` 為預設值"剛好"
if 'feedback' not in st.session_state:
    st.session_state.feedback = "剛好"  # 預設選擇"剛好"

# 顯示應用標題
st.title("互動式節能空調系統模擬")

# 讀取 Colab 產生的虛擬感測資料
df = pd.read_csv("sensor_data.csv")

# 使用者選擇要查看哪一筆模擬資料，並重置積分與回饋
index = st.slider("選擇資料編號", 0, len(df)-1, 0)

# 重置積分與回饋
if index != st.session_state.get('last_index', -1):  # 檢查是否為新資料
    st.session_state.feedback = "剛好"  # 回饋清空為預設值
    st.session_state.points = 0  # 積分歸零

# 儲存當前索引，避免重置多次
st.session_state.last_index = index

# 取得當前選擇資料
temp = df.loc[index, 'temperature']
people = df.loc[index, 'people']

# 顯示當前教室溫度與人數
st.write(f"目前教室溫度：🌡️ {temp:.1f}°C")
st.write(f"目前人數：👥 {int(people)}人")

# 學生回饋
feedback = st.radio("你覺得現在的溫度如何？", ["太冷", "剛好", "太熱"],
                    index=["太冷", "剛好", "太熱"].index(st.session_state.feedback), key="feedback")

# 計算建議的溫度和積分
if feedback == "太熱":
    recommended = temp - 1
    points_awarded = 10  # 給予更多積分，鼓勵節能行為
elif feedback == "太冷":
    recommended = temp + 1
    points_awarded = 5  # 給予較少的積分
else:
    recommended = temp
    points_awarded = 0  # 無需積分獎勳

# 更新並顯示積分
st.session_state.points += points_awarded

# 顯示系統建議
st.success(f"系統建議設定溫度為：{recommended:.1f}°C")

# 顯示學生累積的綠點積分
st.write(f"你的綠點積分：🌱 {st.session_state.points} 點")

# 鼓勵學生繼續參與節能
if points_awarded > 0:
    st.balloons()  # 顯示慶祝氣球，表示有積分獲得
    st.write("太棒了！你為節能行為做出了貢獻！")
    
    
    
    
    

