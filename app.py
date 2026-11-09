import random
import google.generativeai as genai
import streamlit as st

# Page Config
st.set_page_config(
    page_title="HSK 1 Learning Hub", page_icon="🇨🇳", layout="wide"
)

# Custom Compact UI & Duolingo-style Progress Bar CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Force compact layout to eliminate scrolling */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 900px !important;
        margin: auto;
    }
    
    /* Top Header & Navigation Bar */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #FFFFFF;
        padding: 12px 20px;
        border-radius: 14px;
        border: 2px solid #E2E8F0;
        margin-bottom: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    
    /* Beautiful Duolingo-style Progress Bar */
    .duo-progress-container {
        background-color: #E2E8F0;
        border-radius: 999px;
        height: 16px;
        width: 100%;
        overflow: hidden;
        margin-bottom: 16px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
    }
    .duo-progress-bar {
        background: linear-gradient(90deg, #58CC02 0%, #89E219 100%);
        height: 100%;
        border-radius: 999px;
        transition: width 0.4s ease-in-out;
    }
    
    /* Compact Flashcard Container */
    .compact-card {
        background-color: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 35px 20px;
        text-align: center;
        box-shadow: 0 8px 20px -4px rgba(0,0,0,0.04);
        margin-bottom: 16px;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .chinese-text {
        font-size: 4.5rem !important;
        font-weight: 700 !important;
        color: #1E293B;
        line-height: 1.1;
        margin: 0;
    }
    .meaning-text {
        font-size: 2rem !important;
        font-weight: 600 !important;
        color: #1E293B;
        margin: 4px 0;
    }
    .pinyin-text {
        font-size: 1.4rem !important;
        font-weight: 500 !important;
        color: #3B82F6;
        margin-top: 4px;
    }
    .kaiti-font {
        font-family: 'KaiTi', 'STKaiti', 'AR PL Kaiti M GB', serif !important;
    }

    /* Compact Buttons */
    div.stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        font-size: 1rem !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session State Vocabulary
if "vocab_list" not in st.session_state:
  st.session_state.vocab_list = [
      {"id": 1, "chinese": "我", "pinyin": "wǒ", "meaning": "I, me"},
      {"id": 2, "chinese": "我们", "pinyin": "wǒmen", "meaning": "we, us (pl.)"},
      {"id": 3, "chinese": "你", "pinyin": "nǐ", "meaning": "you"},
      {"id": 4, "chinese": "他", "pinyin": "tā", "meaning": "he, him"},
      {"id": 5, "chinese": "她", "pinyin": "tā", "meaning": "she, her"},
      {
          "id": 6,
          "chinese": "这(这儿)",
          "pinyin": "zhè (zhèr)",
          "meaning": "this (here)",
      },
      {
          "id": 7,
          "chinese": "那(那儿)",
          "pinyin": "nà (nàr)",
          "meaning": "that (there)",
      },
      {"id": 8, "chinese": "哪", "pinyin": "nǎ", "meaning": "which"},
      {"id": 9, "chinese": "哪儿", "pinyin": "nǎr", "meaning": "where"},
      {"id": 10, "chinese": "谁", "pinyin": "shéi", "meaning": "who"},
      {"id": 11, "chinese": "什么", "pinyin": "shénme", "meaning": "what"},
      {
          "id": 12,
          "chinese": "多少",
          "pinyin": "duōshǎo",
          "meaning": "how many, how much",
      },
      {"id": 13, "chinese": "几", "pinyin": "jǐ", "meaning": "a few, how many"},
      {"id": 14, "chinese": "怎么", "pinyin": "zěnme", "meaning": "how"},
      {
          "id": 15,
          "chinese": "怎么样",
          "pinyin": "zěnmeyàng",
          "meaning": "how about",
      },
      {"id": 16, "chinese": "一", "pinyin": "yī", "meaning": "one"},
      {"id": 17, "chinese": "二", "pinyin": "èr", "meaning": "two"},
      {"id": 18, "chinese": "三", "pinyin": "sān", "meaning": "three"},
      {"id": 19, "chinese": "四", "pinyin": "sì", "meaning": "four"},
      {"id": 20, "chinese": "五", "pinyin": "wǔ", "meaning": "five"},
      {"id": 21, "chinese": "六", "pinyin": "liù", "meaning": "six"},
      {"id": 22, "chinese": "七", "pinyin": "qī", "meaning": "seven"},
      {"id": 23, "chinese": "八", "pinyin": "bā", "meaning": "eight"},
      {"id": 24, "chinese": "九", "pinyin": "jiǔ", "meaning": "nine"},
      {"id": 25, "chinese": "十", "pinyin": "shí", "meaning": "ten"},
      {
          "id": 26,
          "chinese": "个",
          "pinyin": "gè",
          "meaning": "(for normal objects)",
      },
      {"id": 27, "chinese": "岁", "pinyin": "suì", "meaning": "(for age)"},
      {"id": 28, "chinese": "本", "pinyin": "běn", "meaning": "(for books)"},
      {"id": 29, "chinese": "些", "pinyin": "xiē", "meaning": "some"},
      {
          "id": 30,
          "chinese": "块",
          "pinyin": "kuài",
          "meaning": "piece, chunk",
      },
      {"id": 31, "chinese": "不", "pinyin": "bù", "meaning": "no"},
      {"id": 32, "chinese": "没", "pinyin": "méi", "meaning": "no"},
      {
          "id": 33,
          "chinese": "很",
          "pinyin": "hěn",
          "meaning": "quite, very",
      },
      {"id": 34, "chinese": "太", "pinyin": "tài", "meaning": "too"},
      {"id": 35, "chinese": "都", "pinyin": "dōu", "meaning": "all"},
      {
          "id": 36,
          "chinese": "一点儿",
          "pinyin": "yīdiǎnr",
          "meaning": "a little bit",
      },
      {"id": 37, "chinese": "和", "pinyin": "hé", "meaning": "and"},
      {"id": 38, "chinese": "在", "pinyin": "zài", "meaning": "in, at"},
      {"id": 39, "chinese": "的", "pinyin": "de", "meaning": "possessive particle"},
      {
          "id": 40,
          "chinese": "了",
          "pinyin": "le",
          "meaning": "completed action marker",
      },
      {"id": 41, "chinese": "吗", "pinyin": "ma", "meaning": "question particle"},
      {
          "id": 42,
          "chinese": "呢",
          "pinyin": "ne",
          "meaning": "modal particle",
      },
      {"id": 43, "chinese": "喂", "pinyin": "wèi", "meaning": "hello"},
      {"id": 44, "chinese": "家", "pinyin": "jiā", "meaning": "home"},
      {
          "id": 45,
          "chinese": "学校",
          "pinyin": "xuéxiào",
          "meaning": "school",
      },
      {
          "id": 46,
          "chinese": "饭店",
          "pinyin": "fàndiàn",
          "meaning": "restaurant",
      },
      {
          "id": 47,
          "chinese": "商店",
          "pinyin": "shāngdiàn",
          "meaning": "store",
      },
      {
          "id": 48,
          "chinese": "医院",
          "pinyin": "yīyuàn",
          "meaning": "hospital",
      },
      {
          "id": 49,
          "chinese": "中国",
          "pinyin": "Zhōngguò",
          "meaning": "China",
      },
      {
          "id": 50,
          "chinese": "北京",
          "pinyin": "Běijīng",
          "meaning": "Beijing",
      },
      {"id": 51, "chinese": "上", "pinyin": "shàng", "meaning": "up"},
      {"id": 52, "chinese": "下", "pinyin": "xià", "meaning": "down"},
      {
          "id": 53,
          "chinese": "前面",
          "pinyin": "qiánmiàn",
          "meaning": "front",
      },
      {
          "id": 54,
          "chinese": "后面",
          "pinyin": "hòumiàn",
          "meaning": "behind",
      },
      {"id": 55, "chinese": "里", "pinyin": "lǐ", "meaning": "inside"},
      {
          "id": 56,
          "chinese": "今天",
          "pinyin": "jīntiān",
          "meaning": "today",
      },
      {
          "id": 57,
          "chinese": "明天",
          "pinyin": "míngtiān",
          "meaning": "tomorrow",
      },
      {
          "id": 58,
          "chinese": "昨天",
          "pinyin": "zuótiān",
          "meaning": "yesterday",
      },
      {
          "id": 59,
          "chinese": "上午",
          "pinyin": "shàngwǔ",
          "meaning": "morning",
      },
      {
          "id": 60,
          "chinese": "中午",
          "pinyin": "zhōngwǔ",
          "meaning": "noon",
      },
      {
          "id": 61,
          "chinese": "下午",
          "pinyin": "xiàwǔ",
          "meaning": "afternoon",
      },
      {"id": 62, "chinese": "年", "pinyin": "nián", "meaning": "year"},
      {"id": 63, "chinese": "月", "pinyin": "yuè", "meaning": "month"},
      {
          "id": 64,
          "chinese": "号",
          "pinyin": "hào",
          "meaning": "number/date",
      },
      {"id": 65, "chinese": "星期", "pinyin": "xīngqī", "meaning": "week"},
      {"id": 66, "chinese": "点", "pinyin": "diǎn", "meaning": "o'clock"},
      {
          "id": 67,
          "chinese": "分钟",
          "pinyin": "fēnzhōng",
          "meaning": "minute",
      },
      {"id": 68, "chinese": "现在", "pinyin": "xiànzài", "meaning": "now"},
      {"id": 69, "chinese": "时候", "pinyin": "shíhou", "meaning": "time"},
      {"id": 70, "chinese": "爸爸", "pinyin": "bàba", "meaning": "father"},
      {"id": 71, "chinese": "妈妈", "pinyin": "māma", "meaning": "mother"},
      {"id": 72, "chinese": "儿子", "pinyin": "érzi", "meaning": "son"},
      {"id": 73, "chinese": "女儿", "pinyin": "nǚér", "meaning": "daughter"},
      {
          "id": 74,
          "chinese": "老师",
          "pinyin": "lǎoshī",
          "meaning": "teacher",
      },
      {
          "id": 75,
          "chinese": "学生",
          "pinyin": "xuéshēng",
          "meaning": "student",
      },
      {
          "id": 76,
          "chinese": "同学",
          "pinyin": "tóngxué",
          "meaning": "classmate",
      },
      {"id": 77, "chinese": "朋友", "pinyin": "péngyǒu", "meaning": "friend"},
      {"id": 78, "chinese": "医生", "pinyin": "yīshēng", "meaning": "doctor"},
      {"id": 79, "chinese": "先生", "pinyin": "xiānsheng", "meaning": "sir"},
      {"id": 80, "chinese": "小姐", "pinyin": "xiǎojiě", "meaning": "Miss"},
      {"id": 81, "chinese": "衣服", "pinyin": "yīfu", "meaning": "cloth"},
      {"id": 82, "chinese": "水", "pinyin": "shuǐ", "meaning": "water"},
      {"id": 83, "chinese": "菜", "pinyin": "cài", "meaning": "dish"},
      {"id": 84, "chinese": "米饭", "pinyin": "mǐfàn", "meaning": "rice"},
      {
          "id": 85,
          "chinese": "水果",
          "pinyin": "shuǐguǒ",
          "meaning": "fruit",
      },
      {
          "id": 86,
          "chinese": "苹果",
          "pinyin": "píngguǒ",
          "meaning": "apple",
      },
      {"id": 87, "chinese": "茶", "pinyin": "chá", "meaning": "tea"},
      {"id": 88, "chinese": "杯子", "pinyin": "bēizi", "meaning": "cup"},
      {"id": 89, "chinese": "钱", "pinyin": "qián", "meaning": "money"},
      {
          "id": 90,
          "chinese": "飞机",
          "pinyin": "fēijī",
          "meaning": "airplane",
      },
      {
          "id": 91,
          "chinese": "出租车",
          "pinyin": "chūzūchē",
          "meaning": "taxi",
      },
      {
          "id": 92,
          "chinese": "电视",
          "pinyin": "diànshì",
          "meaning": "television",
      },
      {
          "id": 93,
          "chinese": "电脑",
          "pinyin": "diànnǎo",
          "meaning": "computer",
      },
      {
          "id": 94,
          "chinese": "电影",
          "pinyin": "diànyǐng",
          "meaning": "movie",
      },
      {
          "id": 95,
          "chinese": "天气",
          "pinyin": "tiānqì",
          "meaning": "weather",
      },
      {"id": 96, "chinese": "猫", "pinyin": "māo", "meaning": "cat"},
      {"id": 97, "chinese": "狗", "pinyin": "gǒu", "meaning": "dog"},
      {"id": 98, "chinese": "东西", "pinyin": "dōngxi", "meaning": "thing"},
      {"id": 99, "chinese": "人", "pinyin": "rén", "meaning": "person"},
      {"id": 100, "chinese": "名字", "pinyin": "míngzi", "meaning": "name"},
      {"id": 101, "chinese": "书", "pinyin": "shū", "meaning": "book"},
      {
          "id": 102,
          "chinese": "汉语",
          "pinyin": "hànyǔ",
          "meaning": "mandarin Chinese",
      },
      {
          "id": 103,
          "chinese": "字",
          "pinyin": "zì",
          "meaning": "character",
      },
      {"id": 104, "chinese": "桌子", "pinyin": "zhuōzi", "meaning": "desk"},
      {"id": 105, "chinese": "椅子", "pinyin": "yǐzi", "meaning": "chair"},
      {"id": 106, "chinese": "谢谢", "pinyin": "xièxie", "meaning": "thank"},
      {
          "id": 107,
          "chinese": "不客气",
          "pinyin": "búkèqi",
          "meaning": "you are welcome",
      },
      {
          "id": 108,
          "chinese": "再见",
          "pinyin": "zàijiàn",
          "meaning": "good-bye",
      },
      {"id": 109, "chinese": "请", "pinyin": "qǐng", "meaning": "please"},
      {
          "id": 110,
          "chinese": "对不起",
          "pinyin": "duìbùqǐ",
          "meaning": "sorry",
      },
      {
          "id": 111,
          "chinese": "没关系",
          "pinyin": "méiguānxì",
          "meaning": "It doesn't matter",
      },
      {
          "id": 112,
          "chinese": "是",
          "pinyin": "shì",
          "meaning": "be (am, is, are)",
      },
      {"id": 113, "chinese": "有", "pinyin": "yǒu", "meaning": "have"},
      {"id": 114, "chinese": "看", "pinyin": "kàn", "meaning": "look"},
      {"id": 115, "chinese": "听", "pinyin": "tīng", "meaning": "listen"},
      {"id": 116, "chinese": "说", "pinyin": "shuō", "meaning": "speak"},
      {"id": 117, "chinese": "读", "pinyin": "dú", "meaning": "read"},
      {"id": 118, "chinese": "写", "pinyin": "xiě", "meaning": "write"},
      {
          "id": 119,
          "chinese": "看见",
          "pinyin": "kànjiàn",
          "meaning": "see",
      },
      {"id": 120, "chinese": "叫", "pinyin": "jiào", "meaning": "call"},
      {"id": 121, "chinese": "来", "pinyin": "lái", "meaning": "come"},
      {"id": 122, "chinese": "回", "pinyin": "huí", "meaning": "return"},
      {"id": 123, "chinese": "去", "pinyin": "qù", "meaning": "go"},
      {"id": 124, "chinese": "吃", "pinyin": "chī", "meaning": "eat"},
      {"id": 125, "chinese": "喝", "pinyin": "hē", "meaning": "drink"},
      {
          "id": 126,
          "chinese": "睡觉",
          "pinyin": "shuìjiào",
          "meaning": "sleep",
      },
      {
          "id": 127,
          "chinese": "打电话",
          "pinyin": "dǎdiànhuà",
          "meaning": "make phone call",
      },
      {"id": 128, "chinese": "做", "pinyin": "zuò", "meaning": "do"},
      {"id": 129, "chinese": "买", "pinyin": "mǎi", "meaning": "buy"},
      {"id": 130, "chinese": "开", "pinyin": "kāi", "meaning": "open"},
      {"id": 131, "chinese": "坐", "pinyin": "zuò", "meaning": "sit"},
      {"id": 132, "chinese": "住", "pinyin": "zhù", "meaning": "live"},
      {"id": 133, "chinese": "学习", "pinyin": "xuéxí", "meaning": "study"},
      {"id": 134, "chinese": "工作", "pinyin": "gōngzuò", "meaning": "work"},
      {"id": 135, "chinese": "下雨", "pinyin": "xiàyǔ", "meaning": "rain"},
      {"id": 136, "chinese": "爱", "pinyin": "ài", "meaning": "love"},
      {
          "id": 137,
          "chinese": "喜欢",
          "pinyin": "xǐhuān",
          "meaning": "love, like",
      },
      {"id": 138, "chinese": "想", "pinyin": "xiǎng", "meaning": "want"},
      {
          "id": 139,
          "chinese": "认识",
          "pinyin": "rènshi",
          "meaning": "know",
      },
      {
          "id": 140,
          "chinese": "会",
          "pinyin": "huì",
          "meaning": "can",
      },
      {
          "id": 141,
          "chinese": "能",
          "pinyin": "néng",
          "meaning": "can, be able to",
      },
      {"id": 142, "chinese": "好", "pinyin": "hǎo", "meaning": "good"},
      {"id": 143, "chinese": "大", "pinyin": "dà", "meaning": "big"},
      {"id": 144, "chinese": "小", "pinyin": "xiǎo", "meaning": "small"},
      {
          "id": 145,
          "chinese": "多",
          "pinyin": "duō",
          "meaning": "many, much",
      },
      {
          "id": 146,
          "chinese": "少",
          "pinyin": "shǎo",
          "meaning": "few, little",
      },
      {"id": 147, "chinese": "冷", "pinyin": "lěng", "meaning": "cold"},
      {"id": 148, "chinese": "热", "pinyin": "rè", "meaning": "hot"},
      {
          "id": 149,
          "chinese": "高兴",
          "pinyin": "gāoxìng",
          "meaning": "happy",
      },
      {
          "id": 150,
          "chinese": "漂亮",
          "pinyin": "piàoliang",
          "meaning": "beautiful",
      },
  ]

# Session states
if "fc_index" not in st.session_state:
  st.session_state.fc_index = 0
if "show_answer" not in st.session_state:
  st.session_state.show_answer = False
if "exp" not in st.session_state:
  st.session_state.exp = 0
if "level" not in st.session_state:
  st.session_state.level = 1
if "app_mode" not in st.session_state:
  st.session_state.app_mode = "Flashcards"
if "font_choice" not in st.session_state:
  st.session_state.font_choice = "KaiTi (楷体)"


def get_exp_required(lvl):
  return int(50 * (lvl**1.5))


def add_exp(amount):
  st.session_state.exp += amount
  required = get_exp_required(st.session_state.level)
  while st.session_state.exp >= required:
    st.session_state.exp -= required
    st.session_state.level += 1
    required = get_exp_required(st.session_state.level)
    st.balloons()


# -------------------------------------------------------------
# TOP HEADER BAR & DUOLINGO-LIKE PROGRESS BAR
# -------------------------------------------------------------
current_lvl = st.session_state.level
current_exp = st.session_state.exp
req_exp = get_exp_required(current_lvl)
progress_pct = min(int((current_exp / req_exp) * 100), 100)

st.markdown(
    f"""
    <div class="top-bar">
        <span style="font-weight: 700; color: #1E293B;">🏆 Level {current_lvl}</span>
        <span style="font-weight: 600; color: #64748B;">⭐ {current_exp} / {req_exp} EXP</span>
    </div>
    <div class="duo-progress-container">
        <div class="duo-progress-bar" style="width: {progress_pct}%;"></div>
    </div>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# INLINE COMPACT NAVIGATION (Replacing Sidebar)
# -------------------------------------------------------------
col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns(5)
with col_nav1:
  if st.button("📇 Cards", use_container_width=True):
    st.session_state.app_mode = "Flashcards"
    st.session_state.show_answer = False
with col_nav2:
  if st.button("📝 Quiz", use_container_width=True):
    st.session_state.app_mode = "Quiz"
with col_nav3:
  if st.button("➕ Add", use_container_width=True):
    st.session_state.app_mode = "Add"
with col_nav4:
  if st.button("🤖 AI", use_container_width=True):
    st.session_state.app_mode = "AI"
with col_nav5:
  font_label = (
      "🔤 KaiTi" if st.session_state.font_choice == "KaiTi (楷体)" else "🔤 Sans"
  )
  if st.button(font_label, use_container_width=True):
    st.session_state.font_choice = (
        "Standard"
        if st.session_state.font_choice == "KaiTi (楷体)"
        else "KaiTi (楷体)"
    )
    st.rerun()

font_class = (
    "kaiti-font" if st.session_state.font_choice == "KaiTi (楷体)" else ""
)
app_mode = st.session_state.app_mode

# -------------------------------------------------------------
# 1. FLASHCARDS MODE (Chinese Front ➔ Meaning + Pinyin Back)
# -------------------------------------------------------------
if app_mode == "Flashcards":
  vocab_list = st.session_state.vocab_list
  if vocab_list:
    if st.session_state.fc_index >= len(vocab_list):
      st.session_state.fc_index = 0
    current_card = vocab_list[st.session_state.fc_index]

    if not st.session_state.show_answer:
      st.markdown(
          f"""
                <div class="compact-card">
                    <div class="chinese-text {font_class}">{current_card['chinese']}</div>
                </div>
            """,
          unsafe_allow_html=True,
      )
      if st.button("🔄 Flip Card", use_container_width=True):
        st.session_state.show_answer = True
        st.rerun()
    else:
      st.markdown(
          f"""
                <div class="compact-card">
                    <div class="meaning-text">{current_card['meaning']}</div>
                    <div class="pinyin-text">{current_card['pinyin']}</div>
                </div>
            """,
          unsafe_allow_html=True,
      )

      b1, b2, b3, b4 = st.columns(4)

      def next_card(exp_gain):
        add_exp(exp_gain)
        st.session_state.show_answer = False
        st.session_state.fc_index = (
            st.session_state.fc_index + 1
        ) % len(vocab_list)
        st.rerun()

      with b1:
        if st.button("🔴 Again (+5)", use_container_width=True):
          next_card(5)
      with b2:
        if st.button("🟠 Hard (+10)", use_container_width=True):
          next_card(10)
      with b3:
        if st.button("🟢 Good (+15)", use_container_width=True):
          next_card(15)
      with b4:
        if st.button("⭐ Easy (+20)", use_container_width=True):
          next_card(20)

# -------------------------------------------------------------
# 2. MULTIPLE CHOICE QUIZ MODE
# -------------------------------------------------------------
elif app_mode == "Quiz":
  if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

  if (
      st.button("⚡ New Question", type="primary")
      or st.session_state.quiz_data is None
  ):
    vocab = st.session_state.vocab_list
    if len(vocab) >= 4:
      correct_word = random.choice(vocab)
      distractors = random.sample(
          [w for w in vocab if w["id"] != correct_word["id"]], 3
      )
      options = distractors + [correct_word]
      random.shuffle(options)
      quiz_type = random.choice(["cn_to_meaning", "meaning_to_cn"])
      st.session_state.quiz_data = {
          "correct": correct_word,
          "options": options,
          "type": quiz_type,
      }
      st.rerun()

  if st.session_state.quiz_data:
    q = st.session_state.quiz_data
    correct = q["correct"]

    if q["type"] == "cn_to_meaning":
      st.markdown(
          f"""
                <div class="compact-card" style="min-height: 150px; padding: 20px;">
                    <div style="font-size: 0.9rem; color: #64748B;">What is the meaning & pinyin of:</div>
                    <div class="chinese-text {font_class}" style="font-size: 3rem !important;">{correct['chinese']}</div>
                </div>
            """,
          unsafe_allow_html=True,
      )
    else:
      st.markdown(
          f"""
                <div class="compact-card" style="min-height: 150px; padding: 20px;">
                    <div style="font-size: 0.9rem; color: #64748B;">Select character for:</div>
                    <div class="meaning-text" style="font-size: 1.5rem !important;">{correct['meaning']} ({correct['pinyin']})</div>
                </div>
            """,
          unsafe_allow_html=True,
      )

    c1, c2 = st.columns(2)
    for i, opt in enumerate(q["options"]):
      col = c1 if i % 2 == 0 else c2
      label = (
          f"{opt['meaning']} ({opt['pinyin']})"
          if q["type"] == "cn_to_meaning"
          else f"{opt['chinese']}"
      )
      with col:
        if st.button(label, key=f"q_opt_{i}", use_container_width=True):
          if opt["id"] == correct["id"]:
            add_exp(25)
            st.success("Correct! 🎉 (+25 EXP)")
          else:
            ans = (
                f"{correct['meaning']} ({correct['pinyin']})"
                if q["type"] == "cn_to_meaning"
                else correct["chinese"]
            )
            st.error(f"Incorrect. Answer: {ans}")

# -------------------------------------------------------------
# 3. ADD NEW WORDS
# -------------------------------------------------------------
elif app_mode == "Add":
  st.markdown("### ➕ Add Custom Word")
  with st.form("add_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
      nc = st.text_input("Chinese", placeholder="咖啡")
    with col2:
      np = st.text_input("Pinyin", placeholder="kāfēi")
    with col3:
      nm = st.text_input("Meaning", placeholder="coffee")
    sub = st.form_submit_button("Add Word (+10 EXP)", use_container_width=True)
    if sub:
      if nc and np and nm:
        nid = (
            max([w["id"] for w in st.session_state.vocab_list]) + 1
            if st.session_state.vocab_list
            else 1
        )
        st.session_state.vocab_list.append(
            {"id": nid, "chinese": nc, "pinyin": np, "meaning": nm}
        )
        add_exp(10)
        st.success(f"Added {nc} successfully!")
      else:
        st.error("Please fill all fields.")

# -------------------------------------------------------------
# 4. AI TUTOR (GEMINI ASSISTANT)
# -------------------------------------------------------------
elif app_mode == "AI":
  st.markdown("### 🤖 Gemini AI Tutor")
  api_key = st.text_input(
      "Gemini API Key:", type="password", placeholder="Enter key..."
  )
  if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    if "messages" not in st.session_state:
      st.session_state.messages = [{
          "role": "assistant",
          "content": "Hello! Ask me any HSK 1 question.",
      }]

    for m in st.session_state.messages[-2:]:  # Keep compact view
      st.write(f"**{m['role'].capitalize()}**: {m['content']}")

    prompt = st.text_input("Ask question:", placeholder="e.g. How to use 的?")
    if prompt:
      st.session_state.messages.append({"role": "user", "content": prompt})
      try:
        res = model.generate_content(
            f"You are an HSK 1 Mandarin tutor. Answer concisely: {prompt}"
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": res.text}
        )
        st.rerun()
      except Exception as e:
        st.error(f"Error: {e}")
  else:
    st.info("Enter your Gemini API key above to chat with the AI tutor.")
