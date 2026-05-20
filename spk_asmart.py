"""
╔══════════════════════════════════════════════════════════════════════════╗
║  SPK ASMART — Sistem Pendukung Keputusan Terapi Obat Multi-Penyakit     ║
║  Adaptive Simple Multi-Attribute Rating Technique                        ║
║                                                                          ║
║  Dataset yang digunakan (3 dataset):                                     ║
║   1. drugs_side_effects_drugs_com.csv   → database obat utama            ║
║   2. personalized_medication_dataset.csv → validasi efektivitas & pasien ║
║   3. medicine_dataset.csv               → substitute, chemical class,    ║
║                                           efek samping terperinci        ║
║                                                                          ║
║  Jalankan: streamlit run spk_asmart.py                                   ║
║  Install : pip install streamlit pandas plotly                           ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ══════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="SPK ASMART | Terapi Obat",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════
#  GLOBAL CSS  —  Dark Premium Medical Theme
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
  --bg:        #080d16;
  --surf:      #0f1623;
  --surf2:     #162032;
  --border:    #1e2d44;
  --teal:      #2dd4bf;
  --teal-d:    #0f766e;
  --pink:      #f472b6;
  --pink-d:    #9d174d;
  --blue:      #60a5fa;
  --blue-d:    #1e40af;
  --amber:     #fbbf24;
  --amber-d:   #92400e;
  --purple:    #c084fc;
  --purple-d:  #581c87;
  --emerald:   #34d399;
  --text:      #e2e8f0;
  --muted:     #64748b;
  --muted2:    #94a3b8;
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  background: var(--bg) !important;
  color: var(--text) !important;
}
h1,h2,h3,h4 {
  font-family: 'DM Serif Display', serif !important;
  color: var(--text) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0b1220 0%, #080d16 100%) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] label {
  color: var(--muted2) !important;
  font-size: 0.8rem !important;
}

/* Metric cards */
[data-testid="metric-container"] {
  background: var(--surf) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  padding: 16px 20px !important;
  position: relative; overflow: hidden;
}
[data-testid="metric-container"]::after {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--teal), var(--pink));
}
[data-testid="metric-container"] label {
  color: var(--muted) !important;
  font-size: 0.72rem !important;
  text-transform: uppercase; letter-spacing: .09em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  font-family: 'DM Serif Display', serif !important;
  color: var(--teal) !important;
  font-size: 1.55rem !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.83rem !important;
  letter-spacing: .05em !important;
  color: var(--muted2) !important;
}
.stTabs [aria-selected="true"] {
  color: var(--teal) !important;
}

/* Buttons */
.stButton > button {
  border-radius: 10px !important;
  font-weight: 700 !important;
  letter-spacing: .04em;
  transition: all .18s;
}
.stButton > button:hover { transform: translateY(-2px); }

/* Expander */
.stExpander {
  background: var(--surf) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}

/* ── Custom cards ───────────────────────────────── */
.card {
  background: var(--surf);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px 24px;
  margin-bottom: 14px;
  position: relative; overflow: hidden;
}
.c-teal   { border-left: 4px solid var(--teal); }
.c-pink   { border-left: 4px solid var(--pink); }
.c-blue   { border-left: 4px solid var(--blue); }
.c-amber  { border-left: 4px solid var(--amber); }
.c-purple { border-left: 4px solid var(--purple); }
.c-em     { border-left: 4px solid var(--emerald); }

/* ── Hero gradient bar ──────────────────────────── */
.grad-bar {
  height: 3px;
  background: linear-gradient(90deg, var(--teal), var(--pink), var(--blue));
  border-radius: 999px;
  margin: 10px 0 24px;
}

/* ── Section headers ────────────────────────────── */
.sh {
  border-radius: 12px;
  padding: 14px 18px;
  margin: 20px 0 14px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.sh-teal   { background: linear-gradient(135deg,#031c1a,#042f2b); border: 1px solid #2dd4bf44; }
.sh-pink   { background: linear-gradient(135deg,#1f0a14,#3b0a25); border: 1px solid #f472b644; }
.sh-blue   { background: linear-gradient(135deg,#0a1428,#0c1e3d); border: 1px solid #60a5fa44; }
.sh-amber  { background: linear-gradient(135deg,#1a0f00,#2d1a00); border: 1px solid #fbbf2444; }
.sh-purple { background: linear-gradient(135deg,#130a20,#1e1030); border: 1px solid #c084fc44; }
.sh-em     { background: linear-gradient(135deg,#03150f,#052e1a); border: 1px solid #34d39944; }

/* ── Formula blocks ─────────────────────────────── */
.formula-wrap {
  background: #04090f;
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 22px 26px;
  margin: 12px 0 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88rem;
  line-height: 2.0;
  overflow-x: auto;
}
.ftitle {
  font-size: 0.68rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  font-weight: 700;
  padding-bottom: 10px;
  margin-bottom: 14px;
  border-bottom: 1px solid var(--border);
}
.fmain  { font-size: 1.08rem; font-weight: 700; margin: 8px 0; text-align: center; }
.fsub   { margin: 4px 0 4px 16px; }
.fnote  { margin: 3px 0 3px 16px; font-size: .8rem; font-style: italic; }
.fsec   { margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--border); }

.ft  { color: var(--teal); }
.fp  { color: var(--pink); }
.fb  { color: var(--blue); }
.fa  { color: var(--amber); }
.fpu { color: var(--purple); }
.fe  { color: var(--emerald); }
.fw  { color: var(--text); }
.fm  { color: var(--muted); }

/* ── Badges ─────────────────────────────────────── */
.badge {
  display: inline-block;
  padding: 4px 11px;
  border-radius: 20px;
  font-size: 0.71rem;
  font-weight: 700;
  letter-spacing: .04em;
  margin: 2px;
}
.bt { background: #042f2b; color: var(--teal); }
.bp { background: #3b0a25; color: var(--pink); }
.bb { background: #0c1e3d; color: var(--blue); }
.ba { background: #2d1a00; color: var(--amber); }
.bpu{ background: #1e1030; color: var(--purple); }
.be { background: #052e1a; color: var(--emerald); }

/* ── Confidence bar ──────────────────────────────── */
.cbar-bg   { background: var(--surf2); border-radius:999px; height:8px; overflow:hidden; margin:4px 0; }
.cbar-fill { height:100%; border-radius:999px; }

/* ── Winner cards ────────────────────────────────── */
.wcard {
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 10px;
  transition: transform .2s ease;
  position: relative; overflow: hidden;
}
.wcard:hover { transform: translateY(-3px); }
.wc1 { background: linear-gradient(135deg,#031c1a,#052e26); border: 2px solid var(--teal); }
.wc2 { background: linear-gradient(135deg,#1f0a14,#380a22); border: 2px solid var(--pink); }
.wc3 { background: linear-gradient(135deg,#0a1428,#0c2040); border: 2px solid var(--blue); }

/* ── Info / Warn boxes ───────────────────────────── */
.info-box  { background:#0a1428; border:1px solid var(--blue); border-radius:12px;
             padding:14px 18px; margin:12px 0; font-size:.86rem; }
.warn-box  { background:#1a0f00; border:1px solid var(--amber); border-radius:12px;
             padding:14px 18px; margin:12px 0; font-size:.86rem; }
.teal-box  { background:#031c1a; border:1px solid var(--teal); border-radius:12px;
             padding:14px 18px; margin:12px 0; font-size:.86rem; }
.pink-box  { background:#1f0a14; border:1px solid var(--pink); border-radius:12px;
             padding:14px 18px; margin:12px 0; font-size:.86rem; }
.purple-box{ background:#130a20; border:1px solid var(--purple); border-radius:12px;
             padding:14px 18px; margin:12px 0; font-size:.86rem; }

/* ── Lifestyle tip ───────────────────────────────── */
.tip-row {
  display: flex; gap: 12px; align-items: flex-start;
  background: var(--surf2); border-radius: 10px; padding: 12px 14px;
  margin-bottom: 8px; border: 1px solid var(--border);
}
.tip-icon { font-size: 1.35rem; flex-shrink: 0; margin-top: 1px; }

/* ── Ref card ────────────────────────────────────── */
.ref-card {
  background: var(--surf);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px 16px;
  margin-bottom: 8px;
  font-size: .84rem;
}

/* ── Dataset pill ────────────────────────────────── */
.ds-pill {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 14px; border-radius: 20px;
  font-size: .75rem; font-weight: 700; margin: 3px;
}
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════

def sh(icon, title, sub, c="teal"):
    clr_map = {"teal":"var(--teal)","pink":"var(--pink)","blue":"var(--blue)",
                "amber":"var(--amber)","purple":"var(--purple)","em":"var(--emerald)"}
    clr = clr_map.get(c, "var(--teal)")
    return f"""<div class="sh sh-{c}">
      <span style="font-size:1.4rem">{icon}</span>
      <div>
        <div style="font-family:'DM Serif Display',serif;color:{clr};
                    font-size:1.02rem;margin:0">{title}</div>
        <div style="font-size:.73rem;color:var(--muted);margin-top:2px">{sub}</div>
      </div>
    </div>"""


# ══════════════════════════════════════════════════════
#  KONSTANTA
# ══════════════════════════════════════════════════════

SEVERE_KW = [
    "death","fatal","severe","life-threatening","bleeding","kidney failure",
    "liver failure","coma","seizure","stroke","heart attack","anaphylaxis",
    "rhabdomyolysis","pancreatitis","suicidal","hallucin","agranulocytosis",
]
MODERATE_KW = [
    "swelling","rash","dizziness","headache","nausea","vomiting","diarrhea",
    "pain","insomnia","fatigue","muscle","liver","hypoglycemia","hyperkalemia",
    "bradycardia","edema","constipation","flushing","palpitation",
]

DOSE_MAP = {
    "angiotensin converting enzyme inhibitors": 1,
    "angiotensin-converting enzyme (ace) inhibitors": 1,
    "angiotensin receptor blockers(arb)": 1,
    "angiotensin receptor blockers": 1,
    "thiazide diuretics": 1,
    "low-ceiling diuretics": 1,
    "loop diuretics": 2,
    "high-ceiling diuretics": 2,
    "potassium- sparing diuretics": 1,
    "cardioselective beta blockers": 1,
    "beta blocker- cardioselective": 1,
    "non-cardioselective beta blockers": 2,
    "beta blocker- non selective": 2,
    "calcium channel blockers": 1,
    "calcium channel blockers- dihydropyridines": 1,
    "calcium channel blockers- nondihydropyridines": 2,
    "ace inhibitors with thiazides": 1,
    "non-sulfonylureas": 2,
    "biguanides": 2,
    "sglt-2 inhibitors": 1,
    "sglt2 inhibitors": 1,
    "incretin mimetics": 1,
    "dipeptidyl peptidase 4 inhibitors": 1,
    "dpp-4 inhibitors": 1,
    "sulfonylureas": 1,
    "sulfonylureas (insulin secretogogues)": 1,
    "antidiabetic combinations": 2,
    "insulins": 2,
    "hmg coa inhibitors (statins)": 1,
    "statins": 1,
    "cholesterol absorption inhibitors": 1,
    "pcsk9 inhibitors": 1,
    "fibric acid derivatives": 2,
    "bile acid sequestrants": 3,
    "niacin derivatives": 3,
    "thiazolidinedione": 1,
    "meglitinides": 2,
    "alpha-glucosidase inhibitors": 3,
}

PRICE_MAP = {
    "hmg coa inhibitors (statins)": 50_000,
    "statins": 50_000,
    "angiotensin converting enzyme inhibitors": 40_000,
    "angiotensin-converting enzyme (ace) inhibitors": 40_000,
    "angiotensin receptor blockers(arb)": 80_000,
    "angiotensin receptor blockers": 80_000,
    "thiazide diuretics": 20_000,
    "low-ceiling diuretics": 20_000,
    "loop diuretics": 25_000,
    "high-ceiling diuretics": 25_000,
    "potassium- sparing diuretics": 30_000,
    "cardioselective beta blockers": 55_000,
    "beta blocker- cardioselective": 55_000,
    "non-cardioselective beta blockers": 50_000,
    "beta blocker- non selective": 50_000,
    "calcium channel blockers": 45_000,
    "calcium channel blockers- dihydropyridines": 45_000,
    "calcium channel blockers- nondihydropyridines": 60_000,
    "ace inhibitors with thiazides": 45_000,
    "biguanides": 35_000,
    "non-sulfonylureas": 35_000,
    "sglt-2 inhibitors": 350_000,
    "sglt2 inhibitors": 350_000,
    "incretin mimetics": 600_000,
    "dipeptidyl peptidase 4 inhibitors": 200_000,
    "dpp-4 inhibitors": 200_000,
    "sulfonylureas": 30_000,
    "sulfonylureas (insulin secretogogues)": 30_000,
    "antidiabetic combinations": 180_000,
    "insulins": 150_000,
    "cholesterol absorption inhibitors": 120_000,
    "pcsk9 inhibitors": 1_200_000,
    "fibric acid derivatives": 60_000,
    "bile acid sequestrants": 90_000,
    "niacin derivatives": 70_000,
    "thiazolidinedione": 120_000,
    "meglitinides": 80_000,
    "alpha-glucosidase inhibitors": 40_000,
}

CONTRA = {
    "Hamil / Menyusui": {"preg_cats": ["D","X"]},
    "Gagal Ginjal (CKD)": {
        "class_block": ["non-sulfonylureas","sglt-2 inhibitors","sglt2 inhibitors",
                        "ace inhibitors with thiazides","biguanides"],
    },
    "Gagal Jantung (CHF)": {
        "class_block": ["non-cardioselective beta blockers","beta blocker- non selective",
                        "calcium channel blockers- nondihydropyridines"],
    },
    "Asma / PPOK": {
        "class_block": ["non-cardioselective beta blockers","beta blocker- non selective"],
    },
    "Hiperkalemia": {
        "class_block": ["angiotensin converting enzyme inhibitors",
                        "angiotensin-converting enzyme (ace) inhibitors",
                        "angiotensin receptor blockers","angiotensin receptor blockers(arb)",
                        "potassium- sparing diuretics"],
    },
    "Gout / Hiperurisemia": {
        "class_block": ["thiazide diuretics","low-ceiling diuretics",
                        "loop diuretics","high-ceiling diuretics"],
    },
}


# ══════════════════════════════════════════════════════
#  FUNGSI PREPROCESSING
# ══════════════════════════════════════════════════════

def severity_score_text(text: str) -> float:
    """Hitung severity dari teks bebas (drugs.com)."""
    if not isinstance(text, str): return 3.0
    t = text.lower()
    s = sum(1 for kw in SEVERE_KW   if kw in t)
    m = sum(1 for kw in MODERATE_KW if kw in t)
    return round(min(10.0, s * 2.4 + m * 0.35), 2)

def severity_score_columns(row, se_cols) -> float:
    """Hitung severity dari kolom sideEffect0..41 (medicine_dataset)."""
    all_effects = " ".join(
        str(row[c]).lower() for c in se_cols
        if pd.notna(row.get(c)) and str(row.get(c)).strip() not in ("nan","")
    )
    if not all_effects.strip():
        return 3.0
    # Jumlah efek samping sebagai indikator kasar
    count = sum(1 for c in se_cols
                if pd.notna(row.get(c)) and str(row.get(c)).strip() not in ("nan",""))
    s = sum(1 for kw in SEVERE_KW   if kw in all_effects)
    m = sum(1 for kw in MODERATE_KW if kw in all_effects)
    base = s * 2.4 + m * 0.35
    # Tambah penalti jumlah efek
    count_penalty = min(count * 0.15, 2.0)
    return round(min(10.0, base + count_penalty), 2)

def activity_to_pct(val) -> float:
    if pd.isna(val): return 50.0
    try: return float(str(val).replace("%","").strip())
    except: return 50.0

def get_dose_freq(dc: str) -> int:
    if not isinstance(dc, str): return 2
    lo = dc.lower()
    for cls, f in DOSE_MAP.items():
        if cls in lo: return f
    return 2

def get_price(dc: str) -> int:
    if not isinstance(dc, str): return 100_000
    lo = dc.lower()
    for cls, p in PRICE_MAP.items():
        if cls in lo: return p
    return 100_000

def dose_convenience(freq: int) -> int:
    return {1: 90, 2: 60, 3: 30}.get(freq, 45)

def is_contra(row, conds: list) -> bool:
    for c in conds:
        rules = CONTRA.get(c, {})
        if "preg_cats" in rules:
            if str(row.get("pregnancy_category","")) in rules["preg_cats"]:
                return True
        if "class_block" in rules:
            dc = str(row.get("drug_classes","")).lower()
            for blk in rules["class_block"]:
                if blk in dc: return True
    return False


# ══════════════════════════════════════════════════════
#  DATA LOADING — 3 DATASET
# ══════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def load_all():
    """
    ══════════════════════════════════════════════════════
    INTEGRASI 3 DATASET — Penjelasan Detail
    ══════════════════════════════════════════════════════

    Dataset 1: drugs_side_effects_drugs_com.csv
    ─────────────────────────────────────────────
    Sumber   : Drugs.com via Kaggle
    Isi      : 2.931 obat dari 47 kondisi medis
    Digunakan: Basis utama — nama obat, kelas farmakologi,
               rating pengguna, persentase aktivitas obat,
               teks efek samping, dan kategori kehamilan.
    Kolom kunci yang dipakai:
      • drug_name          → Identitas obat
      • medical_condition  → Filter per penyakit target
      • drug_classes       → Peta ke frekuensi dosis & harga
      • activity           → Efikasi (C1) dalam persen
      • side_effects       → Teks bebas → severity_score (C3)
      • rating             → Kontribusi ke Confidence Score
      • pregnancy_category → Filter kontraindikasi kehamilan

    Dataset 2: personalized_medication_dataset.csv
    ─────────────────────────────────────────────
    Sumber   : Kaggle (sintetis — 1.000 pasien)
    Isi      : Rekam medis sintetis dengan kondisi kronis,
               alergi, efektivitas terapi, efek samping.
    Digunakan: Validasi & statistik distribusi pasien.
               Juga sebagai sumber "Treatment_Effectiveness"
               untuk menambah bobot confidence score.
               Kolom penting: Age, Chronic_Conditions,
               Treatment_Effectiveness, Adverse_Reactions,
               Recovery_Time_Days.

    Dataset 3: medicine_dataset.csv
    ─────────────────────────────────────────────
    Sumber   : Kaggle (248.218 obat India/global)
    Isi      : Nama obat, daftar substitusi (5 kolom),
               efek samping terperinci (42 kolom terpisah),
               kelas terapeutik, kelas kimia, kelas aksi.
    Digunakan: Dua fungsi utama dalam sistem ini:
      1. Pengayaan data efek samping (severity lebih presisi
         karena efek samping dalam kolom terpisah, bukan
         teks bebas), dicocokan via drug name fuzzy match
         ke kelas obat yang sama (Action Class).
      2. Daftar SUBSTITUSI OBAT — setelah obat terpilih,
         sistem menampilkan opsi substitusi dari dataset
         ini untuk memberikan alternatif pilihan.
      Kolom kunci: name, sideEffect0..41, substitute0..4,
                   Action Class, Therapeutic Class.
    ══════════════════════════════════════════════════════
    """
    base = Path(__file__).parent

    # ── Dataset 1: drugs.com ──────────────────────────
    raw  = pd.read_csv(base / "drugs_side_effects_drugs_com.csv")

    # ── Dataset 2: personalized ───────────────────────
    pers = pd.read_csv(base / "personalized_medication_dataset.csv")

    # ── Dataset 3: medicine_dataset ───────────────────
    med  = pd.read_csv(base / "medicine_dataset.csv", low_memory=False)
    med = med[med["Therapeutic Class"].isin(["CARDIAC", "ANTI DIABETIC"])]

    # Kolom efek samping medicine_dataset
    SE_COLS = [f"sideEffect{i}" for i in range(42)]

    # Bangun lookup: Action Class → severity rata-rata dari Dataset 3
    # Ini memperkaya severity score C3 dengan data granular (42 kolom SE)
    action_class_severity = {}
    for ac, grp in med.groupby("Action Class"):
        if pd.isna(ac): continue
        scores = [severity_score_columns(row, SE_COLS) for _, row in grp.iterrows()]
        action_class_severity[str(ac).lower()] = round(
            sum(scores) / len(scores), 2) if scores else 3.0

    # Bangun lookup: nama obat → daftar substitusi dari Dataset 3
    sub_cols = ["substitute0","substitute1","substitute2","substitute3","substitute4"]
    med["name_lower"] = med["name"].str.lower().str.strip()
    substitute_lookup = {}
    for _, row in med.iterrows():
        key = row["name_lower"]
        subs = [str(row[c]).strip() for c in sub_cols
                if pd.notna(row.get(c)) and str(row.get(c)).strip() not in ("nan","")]
        if subs:
            substitute_lookup[key] = subs

    # Bangun lookup: Action Class → Chemical Class (informasi tambahan)
    chem_class_map = (
        med.dropna(subset=["Action Class","Chemical Class"])
           .groupby("Action Class")["Chemical Class"]
           .first()
           .to_dict()
    )

    # Pemetaan Action Class medicine_dataset → kata kunci drug_classes drugs.com
    ACTION_TO_DRUGSCOM = {
        "hmg coa inhibitors (statins)":                        "statin",
        "angiotensin receptor blockers(arb)":                  "angiotensin receptor blockers",
        "beta blocker- cardioselective":                       "cardioselective beta blockers",
        "calcium channel blockers- dihydropyridines (dhp)":    "calcium channel blockers",
        "angiotensin-converting enzyme (ace) inhibitors":      "angiotensin converting enzyme inhibitors",
        "beta blocker- non selective":                         "non-cardioselective beta blockers",
        "high-ceiling diuretics (inhibitors of na+-k+- 2cl cotransport)": "loop diuretics",
        "low-ceiling diuretics (inhibitors of na+cl symport)": "thiazide diuretics",
        "potassium- sparing diuretics":                        "potassium-sparing",
        "biguanides":                                          "non-sulfonylureas",
        "sulfonylureas (insulin secretogogues)":               "sulfonylureas",
        "dpp-4 inhibitors":                                    "dipeptidyl peptidase 4 inhibitors",
        "sglt2 inhibitors":                                    "sglt-2 inhibitors",
        "insulin secretogogues: glp-1 agonists":               "incretin mimetics",
        "thiazolidinedione(ppar gamma agonist)":               "antidiabetic combinations",
    }

    # ── Proses tiap penyakit ──────────────────────────
    targets = {
        "Hipertensi":                  "Hypertension",
        "Diabetes Melitus Tipe 2":     "Diabetes (Type 2)",
        "Kolesterol (Hiperlipidemia)": "Cholesterol",
    }
    dbs = {}

    for label, eng in targets.items():
        df = raw[raw["medical_condition"] == eng].copy()

        # C1 Efikasi dari Dataset 1
        df["efikasi"] = df["activity"].apply(activity_to_pct)

        # C3 Efek Samping: gabungkan Dataset 1 (teks) + Dataset 3 (granular per kelas)
        df["efek_samping_ds1"] = df["side_effects"].apply(severity_score_text)

        def enrich_severity(row):
            """
            Pengayaan C3: ambil severity dari Dataset 3 jika kelas aksinya ada,
            lalu rata-ratakan dengan Dataset 1 (60:40 weight) untuk hasil lebih akurat.
            Jika Dataset 3 tidak punya data untuk kelas ini, pakai Dataset 1 saja.
            """
            dc_lower = str(row.get("drug_classes","")).lower()
            best_ds3 = None
            for ac_key, dc_kw in ACTION_TO_DRUGSCOM.items():
                if dc_kw in dc_lower and ac_key in action_class_severity:
                    best_ds3 = action_class_severity[ac_key]
                    break
            if best_ds3 is not None:
                # Rata-rata tertimbang: 60% Dataset 1, 40% Dataset 3
                return round(0.60 * row["efek_samping_ds1"] + 0.40 * best_ds3, 2)
            return row["efek_samping_ds1"]

        df["efek_samping"] = df.apply(enrich_severity, axis=1)

        # Dosis & harga dari mapping kelas
        df["dosis_freq"]  = df["drug_classes"].apply(get_dose_freq)
        df["dosis_score"] = df["dosis_freq"].apply(dose_convenience)
        df["harga"]       = df["drug_classes"].apply(get_price)

        # Rating & ulasan dari Dataset 1
        df["rating"]        = pd.to_numeric(df["rating"],      errors="coerce").fillna(5.0)
        df["no_of_reviews"] = pd.to_numeric(df["no_of_reviews"],errors="coerce").fillna(1.0)

        # Substitusi dari Dataset 3 (cocokan nama obat)
        def get_subs(name):
            return substitute_lookup.get(str(name).lower().strip(), [])
        df["substitutes"] = df["drug_name"].apply(get_subs)

        # Sumber data severity (untuk transparansi)
        def severity_source(row):
            dc_lower = str(row.get("drug_classes","")).lower()
            for ac_key, dc_kw in ACTION_TO_DRUGSCOM.items():
                if dc_kw in dc_lower and ac_key in action_class_severity:
                    return "DS1 + DS3 (gabungan)"
            return "DS1 (drugs.com)"
        df["severity_source"] = df.apply(severity_source, axis=1)

        dbs[label] = df.reset_index(drop=True)

    # Statistik dari Dataset 2 (pers) untuk referensi
    effectiveness_stats = pers["Treatment_Effectiveness"].value_counts().to_dict()
    adverse_pct = (pers["Adverse_Reactions"] == "Yes").mean() * 100

    return dbs, pers, action_class_severity, substitute_lookup, effectiveness_stats, adverse_pct

# Load semua data
dbs, pers_df, ac_severity, sub_lookup, eff_stats, adv_pct = load_all()


# ══════════════════════════════════════════════════════
#  ASMART ENGINE
# ══════════════════════════════════════════════════════

def adaptive_weights(age: int, is_poor: bool, elderly_risk: bool) -> dict:
    """Tahap 1 — Bobot Adaptif W_j."""
    W = {"efikasi": 40, "dosis": 20, "efek_samping": 25, "harga": 15}
    if age > 60 or elderly_risk:
        W["efek_samping"] += 20; W["efikasi"] -= 10
        W["dosis"]        -=  5; W["harga"]   -=  5
    if is_poor:
        W["harga"]       += 25; W["efikasi"]      -= 10
        W["dosis"]        -=  5; W["efek_samping"] -= 10
    return W

def normalize_w(W: dict) -> dict:
    """Tahap 3 — w_j = W_j / Σ W_j."""
    total = sum(W.values())
    return {k: round(v / total, 6) for k, v in W.items()}

def utility(series: pd.Series, is_cost: bool) -> pd.Series:
    """Tahap 4 — Normalisasi utility 0–100."""
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series([50.0] * len(series), index=series.index)
    if is_cost:
        return 100 * (hi - series) / (hi - lo)
    return 100 * (series - lo) / (hi - lo)

def confidence_score(row) -> float:
    """
    Confidence Score = gabungan 3 dimensi:
      70% → V_i / 100             (kekuatan algoritmik ASMART)
      20% → rating / 10           (validasi pengguna nyata, Dataset 1)
      10% → min(reviews/500, 1)   (dukungan volume data)
    """
    vi      = float(row["V_i"]) / 100.0
    rating  = min(float(row.get("rating", 5.0)), 10.0) / 10.0
    reviews = min(float(row.get("no_of_reviews", 1.0)) / 500.0, 1.0)
    return round((0.70 * vi + 0.20 * rating + 0.10 * reviews) * 100, 1)

def run_asmart(disease, age, is_poor, elderly_risk, contra_conds, top_n=10):
    df = dbs[disease].copy()

    # Tahap 2: Hard constraint
    mask   = df.apply(lambda r: is_contra(r, contra_conds), axis=1)
    elim   = df[mask].copy()
    df     = df[~mask].copy()
    if df.empty:
        return pd.DataFrame(), {}, {}, elim

    W_raw  = adaptive_weights(age, is_poor, elderly_risk)
    W_norm = normalize_w(W_raw)

    df["u_efikasi"]      = utility(df["efikasi"],      is_cost=False)
    df["u_dosis"]        = utility(df["dosis_score"],  is_cost=False)
    df["u_efek_samping"] = utility(df["efek_samping"], is_cost=True)
    df["u_harga"]        = utility(df["harga"],        is_cost=True)

    df["V_i"] = (
        W_norm["efikasi"]      * df["u_efikasi"]      +
        W_norm["dosis"]        * df["u_dosis"]         +
        W_norm["efek_samping"] * df["u_efek_samping"]  +
        W_norm["harga"]        * df["u_harga"]
    ).round(4)

    df = df.sort_values("V_i", ascending=False).head(top_n).reset_index(drop=True)
    df["Rank"]       = df.index + 1
    df["Confidence"] = df.apply(confidence_score, axis=1)

    return df, W_raw, W_norm, elim


# ══════════════════════════════════════════════════════
#  SARAN GAYA HIDUP
# ══════════════════════════════════════════════════════
LIFESTYLE = {
    "Hipertensi": {
        "icon": "❤️", "target_label": "Tekanan Darah",
        "target_val": "< 130/80 mmHg (AHA/ACC 2023)",
        "quote": "Tekanan darah terkontrol hari ini adalah investasi umur panjang esok hari.",
        "diet": [
            ("🧂","Batasi natrium < 2.300 mg/hari — setara 1 sendok teh garam. Hindari makanan kemasan, keripik, dan saus instan."),
            ("🫐","Perbanyak kalium: pisang, alpukat, bayam, kentang rebus — kalium menetralkan efek natrium pada tekanan darah."),
            ("🐟","Omega-3 dari ikan (salmon, sarden, kembung) 2–3×/minggu terbukti menurunkan sistolik."),
            ("🥦","Pola makan DASH (Dietary Approaches to Stop Hypertension): kaya buah, sayuran, biji-bijian, rendah lemak jenuh."),
        ],
        "olahraga": [
            ("🚶","Jalan cepat 30 menit/hari, 5 hari/minggu — paling efektif menurunkan tekanan darah secara non-farmakologis."),
            ("🏊","Renang atau bersepeda: aerobik berdampak rendah, ideal untuk pasien dengan risiko kardiovaskular."),
            ("🧘","Yoga & meditasi: menurunkan sistolik 4–5 mmHg melalui aktivasi saraf parasimpatik."),
            ("⚠️","Hindari Valsalva maneuver (menahan napas saat angkat beban berat) tanpa pengawasan."),
        ],
        "gaya_hidup": [
            ("😴","Tidur 7–8 jam/malam — sleep apnea dan defisit tidur kronik meningkatkan tekanan darah signifikan."),
            ("🚭","Berhenti merokok — nikotin menyempitkan pembuluh darah dan meningkatkan risiko stroke."),
            ("⚖️","Turunkan berat badan: setiap ↓1 kg = ↓1 mmHg tekanan darah secara rata-rata."),
            ("📏","Pantau tekanan darah di rumah 2×/hari (pagi & malam), catat untuk ditunjukkan ke dokter."),
        ],
        "monitoring": [
            ("🩺","Kontrol rutin setiap 1–3 bulan; target < 130/80 mmHg."),
            ("🧪","Cek fungsi ginjal (kreatinin, GFR) & elektrolit tahunan — obat antihipertensi memengaruhi keduanya."),
            ("❤️","EKG berkala jika ada riwayat gangguan jantung atau menggunakan beta-blocker."),
        ],
        "targets": [
            ("Tekanan Darah (Umum)","< 130/80 mmHg","AHA/ACC 2023"),
            ("Tekanan Darah (Lansia > 65 thn)","< 140/90 mmHg","AHA/ACC 2023"),
            ("BMI Ideal (Standar Asia)","18.5 – 22.9","KalbeMed / WHO Asia-Pacific"),
            ("Asupan Natrium","< 2.300 mg/hari","AHA 2021"),
            ("Aktivitas Fisik","≥ 150 menit/minggu aerobik","AHA 2023"),
        ],
    },
    "Diabetes Melitus Tipe 2": {
        "icon": "🩸", "target_label": "HbA1c",
        "target_val": "< 7.0% (ADA 2023)",
        "quote": "Gula darah terkontrol hari ini adalah perlindungan organ 10 tahun ke depan.",
        "diet": [
            ("🌾","Pilih karbohidrat indeks glikemik rendah: beras merah, oat, quinoa, ubi jalar — serat memperlambat absorpsi gula."),
            ("🥗","Pola 'Piring Sehat': ½ piring sayuran non-tepung, ¼ protein, ¼ karbohidrat kompleks (rekomendasi ADA 2023)."),
            ("🍗","Protein tanpa lemak (ayam, tahu, tempe, kacang) membantu kenyang tanpa lonjakan gula."),
            ("🚫","Hindari minuman manis: 1 kaleng soda mengandung ±39 gr gula, setara ~4 sendok makan gula pasir."),
        ],
        "olahraga": [
            ("🚶","150 menit/minggu aerobik sedang menurunkan HbA1c rata-rata 0.6% (Cochrane meta-analisis)."),
            ("🏋️","Latihan resistensi 2–3×/minggu membangun massa otot → meningkatkan sensitivitas insulin secara permanen."),
            ("⏰","Berdiri atau jalan 5 menit setiap 30 menit duduk — terbukti menurunkan gula darah post-makan."),
            ("📉","Monitor gula darah sebelum & sesudah olahraga — waspadai hipoglikemia jika menggunakan sulfonilurea/insulin."),
        ],
        "gaya_hidup": [
            ("😴","Tidur 7–9 jam — kurang tidur menurunkan sensitivitas insulin dan meningkatkan kortisol."),
            ("🧠","Manajemen stres aktif — kortisol kronik merangsang produksi glukosa di hati (glukoneogenesis)."),
            ("🦶","Periksa kaki setiap hari — neuropati diabetik membuat luka tidak terasa, infeksi bisa sangat serius."),
            ("🦷","Jaga kebersihan mulut — periodontitis dan diabetes saling memperburuk secara dua arah."),
        ],
        "monitoring": [
            ("🩸","Cek gula darah mandiri sesuai anjuran dokter; target GDP 80–130 mg/dL."),
            ("🧪","HbA1c setiap 3 bulan hingga target, lalu tiap 6 bulan."),
            ("👁️","Funduskopi tahunan untuk deteksi dini retinopati diabetik."),
            ("🫀","Profil lipid tahunan — diabetes meningkatkan risiko penyakit kardiovaskular 2–4×."),
        ],
        "targets": [
            ("HbA1c (Dewasa)","< 7.0%","ADA 2023"),
            ("HbA1c (Lansia)","< 7.5 – 8.0%","ADA 2023"),
            ("Gula Darah Puasa","80 – 130 mg/dL","ADA 2023"),
            ("Gula Darah 2 jam PP","< 180 mg/dL","ADA 2023"),
            ("Tekanan Darah","< 130/80 mmHg","ADA 2023"),
        ],
    },
    "Kolesterol (Hiperlipidemia)": {
        "icon": "🫀", "target_label": "LDL",
        "target_val": "< 100 mg/dL (risiko sedang) atau < 70 mg/dL (risiko tinggi)",
        "quote": "Kolesterol sehat berarti arteri bersih dan jantung yang kuat seumur hidup.",
        "diet": [
            ("🥑","Lemak tak jenuh tunggal (alpukat, minyak zaitun, kacang almond) menurunkan LDL tanpa mengurangi HDL."),
            ("🐟","Omega-3 dari ikan laut dalam 2–3×/minggu atau suplemen menurunkan trigliserida hingga 30%."),
            ("🌾","Serat larut (oat, kacang hitam, apel) membentuk gel di usus yang mengikat kolesterol sebelum diserap."),
            ("🚫","Kurangi lemak jenuh (mentega, santan, daging merah berlemak) — setiap 1% kalori dari lemak jenuh = LDL ↑2 mg/dL."),
        ],
        "olahraga": [
            ("🚴","Aerobik 30–60 menit/hari meningkatkan HDL 3–9% dan menurunkan trigliserida."),
            ("🏃","HIIT (High-Intensity Interval Training) ringan lebih efektif meningkatkan HDL dibanding olahraga konstan."),
            ("🎯","Target minimum: 150 menit/minggu intensitas sedang atau 75 menit intensitas tinggi (ACC/AHA 2019)."),
        ],
        "gaya_hidup": [
            ("🚭","Berhenti merokok — merokok menurunkan HDL dan merusak lapisan pembuluh darah, mempercepat aterosklerosis."),
            ("⚖️","Penurunan BB 5–10% pada pasien overweight dapat menurunkan LDL 15–20 mg/dL."),
            ("🍷","Batasi alkohol — konsumsi berlebihan meningkatkan trigliserida dan tekanan darah."),
            ("🧘","Kelola stres — kortisol merangsang produksi kolesterol di hati."),
        ],
        "monitoring": [
            ("🧪","Profil lipid lengkap (LDL, HDL, trigliserida, total) setiap 6–12 bulan."),
            ("🔬","Uji fungsi hati (SGOT, SGPT) berkala jika menggunakan statin — waspadai miopati."),
            ("💊","Jangan hentikan statin mendadak — dapat memicu rebound inflamasi kardiovaskular."),
            ("🩺","Target LDL: < 100 (risiko sedang), < 70 mg/dL (risiko tinggi/CVD)."),
        ],
        "targets": [
            ("LDL (Risiko Rendah)","< 130 mg/dL","ACC/AHA 2019"),
            ("LDL (Risiko Sedang)","< 100 mg/dL","ACC/AHA 2019"),
            ("LDL (Risiko Tinggi/CVD)","< 70 mg/dL","ACC/AHA 2019"),
            ("HDL (Pria)","≥ 40 mg/dL","ACC/AHA 2019"),
            ("HDL (Wanita)","≥ 50 mg/dL","ACC/AHA 2019"),
            ("Trigliserida","< 150 mg/dL","ACC/AHA 2019"),
        ],
    },
}


# ══════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:16px 0 22px">
      <div style="font-size:2.4rem">🩺</div>
      <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;font-weight:700;
                  background:linear-gradient(135deg,#2dd4bf,#f472b6);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  background-clip:text;margin-top:4px">SPK ASMART</div>
      <div style="font-size:.68rem;color:#475569;letter-spacing:.13em;
                  text-transform:uppercase;margin-top:3px">Terapi Obat Multi-Penyakit</div>
    </div>
    <div style="height:2px;background:linear-gradient(90deg,#2dd4bf,#f472b6);
                border-radius:999px;margin-bottom:18px"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:.77rem;color:#2dd4bf;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">🧬 Penyakit Target</div>', unsafe_allow_html=True)
    disease = st.selectbox("Penyakit", list(dbs.keys()), label_visibility="collapsed")

    st.markdown('<div style="font-size:.77rem;color:#60a5fa;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin:12px 0 6px">👤 Profil Pasien</div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca: age    = st.number_input("Usia (thn)", 10, 95, 45, step=1)
    with cb: gender = st.selectbox("Kelamin", ["Pria","Wanita","Lainnya"])
    cc, cd = st.columns(2)
    with cc: weight = st.number_input("BB (kg)", 30, 200, 65)
    with cd: height = st.number_input("TB (cm)", 100, 220, 165)

    bmi = weight / ((height / 100) ** 2)
    # Klasifikasi BMI Standar Asia / Indonesia (KalbeMed)
    if bmi < 18.5:
        bmi_cat   = "Kurang (Underweight)"
        bmi_color = "#60a5fa"
    elif bmi < 23.0:
        bmi_cat   = "Normal"
        bmi_color = "#2dd4bf"
    elif bmi < 25.0:
        bmi_cat   = "Kelebihan BB (Overweight)"
        bmi_color = "#fbbf24"
    elif bmi < 30.0:
        bmi_cat   = "Obesitas Tingkat I"
        bmi_color = "#f97316"
    else:
        bmi_cat   = "Obesitas Tingkat II"
        bmi_color = "#f472b6"
    bmi_short = {
        "Kurang (Underweight)":      "Underweight",
        "Normal":                    "Normal",
        "Kelebihan BB (Overweight)": "Overweight",
        "Obesitas Tingkat I":        "Obesitas I",
        "Obesitas Tingkat II":       "Obesitas II",
    }.get(bmi_cat, bmi_cat)
    st.markdown(f"""
    <div style="background:var(--surf2);border:1px solid var(--border);border-radius:10px;
                padding:10px 14px;text-align:center;margin:4px 0 12px">
      <span style="font-size:1.25rem;font-weight:800;color:{bmi_color}">{bmi:.1f}</span>
      <span style="font-size:.74rem;color:var(--muted);margin-left:6px">BMI · {bmi_short}</span>
      <div style="font-size:.65rem;color:var(--muted);margin-top:2px">Standar Asia/Indonesia</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:.77rem;color:#f472b6;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin:4px 0 6px">⛔ Kontraindikasi / Komorbid</div>', unsafe_allow_html=True)
    contra_conds = st.multiselect("Kondisi", list(CONTRA.keys()), label_visibility="collapsed")

    st.markdown('<div style="font-size:.77rem;color:#fbbf24;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin:12px 0 6px">💰 Faktor Lain</div>', unsafe_allow_html=True)
    is_poor      = st.checkbox("Pasien Kurang Mampu / BPJS PBI")
    elderly_risk = st.checkbox("Risiko Geriatri (Fragilitas)")

    st.markdown('<div style="font-size:.77rem;color:#c084fc;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin:12px 0 6px">🔢 Parameter</div>', unsafe_allow_html=True)
    top_n = st.slider("Top-N Obat Ditampilkan", 5, 20, 10)

    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("⚡  Jalankan Analisis ASMART", use_container_width=True, type="primary")

    st.markdown("""
    <hr style="border-color:#1e2d44;margin:16px 0 10px">
    <div style="font-size:.67rem;color:#334155;text-align:center;line-height:1.75">
      <span style="color:#2dd4bf;font-weight:700">Dataset 1</span> · drugs_side_effects_drugs_com.csv<br>
      <span style="color:#f472b6;font-weight:700">Dataset 2</span> · personalized_medication_dataset.csv<br>
      <span style="color:#60a5fa;font-weight:700">Dataset 3</span> · medicine_dataset.csv<br><br>
      ⚠️ Alat bantu akademis — bukan pengganti dokter.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  HERO HEADER
# ══════════════════════════════════════════════════════
DISEASE_ICON = {
    "Hipertensi": "❤️",
    "Diabetes Melitus Tipe 2": "🩸",
    "Kolesterol (Hiperlipidemia)": "🫀",
}
DISEASE_SUB = {
    "Hipertensi":                  "Pemilihan terapi antihipertensi adaptif berdasarkan profil klinis dan sosioekonomik",
    "Diabetes Melitus Tipe 2":     "Rekomendasi obat antidiabetik oral & injeksi berbasis bukti klinis",
    "Kolesterol (Hiperlipidemia)": "Pemilihan terapi penurun lipid yang dipersonalisasi per pasien",
}

st.markdown(f"""
<div style="padding:24px 0 8px">
  <div style="font-family:'DM Serif Display',serif;font-size:2.2rem;color:#e2e8f0;line-height:1.2">
    {DISEASE_ICON.get(disease,"💊")} Sistem Pendukung Keputusan
    <span style="background:linear-gradient(135deg,#2dd4bf,#f472b6);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 background-clip:text">Terapi Obat</span>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px">
    <span style="padding:4px 14px;border-radius:20px;font-size:.73rem;font-weight:700;
                 background:#042f2b;color:#2dd4bf;border:1px solid #2dd4bf44">METODE ASMART</span>
    <span style="padding:4px 14px;border-radius:20px;font-size:.73rem;font-weight:700;
                 background:#3b0a25;color:#f472b6;border:1px solid #f472b644">ADAPTIVE WEIGHTS</span>
    <span style="padding:4px 14px;border-radius:20px;font-size:.73rem;font-weight:700;
                 background:#0c1e3d;color:#60a5fa;border:1px solid #60a5fa44">3 DATASET TERINTEGRASI</span>
    <span style="padding:4px 14px;border-radius:20px;font-size:.73rem;font-weight:700;
                 background:#2d1a00;color:#fbbf24;border:1px solid #fbbf2444">CONFIDENCE SCORE</span>
  </div>
  <p style="color:#475569;font-size:.88rem;margin-top:10px">
    {DISEASE_SUB.get(disease,"")} — menggunakan
    <em>Adaptive Simple Multi-Attribute Rating Technique</em>
  </p>
</div>
<div class="grad-bar"></div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════
t1, t2, t3, t4, t5 = st.tabs([
    "📊  Hasil & Rekomendasi",
    "📐  Metodologi & Rumus",
    "🔬  Transparansi Hitung",
    "💚  Saran Gaya Hidup",
    "📚  Dataset & Referensi",
])


# ══════════════════════════════════════════════════════
#  TAB 1 — HASIL & REKOMENDASI
# ══════════════════════════════════════════════════════
with t1:
    if not run:
        st.markdown("""
        <div class="card" style="text-align:center;padding:56px 20px;border-style:dashed">
          <div style="font-size:3.2rem;margin-bottom:14px">🏥</div>
          <div style="font-family:'DM Serif Display',serif;font-size:1.5rem;
               background:linear-gradient(135deg,#2dd4bf,#f472b6);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text">Siap Menganalisis</div>
          <p style="color:#475569;margin:10px 0 0;font-size:.88rem">
            Lengkapi profil pasien di sidebar, lalu klik<br>
            <strong style="color:#2dd4bf">⚡ Jalankan Analisis ASMART</strong>
          </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Menjalankan ASMART Engine — 3 dataset…"):
            result, W_raw, W_norm, elim = run_asmart(
                disease, age, is_poor, elderly_risk, contra_conds, top_n)

        if result.empty:
            st.error("❌ Semua obat dieliminasi oleh filter kontraindikasi. Kurangi kondisi.")
            st.stop()

        total_db = len(dbs[disease])
        elim_n   = len(elim)

        # ── KPI ──────────────────────────────────────────
        k1,k2,k3,k4 = st.columns(4)
        with k1: st.metric("Total Database", total_db)
        with k2: st.metric("Lolos Filter", total_db - elim_n)
        with k3: st.metric("Dieliminasi", elim_n,
                           delta=f"-{elim_n}" if elim_n else "0", delta_color="inverse")
        with k4: st.metric(f"Top-{top_n} Tampil", len(result))

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Profil pasien ─────────────────────────────────
        st.markdown(sh("👤","Ringkasan Profil Pasien","Data yang digunakan engine ASMART","teal"),
                    unsafe_allow_html=True)
        gi = "👨" if gender=="Pria" else "👩"
        profil_tags = []
        if age > 60 or elderly_risk: profil_tags.append('<span class="badge bt">👴 Lansia/Geriatri</span>')
        if is_poor:  profil_tags.append('<span class="badge ba">💰 Kurang Mampu</span>')
        if contra_conds: profil_tags.append(f'<span class="badge bp">⛔ {len(contra_conds)} Kontraindikasi</span>')
        if not profil_tags: profil_tags.append('<span class="badge be">✅ Tidak Ada Faktor Khusus</span>')

        st.markdown(f"""
        <div class="card c-teal">
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px">
            <div style="background:var(--surf2);border-radius:10px;padding:12px;border:1px solid var(--border)">
              <div style="font-size:.7rem;color:var(--muted);text-transform:uppercase">{gi} Kelamin</div>
              <div style="font-weight:700;font-size:.9rem;margin-top:3px">{gender}</div>
            </div>
            <div style="background:var(--surf2);border-radius:10px;padding:12px;border:1px solid var(--border)">
              <div style="font-size:.7rem;color:var(--muted);text-transform:uppercase">🎂 Usia</div>
              <div style="font-weight:700;font-size:.9rem;margin-top:3px">{age} Tahun</div>
            </div>
            <div style="background:var(--surf2);border-radius:10px;padding:12px;border:1px solid var(--border)">
              <div style="font-size:.7rem;color:var(--muted);text-transform:uppercase">⚖️ BMI</div>
              <div style="font-weight:700;font-size:.9rem;margin-top:3px;color:{bmi_color}">{bmi:.1f} · {bmi_cat}</div>
              <div style="font-size:.65rem;color:var(--muted)">Standar Asia/Indonesia</div>
            </div>
            <div style="background:var(--surf2);border-radius:10px;padding:12px;border:1px solid var(--border)">
              <div style="font-size:.7rem;color:var(--muted);text-transform:uppercase">🏥 Penyakit</div>
              <div style="font-weight:700;font-size:.82rem;margin-top:3px">{disease[:22]}{'…' if len(disease)>22 else ''}</div>
            </div>
          </div>
          <div style="padding-top:10px;border-top:1px solid var(--border)">
            <span style="font-size:.72rem;color:var(--muted);margin-right:6px">Faktor Khusus:</span>
            {" ".join(profil_tags)}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Bobot adaptif ─────────────────────────────────
        st.markdown(sh("⚖️","Bobot Adaptif Aktif","Berubah otomatis — lihat Tab Metodologi untuk logikanya","pink"),
                    unsafe_allow_html=True)

        def pct(k): return f"{W_norm[k]*100:.1f}%"
        crit_info = [
            ("Efikasi",      "C1", "Benefit", W_raw["efikasi"],     W_norm["efikasi"],     "var(--teal)"),
            ("Dosis",        "C2", "Benefit", W_raw["dosis"],       W_norm["dosis"],       "var(--blue)"),
            ("Efek Samping", "C3", "Cost",    W_raw["efek_samping"],W_norm["efek_samping"],"var(--pink)"),
            ("Harga",        "C4", "Cost",    W_raw["harga"],       W_norm["harga"],       "var(--amber)"),
        ]
        cols_w = st.columns(4)
        for col, (lbl, code, typ, raw_v, norm_v, clr) in zip(cols_w, crit_info):
            with col:
                st.markdown(f"""
                <div style="background:var(--surf2);border:1px solid var(--border);
                            border-radius:12px;padding:14px 16px;text-align:center">
                  <div style="font-size:.68rem;color:var(--muted);text-transform:uppercase;margin-bottom:6px">
                    {code} · {lbl}
                    <span style="font-size:.65rem;color:var(--muted)"> ({typ})</span>
                  </div>
                  <div style="font-size:1.6rem;font-weight:800;color:{clr};font-family:'DM Serif Display',serif">
                    {norm_v:.3f}
                  </div>
                  <div style="font-size:.72rem;color:var(--muted);margin:4px 0">W = {raw_v} → {pct(lbl.lower().replace(' ','_') if lbl!='Efek Samping' else 'efek_samping')}</div>
                  <div class="cbar-bg">
                    <div class="cbar-fill" style="width:{norm_v*100:.1f}%;background:{clr}"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        if elim_n > 0:
            elim_list = " · ".join(elim["drug_name"].head(6).str.title().tolist())
            more = f" +{elim_n-6} lainnya" if elim_n > 6 else ""
            st.markdown(f"""
            <div class="warn-box">
              ⛔ <strong>{elim_n} obat dieliminasi</strong> (hard constraint —
              kondisi: <em>{', '.join(contra_conds)}</em>)<br>
              <span style="font-size:.82rem;color:var(--muted2)">{elim_list}{more}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<hr style="border-color:var(--border);margin:22px 0">', unsafe_allow_html=True)

        # ── Top 3 medals ──────────────────────────────────
        st.markdown(sh("🏆","Top 3 Rekomendasi Terbaik","Obat dengan skor ASMART tertinggi untuk profil ini","blue"),
                    unsafe_allow_html=True)

        medals = [("🥇","wc1","var(--teal)"),("🥈","wc2","var(--pink)"),("🥉","wc3","var(--blue)")]
        mc1,mc2,mc3 = st.columns(3)
        for col, (em,wc,clr), (_, row) in zip([mc1,mc2,mc3], medals, result.head(3).iterrows()):
            conf      = float(row["Confidence"])
            conf_clr  = ("var(--teal)" if conf>=70 else "var(--amber)" if conf>=45 else "var(--pink)")
            subs      = row.get("substitutes",[])
            subs_html = ""
            if subs:
                subs_html = f'<div style="font-size:.68rem;color:var(--muted);margin-top:8px">Substitusi (DS3): {", ".join(s[:25] for s in subs[:2])}{"…" if len(subs)>2 else ""}</div>'
            with col:
                st.markdown(f"""
                <div class="wcard {wc}" style="text-align:center">
                  <div style="font-size:2rem;margin-bottom:4px">{em}</div>
                  <div style="font-size:.68rem;color:var(--muted);letter-spacing:.1em;text-transform:uppercase">
                    Peringkat #{int(row['Rank'])}
                  </div>
                  <div style="font-family:'DM Serif Display',serif;font-size:1rem;
                              color:var(--text);margin:8px 0 4px;text-transform:capitalize">
                    {row['drug_name'].title()}
                  </div>
                  <div style="font-size:.7rem;color:var(--muted);margin-bottom:12px;min-height:28px">
                    {str(row['drug_classes'])[:55]}{'…' if len(str(row['drug_classes']))>55 else ''}
                  </div>

                  <div style="margin-bottom:8px">
                    <div style="font-size:.7rem;color:var(--muted)">Skor ASMART (V_i)</div>
                    <div style="font-family:'DM Serif Display',serif;font-size:1.9rem;
                                font-weight:700;color:{clr}">{row['V_i']:.4f}</div>
                  </div>

                  <div style="margin-bottom:10px">
                    <div style="font-size:.7rem;color:var(--muted);margin-bottom:2px">
                      Confidence Score
                      <span style="font-size:.65rem"> (V_i + Rating + Data)</span>
                    </div>
                    <div class="cbar-bg">
                      <div class="cbar-fill" style="width:{conf}%;background:{conf_clr}"></div>
                    </div>
                    <div style="font-size:.8rem;font-weight:700;color:{conf_clr};margin-top:3px">
                      {conf:.1f}%
                      {'🟢' if conf>=70 else '🟡' if conf>=45 else '🔴'}
                    </div>
                  </div>

                  <div style="display:flex;flex-wrap:wrap;gap:3px;justify-content:center">
                    <span class="badge bt">⭐ {row['rating']:.1f}/10</span>
                    <span class="badge bb">💊 {int(row['dosis_freq'])}×/hari</span>
                    <span class="badge ba">Rp {int(row['harga'])//1000}rb/bln</span>
                  </div>
                  <div style="margin-top:8px;background:var(--surf);border-radius:8px;padding:7px;font-size:.72rem">
                    <span style="color:var(--teal)">Efikasi: {row['efikasi']:.0f}%</span>
                    &nbsp;|&nbsp;
                    <span style="color:var(--pink)">ES: {row['efek_samping']:.1f}/10</span>
                    &nbsp;|&nbsp;
                    <span style="font-size:.65rem;color:var(--muted)">{row['severity_source']}</span>
                  </div>
                  {subs_html}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Bar chart ─────────────────────────────────────
        st.markdown(sh("📊","Grafik Peringkat Lengkap","Skor V_i semua kandidat yang lolos filter","teal"),
                    unsafe_allow_html=True)
        fig_bar = px.bar(
            result, x="V_i",
            y=result["drug_name"].str.title() + " (#" + result["Rank"].astype(str) + ")",
            orientation="h", text="V_i",
            color="V_i",
            color_continuous_scale=[[0,"#3b0a25"],[.4,"#f472b6"],[.7,"#60a5fa"],[1,"#2dd4bf"]],
            labels={"V_i":"Skor ASMART (V_i)","y":"Nama Obat"},
        )
        fig_bar.update_traces(texttemplate="%{x:.4f}", textposition="outside",
                              textfont_size=10, marker_line_width=0)
        fig_bar.update_layout(
            plot_bgcolor="#04090f", paper_bgcolor="#0f1623",
            font_color="#e2e8f0", font_family="DM Sans",
            coloraxis_showscale=False,
            yaxis=dict(autorange="reversed", tickfont_size=10, gridcolor="#1e2d44"),
            xaxis=dict(range=[0,115], gridcolor="#1e2d44"),
            margin=dict(l=10,r=60,t=20,b=10),
            height=max(340, 38*len(result)+80),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # ── Radar ─────────────────────────────────────────
        st.markdown(sh("🕸️","Profil Utility Multi-Dimensi","Perbandingan visual Top-5 kandidat","pink"),
                    unsafe_allow_html=True)
        top5 = result.head(5)
        cats  = ["Efikasi (C1)","Kemudahan Dosis (C2)","Keamanan Efek Samping (C3)","Keterjangkauan Harga (C4)"]
        pal   = ["#2dd4bf","#f472b6","#60a5fa","#c084fc","#fbbf24"]
        fig_r = go.Figure()
        for i, (_, row) in enumerate(top5.iterrows()):
            vals = [row["u_efikasi"],row["u_dosis"],row["u_efek_samping"],row["u_harga"]]
            fig_r.add_trace(go.Scatterpolar(
                r=vals+[vals[0]], theta=cats+[cats[0]],
                fill="toself", name=row["drug_name"].title(),
                line=dict(color=pal[i], width=2),
                fillcolor=pal[i], opacity=.15,
            ))
        fig_r.update_layout(
            polar=dict(
                bgcolor="#04090f",
                radialaxis=dict(visible=True, range=[0,100],
                                tickfont_color="#475569", gridcolor="#1e2d44"),
                angularaxis=dict(tickfont_color="#94a3b8", gridcolor="#1e2d44"),
            ),
            plot_bgcolor="#0f1623", paper_bgcolor="#0f1623",
            font_color="#e2e8f0",
            legend=dict(bgcolor="#0f1623",bordercolor="#1e2d44",borderwidth=1,font_size=10),
            height=380, margin=dict(t=20,b=20),
        )
        st.plotly_chart(fig_r, use_container_width=True)

        # ── Confidence chart ──────────────────────────────
        st.markdown(sh("🎯","Confidence Score Semua Kandidat","Gabungan V_i + Rating + Volume Ulasan","amber"),
                    unsafe_allow_html=True)
        cf_df = result[["drug_name","Confidence","V_i","rating"]].copy()
        cf_df["drug_name"] = cf_df["drug_name"].str.title()
        fig_cf = px.bar(
            cf_df, x="Confidence", y="drug_name", orientation="h",
            color="Confidence",
            color_continuous_scale=[[0,"#3b0a25"],[0.45,"#92400e"],[0.7,"#fbbf24"],[1,"#2dd4bf"]],
            text="Confidence",
            labels={"Confidence":"Confidence Score (%)","drug_name":"Obat"},
        )
        fig_cf.update_traces(texttemplate="%{x:.1f}%", textposition="outside",
                             textfont_size=10, marker_line_width=0)
        fig_cf.update_layout(
            plot_bgcolor="#04090f", paper_bgcolor="#0f1623",
            font_color="#e2e8f0", coloraxis_showscale=False,
            yaxis=dict(autorange="reversed",tickfont_size=10,gridcolor="#1e2d44"),
            xaxis=dict(range=[0,115],gridcolor="#1e2d44"),
            margin=dict(l=10,r=60,t=10,b=10),
            height=max(300, 38*len(result)+80),
        )
        st.plotly_chart(fig_cf, use_container_width=True)

        # ── Tabel lengkap ─────────────────────────────────
        st.markdown(sh("📋","Tabel Lengkap Hasil Perangkingan","Semua kriteria, utility, skor, confidence, sumber severity","blue"),
                    unsafe_allow_html=True)
        tbl = result[[
            "Rank","drug_name","drug_classes",
            "efikasi","dosis_freq","efek_samping","harga",
            "u_efikasi","u_dosis","u_efek_samping","u_harga",
            "V_i","Confidence","rating","no_of_reviews","severity_source",
        ]].copy()
        tbl.columns = [
            "Rank","Nama Obat","Kelas Obat",
            "Efikasi(%)","Dosis/Hari","Efek Samping(0–10)","Harga(Rp/bln)",
            "U₁ Efikasi","U₂ Dosis","U₃ EfekSamping","U₄ Harga",
            "V_i","Confidence(%)","Rating","Ulasan","Sumber Severity",
        ]
        tbl["Nama Obat"] = tbl["Nama Obat"].str.title()
        st.dataframe(tbl, use_container_width=True, height=400, hide_index=True)

        # ── Substitusi dari Dataset 3 ─────────────────────
        best_drug = result.iloc[0]["drug_name"]
        best_subs = result.iloc[0].get("substitutes", [])
        if best_subs:
            st.markdown(sh("🔄","Obat Substitusi (dari Dataset 3)","Alternatif untuk obat rekomendasi #1 — sumber: medicine_dataset.csv","em"),
                        unsafe_allow_html=True)
            s_cols = st.columns(min(len(best_subs), 5))
            for s_col, sub_name in zip(s_cols, best_subs[:5]):
                with s_col:
                    st.markdown(f"""
                    <div style="background:var(--surf2);border:1px solid var(--border);
                                border-radius:10px;padding:12px;text-align:center;font-size:.82rem">
                      <div style="font-size:1.2rem;margin-bottom:4px">💊</div>
                      <div style="color:var(--teal);font-weight:600;text-transform:capitalize">
                        {sub_name[:30]}{'…' if len(sub_name)>30 else ''}
                      </div>
                      <div style="font-size:.68rem;color:var(--muted);margin-top:3px">Substitusi</div>
                    </div>
                    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  TAB 2 — METODOLOGI & RUMUS
# ══════════════════════════════════════════════════════
with t2:
    st.markdown("""
    <div style="font-family:'DM Serif Display',serif;font-size:1.85rem;color:#e2e8f0;
                padding-bottom:6px;margin-top:4px">
      Metodologi
      <span style="background:linear-gradient(135deg,#2dd4bf,#f472b6);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
        ASMART
      </span>
    </div>
    <p style="color:#475569;font-size:.88rem;margin-bottom:24px">
      <strong style="color:#94a3b8">Adaptive Simple Multi-Attribute Rating Technique</strong>
      — pengembangan SMART (Edwards, 1977) dengan logika adaptif bobot kriteria
      berdasarkan profil klinis dan sosioekonomik pasien secara real-time.
    </p>
    """, unsafe_allow_html=True)

    # Kriteria tabel
    crit_df = pd.DataFrame({
        "Kode":    ["C1","C2","C3","C4"],
        "Kriteria":["Efikasi / Efektivitas Obat",
                    "Kemudahan Dosis (Kepatuhan Pasien)",
                    "Risiko Efek Samping (Safety)",
                    "Harga Obat / Biaya Terapi"],
        "Jenis":   ["Benefit","Benefit","Cost","Cost"],
        "W Default":[40,20,25,15],
        "Sumber Data DS":["DS1: activity (%)",
                          "DS1: drug_classes → frekuensi",
                          "DS1: side_effects + DS3: sideEffect0-41",
                          "Mapping PRICE_MAP dari drug_classes"],
        "Keterangan":["Persen pasien yang membaik dengan obat ini",
                      "1×/hari lebih baik dari 3×/hari (kepatuhan lebih tinggi)",
                      "Severity teks + granular 42 kolom efek samping; gabungan 60:40",
                      "Estimasi biaya bulanan berdasarkan kelas farmakologi"],
    })
    st.markdown(sh("📌","Tabel Kriteria SPK","4 kriteria dengan penjelasan sumber data","teal"), unsafe_allow_html=True)
    st.dataframe(crit_df, use_container_width=True, hide_index=True)

    st.markdown('<hr style="border-color:var(--border);margin:22px 0">', unsafe_allow_html=True)
    st.markdown(sh("🔄","5 Tahap Algoritma ASMART","Alur komputasi sekuensial dari input ke ranking","blue"), unsafe_allow_html=True)

    # ── Tahap 1 ──────────────────────────────────────────
    with st.expander("① Tahap 1 — Bobot Adaptif (W_j)", expanded=True):
        st.markdown("""
        **Tujuan:** Menentukan bobot kepentingan kriteria secara otomatis sesuai profil pasien.
        Bobot *tidak statis* — itulah yang membedakan ASMART dari SMART konvensional.
        """)
        st.markdown("""
        <div class="formula-wrap">
          <div class="ftitle ft">📌 Bobot Default (W_j) — Tanpa Kondisi Khusus</div>
          <div class="fsub fw">C₁  Efikasi / Efektivitas Obat &nbsp;&nbsp;&nbsp;→&nbsp; <span class="ft">W₁ = 40</span></div>
          <div class="fsub fw">C₂  Kemudahan Dosis &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→&nbsp; <span class="ft">W₂ = 20</span></div>
          <div class="fsub fw">C₃  Risiko Efek Samping &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→&nbsp; <span class="ft">W₃ = 25</span></div>
          <div class="fsub fw">C₄  Harga Obat &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→&nbsp; <span class="ft">W₄ = 15</span></div>
          <div class="fsub fm">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;───────</div>
          <div class="fsub fw">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Σ W = <span class="ft">100</span></div>

          <div class="fsec">
            <div class="ftitle fa">⚙️ Penyesuaian — Pasien Lansia (Usia > 60) atau Risiko Geriatri</div>
            <div class="fnote fm">Prioritas: keselamatan pasien (efek samping diutamakan)</div>
            <div class="fsub fw">W₃ (Efek Samping) ← W₃ + <span class="fa">20</span></div>
            <div class="fsub fw">W₁ (Efikasi)      ← W₁ − <span class="fa">10</span></div>
            <div class="fsub fw">W₂ (Dosis)        ← W₂ − <span class="fa"> 5</span></div>
            <div class="fsub fw">W₄ (Harga)        ← W₄ − <span class="fa"> 5</span></div>
          </div>

          <div class="fsec">
            <div class="ftitle fp">⚙️ Penyesuaian — Pasien Kurang Mampu / BPJS PBI</div>
            <div class="fnote fm">Prioritas: keterjangkauan harga</div>
            <div class="fsub fw">W₄ (Harga)        ← W₄ + <span class="fp">25</span></div>
            <div class="fsub fw">W₁ (Efikasi)      ← W₁ − <span class="fp">10</span></div>
            <div class="fsub fw">W₂ (Dosis)        ← W₂ − <span class="fp"> 5</span></div>
            <div class="fsub fw">W₃ (Efek Samping) ← W₃ − <span class="fp">10</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tahap 2 ──────────────────────────────────────────
    with st.expander("② Tahap 2 — Hard Constraint (Filter Kontraindikasi)"):
        st.markdown("""
        **Tujuan:** Eliminasi obat yang **berbahaya** bagi kondisi spesifik pasien sebelum
        perhitungan dimulai. Ini adalah **keselamatan absolut** — tidak ada skor V_i yang
        dapat melampaui aturan eliminasi ini.
        """)
        st.markdown("""
        <div class="formula-wrap">
          <div class="ftitle fp">⛔ Aturan Eliminasi (Hard Constraint)</div>
          <div class="fsub fw"><span class="fp">Hamil / Menyusui</span>
               → hapus semua obat pregnancy_category = <span class="fa">D</span> atau <span class="fa">X</span></div>
          <div class="fsub fw"><span class="fp">Gagal Ginjal (CKD)</span>
               → hapus Metformin, SGLT-2, ACEi+Tiazid</div>
          <div class="fsub fw"><span class="fp">Gagal Jantung (CHF)</span>
               → hapus CCB non-DHP, Beta-blocker non-selektif</div>
          <div class="fsub fw"><span class="fp">Asma / PPOK</span>
               → hapus Beta-blocker non-selektif (risiko bronkospasme)</div>
          <div class="fsub fw"><span class="fp">Hiperkalemia</span>
               → hapus ACEi, ARB, Diuretik K-sparing</div>
          <div class="fsub fw"><span class="fp">Gout / Hiperurisemia</span>
               → hapus Tiazid, Loop Diuretik</div>
          <div class="fsec">
            <div class="fnote fa">
              Logika: IF kelas_obat ∈ daftar_terlarang[kondisi_pasien]
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;THEN obat = EXCLUDED (tidak masuk Tahap 3–5)
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tahap 3 ──────────────────────────────────────────
    with st.expander("③ Tahap 3 — Normalisasi Bobot (w_j)"):
        st.markdown("""
        **Tujuan:** Mengubah bobot mentah W_j ke nilai relatif sehingga
        **Σ w_j = 1**. Ini diperlukan agar skala perhitungan V_i konsisten di rentang 0–100.
        """)
        st.latex(r"w_j = \frac{W_j}{\displaystyle\sum_{j=1}^{n} W_j}")
        st.markdown("""
        <div class="formula-wrap">
          <div class="ftitle fb">✏️ Contoh Numerik — Profil Default (tanpa adaptasi)</div>
          <div class="fsub fw">Σ W  =  40 + 20 + 25 + 15  =  <span class="ft">100</span></div>
          <div class="fsub fw" style="margin-top:8px">w₁ (Efikasi)       =  40 / 100  =  <span class="ft">0.40</span>  <span class="fm">(40.0%)</span></div>
          <div class="fsub fw">w₂ (Dosis)         =  20 / 100  =  <span class="ft">0.20</span>  <span class="fm">(20.0%)</span></div>
          <div class="fsub fw">w₃ (Efek Samping)  =  25 / 100  =  <span class="ft">0.25</span>  <span class="fm">(25.0%)</span></div>
          <div class="fsub fw">w₄ (Harga)         =  15 / 100  =  <span class="ft">0.15</span>  <span class="fm">(15.0%)</span></div>
          <div class="fsub fm" style="margin-top:4px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;──────</div>
          <div class="fsub fw">Σ w  =  <span class="ft">1.00</span>  ✓</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tahap 4 ──────────────────────────────────────────
    with st.expander("④ Tahap 4 — Normalisasi Nilai Utility (u_ij)"):
        st.markdown("""
        **Tujuan:** Menyetarakan semua data mentah (%, Rp, frekuensi/hari) ke
        **skala seragam 0–100** menggunakan normalisasi min-max.
        """)
        ca4, cb4 = st.columns(2)
        with ca4:
            st.markdown("**Kriteria Benefit** (lebih tinggi = lebih baik)")
            st.latex(r"u_{ij} = 100 \times \frac{C_{out} - C_{min}}{C_{max} - C_{min}}")
            st.markdown("""
            <div class="formula-wrap" style="font-size:.82rem">
              <div class="ftitle ft">Digunakan untuk C1 (Efikasi) dan C2 (Dosis)</div>
              <div class="fnote fm">Contoh: Obat A, Efikasi = 87%</div>
              <div class="fsub fw">C_min = 10%,  C_max = 100%</div>
              <div class="fsub fw">u_A = 100 × (87−10)/(100−10)</div>
              <div class="fsub fw">    = 100 × 77/90 = <span class="ft">85.56</span></div>
            </div>
            """, unsafe_allow_html=True)
        with cb4:
            st.markdown("**Kriteria Cost** (lebih rendah = lebih baik)")
            st.latex(r"u_{ij} = 100 \times \frac{C_{max} - C_{out}}{C_{max} - C_{min}}")
            st.markdown("""
            <div class="formula-wrap" style="font-size:.82rem">
              <div class="ftitle fp">Digunakan untuk C3 (Efek Samping) dan C4 (Harga)</div>
              <div class="fnote fm">Contoh: Obat A, Harga = Rp 40.000</div>
              <div class="fsub fw">C_min = 20.000, C_max = 1.200.000</div>
              <div class="fsub fw">u_A = 100 × (1.200.000−40.000)/(1.200.000−20.000)</div>
              <div class="fsub fw">    = 100 × 1.160.000/1.180.000 = <span class="fp">98.31</span></div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
        <div class="formula-wrap">
          <div class="ftitle fa">⚙️ Konversi Frekuensi Dosis → Skor Kenyamanan (Benefit)</div>
          <div class="fnote fm">Frekuensi dosis diubah ke skor kenyamanan sebelum normalisasi:</div>
          <div class="fsub fw">1×/hari  →  dosis_score = <span class="ft">90</span>  <span class="fm">← sangat mudah dipatuhi</span></div>
          <div class="fsub fw">2×/hari  →  dosis_score = <span class="fa">60</span>  <span class="fm">← cukup mudah</span></div>
          <div class="fsub fw">3×/hari  →  dosis_score = <span class="fp">30</span>   <span class="fm">← risiko lupa tinggi</span></div>
          <div class="fnote fm">dosis_score diperlakukan sebagai BENEFIT → obat 1×/hari = utilitas tertinggi</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="teal-box">
          💡 <strong>Pengayaan C3 dari Dataset 3 (medicine_dataset.csv):</strong><br>
          Nilai efek samping C3 tidak hanya dari teks bebas DS1, tetapi juga digabung dengan
          severity rata-rata per kelas aksi dari DS3 (42 kolom efek samping terpisah).<br>
          <strong>Formula:</strong>  efek_samping = 0.60 × severity_DS1 + 0.40 × severity_DS3<br>
          Jika kelas aksi tidak ditemukan di DS3 → pakai DS1 saja (100%).
        </div>
        """, unsafe_allow_html=True)

    # ── Tahap 5 ──────────────────────────────────────────
    with st.expander("⑤ Tahap 5 — Skor Akhir & Perangkingan (V_i)"):
        st.markdown("""
        **Tujuan:** Setiap obat mendapat skor akhir V_i dari penjumlahan terbobot semua utilitas.
        Obat dirangking dari V_i tertinggi ke terendah.
        """)
        st.latex(r"V_i = \sum_{j=1}^{n} \left( w_j \times u_{ij} \right)")
        st.latex(r"V_i = w_1 \cdot u_{i1} + w_2 \cdot u_{i2} + w_3 \cdot u_{i3} + w_4 \cdot u_{i4}")
        st.markdown("""
        <div class="formula-wrap">
          <div class="ftitle fa">✏️ Contoh Numerik — Profil Default (w = 0.40, 0.20, 0.25, 0.15)</div>
          <div class="fnote fm">Obat A: u₁=85.6, u₂=90.0, u₃=72.4, u₄=98.3</div>
          <div class="fsub fw" style="margin-top:8px">
            V_A = (<span class="fb">0.40</span> × 85.6) + (<span class="ft">0.20</span> × 90.0) + (<span class="fp">0.25</span> × 72.4) + (<span class="fa">0.15</span> × 98.3)
          </div>
          <div class="fsub fw">
            V_A = <span class="fb">34.24</span> + <span class="ft">18.00</span> + <span class="fp">18.10</span> + <span class="fa">14.75</span>
          </div>
          <div class="fsub fw">V_A = <span class="ft" style="font-size:1.1rem;font-weight:700">85.09</span></div>
          <div class="fsec">
            <div class="fnote fm">Semua obat yang lolos Tahap 2 dihitung V_i-nya.</div>
            <div class="fnote fm">Diurutkan: V_i₁ ≥ V_i₂ ≥ … ≥ V_iₙ  →  Obat #1 = rekomendasi terbaik.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Confidence Score ──────────────────────────────────
    st.markdown('<hr style="border-color:var(--border);margin:22px 0">', unsafe_allow_html=True)
    st.markdown(sh("🎯","Confidence Score — Tingkat Keyakinan Rekomendasi",
                   "Gabungan kekuatan algoritmik + validasi pengguna + dukungan data","amber"),
                unsafe_allow_html=True)
    st.latex(r"\text{Confidence}_i = 0.70 \times \frac{V_i}{100} + 0.20 \times \frac{\text{Rating}_i}{10} + 0.10 \times \min\!\left(\frac{\text{Reviews}_i}{500},\;1\right)")
    st.markdown("""
    <div class="formula-wrap">
      <div class="ftitle fa">📊 Komponen Confidence Score</div>
      <div class="fsub fw">70% → V_i / 100              <span class="fm">← kekuatan algoritmik ASMART (Dataset 1+3)</span></div>
      <div class="fsub fw">20% → Rating / 10             <span class="fm">← validasi pengguna nyata (Dataset 1)</span></div>
      <div class="fsub fw">10% → min(Reviews/500, 1)     <span class="fm">← volume data pendukung (Dataset 1)</span></div>
      <div class="fsec">
        <div class="ftitle ft">🟢 Interpretasi</div>
        <div class="fsub fw">Confidence ≥ 70%  →  Sangat direkomendasikan</div>
        <div class="fsub fw">Confidence 45–70% →  Rekomendasikan dengan pengawasan dokter</div>
        <div class="fsub fw">Confidence &lt; 45%  →  Pertimbangkan alternatif atau konsultasi mendalam</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # SMART vs ASMART
    st.markdown('<hr style="border-color:var(--border);margin:22px 0">', unsafe_allow_html=True)
    st.markdown(sh("🔄","SMART Konvensional vs ASMART","Keunggulan pendekatan adaptif","purple"), unsafe_allow_html=True)
    comp_df = pd.DataFrame({
        "Aspek":["Bobot Kriteria","Profil Pasien","Kontraindikasi","Personalisasi","Data Efek Samping"],
        "SMART Konvensional":["Statis","Tidak dipertimbangkan","Manual oleh dokter","Tidak ada","Satu sumber teks"],
        "ASMART (Sistem Ini)":["Adaptif per pasien","Usia, geriatri, ekonomi",
                               "Hard constraint otomatis","Real-time per pasien",
                               "DS1 (teks) + DS3 (42 kolom terpisah), gabungan 60:40"],
    })
    st.dataframe(comp_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════
#  TAB 3 — TRANSPARANSI
# ══════════════════════════════════════════════════════
with t3:
    st.markdown("""
    <div style="font-family:'DM Serif Display',serif;font-size:1.85rem;color:#e2e8f0;
                padding-bottom:6px;margin-top:4px">
      Transparansi &
      <span style="background:linear-gradient(135deg,#2dd4bf,#f472b6);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
        Akuntabilitas
      </span>
    </div>
    <p style="color:#475569;font-size:.88rem;margin-bottom:20px">
      Semua langkah komputasi ditampilkan terbuka untuk validasi akademis, sidang skripsi,
      dan verifikasi pakar medis.
    </p>
    """, unsafe_allow_html=True)

    if not run:
        st.markdown('<div class="info-box">ℹ️ Jalankan analisis dari sidebar terlebih dahulu.</div>',
                    unsafe_allow_html=True)
    elif result.empty:
        st.markdown('<div class="warn-box">⚠️ Tidak ada hasil.</div>', unsafe_allow_html=True)
    else:
        # Weight breakdown
        st.markdown(sh("①","Detail Bobot Adaptif","W_j mentah → w_j ternormalisasi","teal"), unsafe_allow_html=True)
        ca3, cb3 = st.columns([1, 1.1])
        with ca3:
            wt = pd.DataFrame({
                "Kriteria":["C1 Efikasi","C2 Dosis","C3 Efek Samping","C4 Harga"],
                "Jenis":["Benefit","Benefit","Cost","Cost"],
                "W_j":   [W_raw["efikasi"],W_raw["dosis"],W_raw["efek_samping"],W_raw["harga"]],
                "w_j":   [W_norm["efikasi"],W_norm["dosis"],W_norm["efek_samping"],W_norm["harga"]],
                "Persen":[f"{W_norm[k]*100:.1f}%" for k in ["efikasi","dosis","efek_samping","harga"]],
            })
            st.dataframe(wt, hide_index=True, use_container_width=True)
        with cb3:
            fig_pie = px.pie(
                values=[W_raw["efikasi"],W_raw["dosis"],W_raw["efek_samping"],W_raw["harga"]],
                names=["C1 Efikasi","C2 Dosis","C3 Efek Samping","C4 Harga"],
                color_discrete_sequence=["#2dd4bf","#60a5fa","#f472b6","#fbbf24"],
                hole=0.42,
            )
            fig_pie.update_layout(
                paper_bgcolor="#0f1623", font_color="#e2e8f0",
                legend=dict(bgcolor="#0f1623",bordercolor="#1e2d44",borderwidth=1),
                height=240, margin=dict(t=10,b=10,l=10,r=10),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Utility matrix
        st.markdown(sh("②","Matriks Utility — Semua Kandidat","u_ij per kriteria setelah normalisasi min-max","pink"), unsafe_allow_html=True)
        full_df = dbs[disease].copy()
        mask2   = full_df.apply(lambda r: is_contra(r, contra_conds), axis=1)
        udf     = full_df[~mask2].copy()
        udf["u_efikasi"]      = utility(udf["efikasi"],     False)
        udf["u_dosis"]        = utility(udf["dosis_score"], False)
        udf["u_efek_samping"] = utility(udf["efek_samping"],True)
        udf["u_harga"]        = utility(udf["harga"],       True)
        udf["V_i_full"] = (
            W_norm["efikasi"]*udf["u_efikasi"] + W_norm["dosis"]*udf["u_dosis"] +
            W_norm["efek_samping"]*udf["u_efek_samping"] + W_norm["harga"]*udf["u_harga"]
        ).round(4)
        ushw = udf[["drug_name","efikasi","dosis_freq","efek_samping","harga",
                    "u_efikasi","u_dosis","u_efek_samping","u_harga","V_i_full","severity_source"]].copy()
        ushw.columns = ["Nama Obat","Efikasi(%)","Dosis/Hari","Efek Samping","Harga(Rp)",
                        "U₁ Efikasi","U₂ Dosis","U₃ Efek Samping","U₄ Harga","V_i","Sumber SE"]
        for c in ["U₁ Efikasi","U₂ Dosis","U₃ Efek Samping","U₄ Harga"]:
            ushw[c] = ushw[c].round(2)
        ushw["Nama Obat"] = ushw["Nama Obat"].str.title()
        ushw = ushw.sort_values("V_i",ascending=False).reset_index(drop=True)
        st.dataframe(ushw, use_container_width=True, height=360, hide_index=True)

        # Step by step V_i
        st.markdown(sh("③","Rincian Perhitungan V_i per Obat","Kontribusi w_j × u_ij per kriteria","blue"), unsafe_allow_html=True)
        cr = []
        for _, row in result.iterrows():
            c1=round(W_norm["efikasi"]*row["u_efikasi"],4)
            c2=round(W_norm["dosis"]*row["u_dosis"],4)
            c3=round(W_norm["efek_samping"]*row["u_efek_samping"],4)
            c4=round(W_norm["harga"]*row["u_harga"],4)
            cr.append({
                "Rank":int(row["Rank"]),"Nama Obat":row["drug_name"].title(),
                "w₁·u₁ (C1)":c1,"w₂·u₂ (C2)":c2,"w₃·u₃ (C3)":c3,"w₄·u₄ (C4)":c4,
                "V_i":row["V_i"],"Confidence(%)":row["Confidence"],
                "Ekspresi":f"{W_norm['efikasi']:.3f}×{row['u_efikasi']:.1f}+{W_norm['dosis']:.3f}×{row['u_dosis']:.1f}+{W_norm['efek_samping']:.3f}×{row['u_efek_samping']:.1f}+{W_norm['harga']:.3f}×{row['u_harga']:.1f}",
            })
        st.dataframe(pd.DataFrame(cr), use_container_width=True, height=380, hide_index=True)

        # Stacked bar
        st.markdown(sh("④","Dekomposisi Kontribusi Kriteria","Stacked bar — berapa persen tiap kriteria berkontribusi ke V_i","amber"), unsafe_allow_html=True)
        stk = []
        for _,row in result.head(10).iterrows():
            stk.append({"Obat":row["drug_name"].title(),
                        "C1 Efikasi":round(W_norm["efikasi"]*row["u_efikasi"],2),
                        "C2 Dosis":round(W_norm["dosis"]*row["u_dosis"],2),
                        "C3 Efek Samping":round(W_norm["efek_samping"]*row["u_efek_samping"],2),
                        "C4 Harga":round(W_norm["harga"]*row["u_harga"],2)})
        stk_df = pd.DataFrame(stk)
        fig3 = go.Figure()
        for crit,clr in [("C1 Efikasi","#2dd4bf"),("C2 Dosis","#60a5fa"),
                         ("C3 Efek Samping","#f472b6"),("C4 Harga","#fbbf24")]:
            fig3.add_trace(go.Bar(name=crit,y=stk_df["Obat"],x=stk_df[crit],
                                  orientation="h",marker_color=clr))
        fig3.update_layout(
            barmode="stack", plot_bgcolor="#04090f", paper_bgcolor="#0f1623",
            font_color="#e2e8f0",
            legend=dict(bgcolor="#0f1623",bordercolor="#1e2d44",borderwidth=1,
                        orientation="h",yanchor="bottom",y=1.02),
            yaxis=dict(autorange="reversed",tickfont_size=10,gridcolor="#1e2d44"),
            xaxis=dict(gridcolor="#1e2d44"),
            height=max(300, 38*min(10,len(result))+100),
            margin=dict(l=10,r=20,t=50,b=10),
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Heatmap
        st.markdown(sh("⑤","Heatmap Matriks Utility","Visualisasi nilai u_ij — merah rendah, hijau tinggi","em"), unsafe_allow_html=True)
        hm = result[["drug_name","u_efikasi","u_dosis","u_efek_samping","u_harga"]].copy()
        hm["drug_name"] = hm["drug_name"].str.title()
        hm = hm.set_index("drug_name")
        hm.columns = ["C1 Efikasi","C2 Dosis","C3 Efek Samping","C4 Harga"]
        fig_hm = px.imshow(hm, text_auto=".1f",
                           color_continuous_scale=[[0,"#3b0a25"],[.5,"#1a0f00"],[1,"#042f2b"]],
                           aspect="auto")
        fig_hm.update_layout(
            paper_bgcolor="#0f1623", font_color="#e2e8f0",
            coloraxis_showscale=True,
            height=max(280, 32*len(result)+80),
            margin=dict(l=10,r=10,t=10,b=10),
        )
        st.plotly_chart(fig_hm, use_container_width=True)


# ══════════════════════════════════════════════════════
#  TAB 4 — SARAN GAYA HIDUP
# ══════════════════════════════════════════════════════
with t4:
    ls = LIFESTYLE.get(disease, LIFESTYLE["Hipertensi"])
    st.markdown(f"""
    <div style="font-family:'DM Serif Display',serif;font-size:1.85rem;color:#e2e8f0;
                padding-bottom:6px;margin-top:4px">
      {ls['icon']} Saran Gaya Hidup
      <span style="background:linear-gradient(135deg,#2dd4bf,#f472b6);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
        — {disease}
      </span>
    </div>
    <p style="color:#475569;font-size:.88rem;margin-bottom:8px">
      Terapi obat bekerja optimal dikombinasikan perubahan gaya hidup.
      Panduan ini berdasarkan <strong style="color:#94a3b8">JNC 8, ADA 2023, ACC/AHA 2019</strong>.
    </p>
    """, unsafe_allow_html=True)

    if run and not result.empty:
        best_drug = result.iloc[0]["drug_name"].title()
        conf_best = result.iloc[0]["Confidence"]
        cf_clr = "#2dd4bf" if conf_best>=70 else "#fbbf24" if conf_best>=45 else "#f472b6"
        st.markdown(f"""
        <div class="teal-box" style="margin-bottom:20px">
          💊 Berdasarkan analisis ASMART, rekomendasi #1 untuk profil Anda adalah
          <strong style="color:#2dd4bf">{best_drug}</strong>
          dengan Confidence Score
          <strong style="color:{cf_clr}">{conf_best:.1f}%</strong>.
          Kombinasikan dengan saran di bawah untuk hasil optimal.
        </div>
        """, unsafe_allow_html=True)

    ca4l, cb4l = st.columns(2)
    with ca4l:
        st.markdown(sh("🥗","Pola Makan & Nutrisi","","teal"), unsafe_allow_html=True)
        for icon, tip in ls.get("diet",[]):
            st.markdown(f'<div class="tip-row"><div class="tip-icon">{icon}</div><div style="font-size:.85rem;color:#cbd5e1;line-height:1.55">{tip}</div></div>', unsafe_allow_html=True)

        st.markdown(sh("🏃","Aktivitas Fisik & Olahraga","","blue"), unsafe_allow_html=True)
        for icon, tip in ls.get("olahraga",[]):
            st.markdown(f'<div class="tip-row"><div class="tip-icon">{icon}</div><div style="font-size:.85rem;color:#cbd5e1;line-height:1.55">{tip}</div></div>', unsafe_allow_html=True)

    with cb4l:
        st.markdown(sh("🧘","Gaya Hidup & Kebiasaan","","amber"), unsafe_allow_html=True)
        for icon, tip in ls.get("gaya_hidup",[]):
            st.markdown(f'<div class="tip-row"><div class="tip-icon">{icon}</div><div style="font-size:.85rem;color:#cbd5e1;line-height:1.55">{tip}</div></div>', unsafe_allow_html=True)

        st.markdown(sh("🩺","Monitoring & Kontrol Rutin","","pink"), unsafe_allow_html=True)
        for icon, tip in ls.get("monitoring",[]):
            st.markdown(f'<div class="tip-row"><div class="tip-icon">{icon}</div><div style="font-size:.85rem;color:#cbd5e1;line-height:1.55">{tip}</div></div>', unsafe_allow_html=True)

    # Target klinis
    st.markdown('<hr style="border-color:var(--border);margin:22px 0">', unsafe_allow_html=True)
    st.markdown(sh("🎯","Target Klinis Berdasarkan Panduan Terkini","","em"), unsafe_allow_html=True)
    t_df = pd.DataFrame(ls.get("targets",[]), columns=["Parameter","Target","Referensi"])
    st.dataframe(t_df, use_container_width=True, hide_index=True)

    # Tabel klasifikasi BMI Asia
    st.markdown('<hr style="border-color:var(--border);margin:22px 0">', unsafe_allow_html=True)
    st.markdown(sh("⚖️","Klasifikasi BMI — Standar Asia/Indonesia","Sumber: KalbeMed / WHO Asia-Pacific 2000","amber"), unsafe_allow_html=True)

    bmi_tiers = [
        ("< 18.5",        "Kurang (Underweight)",          "Risiko kurang gizi, osteoporosis, imun menurun",         "#60a5fa"),
        ("18.5 – 22.9",   "Normal",                        "Risiko penyakit metabolik paling rendah",                "#2dd4bf"),
        ("23.0 – 24.9",   "Kelebihan BB (Overweight)",     "Risiko mulai meningkat; perlu pemantauan",               "#fbbf24"),
        ("25.0 – 29.9",   "Obesitas Tingkat I",            "Risiko tinggi: hipertensi, DM, dislipidemia",            "#f97316"),
        ("≥ 30.0",        "Obesitas Tingkat II",           "Risiko sangat tinggi; intervensi medis dianjurkan",      "#f472b6"),
    ]

    bmi_cols = st.columns(5)
    for col, (rentang, label, risiko, clr) in zip(bmi_cols, bmi_tiers):
        is_current = (
            (rentang == "< 18.5"      and bmi < 18.5) or
            (rentang == "18.5 – 22.9" and 18.5 <= bmi < 23.0) or
            (rentang == "23.0 – 24.9" and 23.0 <= bmi < 25.0) or
            (rentang == "25.0 – 29.9" and 25.0 <= bmi < 30.0) or
            (rentang == "≥ 30.0"      and bmi >= 30.0)
        )
        border_style = f"3px solid {clr}" if is_current else f"1px solid {clr}44"
        glow = f"box-shadow:0 0 12px {clr}44;" if is_current else ""
        badge_html = '<div style="font-size:.68rem;font-weight:700;color:#0f1623;background:{};border-radius:6px;padding:2px 8px;margin-top:4px;display:inline-block">ANDA</div>'.format(clr) if is_current else ""
        with col:
            st.markdown(f"""
            <div style="background:var(--surf2);border:{border_style};border-radius:12px;
                        padding:14px 12px;text-align:center;{glow}">
              <div style="font-size:.7rem;color:{clr};font-weight:700;margin-bottom:6px">{rentang}</div>
              <div style="font-size:.78rem;font-weight:700;color:#e2e8f0;line-height:1.3;min-height:36px">{label}</div>
              <div style="font-size:.68rem;color:var(--muted);margin-top:6px;line-height:1.4">{risiko}</div>
              {badge_html}
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:var(--surf2);border:1px solid var(--border);border-radius:10px;
                padding:12px 16px;margin:12px 0;font-size:.84rem;display:flex;align-items:center;gap:12px">
      <span style="font-size:1.6rem">⚖️</span>
      <div>
        <strong style="color:#e2e8f0">BMI Anda saat ini: </strong>
        <span style="font-size:1.1rem;font-weight:800;color:{bmi_color}">{bmi:.1f}</span>
        <span style="margin-left:8px;padding:3px 10px;background:{bmi_color}22;color:{bmi_color};
                     border-radius:20px;font-size:.75rem;font-weight:700;border:1px solid {bmi_color}55">
          {bmi_cat}
        </span>
        <div style="font-size:.75rem;color:var(--muted);margin-top:4px">
          Standar Asia / Indonesia (KalbeMed · WHO Asia-Pacific 2000)
          — berbeda dengan standar WHO global yang batas overweight di ≥ 25.0
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="border-color:var(--border);margin:22px 0">', unsafe_allow_html=True)
    st.markdown(sh("👤","Saran Personal Berdasarkan Profil Anda","","purple"), unsafe_allow_html=True)

    tips_p = []
    if age > 60 or elderly_risk:
        tips_p.append(("👴","Pasien lansia: prioritaskan obat dosis tunggal (1×/hari) dengan efek samping minimal. Waspadai polifarmasi — tunjukkan semua obat yang dikonsumsi kepada dokter."))
    if bmi >= 30.0:
        tips_p.append(("⚖️",f"BMI Anda {bmi:.1f} termasuk <strong>Obesitas Tingkat II</strong> (standar Asia/Indonesia). Penurunan BB 5–10% dapat memperbaiki kondisi {disease} secara signifikan bahkan tanpa penambahan obat."))
    elif bmi >= 25.0:
        tips_p.append(("⚖️",f"BMI Anda {bmi:.1f} termasuk <strong>Obesitas Tingkat I</strong> (standar Asia/Indonesia, normal: 18.5–22.9). Target penurunan BB bertahap dengan defisit kalori 300–500 kkal/hari."))
    elif bmi >= 23.0:
        tips_p.append(("⚖️",f"BMI Anda {bmi:.1f} termasuk <strong>Kelebihan Berat Badan (Overweight)</strong> (standar Asia: ≥23.0). Jaga pola makan dan tingkatkan aktivitas fisik untuk mencapai BMI 18.5–22.9."))
    if is_poor:
        tips_p.append(("💊","Manfaatkan program JKN/BPJS. Obat generik berkualitas setara paten tersedia di Faskes tingkat 1 — minta resep generik dari dokter."))
    if gender == "Wanita" and age >= 40:
        tips_p.append(("🌸","Wanita perimenopause: perubahan hormonal dapat memperburuk tekanan darah dan profil lipid — diskusikan dengan dokter kandungan."))
    if not tips_p:
        tips_p.append(("✅","Profil Anda tidak memiliki risiko tambahan yang teridentifikasi. Tetap patuhi terapi dan jadwal kontrol rutin."))

    for icon, tip in tips_p:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#042f2b,#130a20);border:1px solid #2dd4bf44;
                    border-radius:12px;padding:14px 16px;margin-bottom:8px;
                    display:flex;gap:12px;align-items:flex-start">
          <div style="font-size:1.4rem;flex-shrink:0">{icon}</div>
          <div style="font-size:.88rem;color:#e2e8f0;line-height:1.55;font-weight:500">{tip}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="purple-box" style="margin-top:16px">
      💜 <strong style="color:#c084fc">Semangat Pantang Menyerah</strong><br>
      <span style="color:#e2e8f0;line-height:1.7">
        {ls['quote']}<br><br>
        Menjalani terapi jangka panjang memang tidak mudah, tetapi setiap langkah kecil membawa Anda
        lebih dekat pada kualitas hidup yang lebih baik.
        <strong style="color:#2dd4bf">Anda tidak sendirian</strong> — tim medis dan keluarga hadir mendukung Anda. 💪
      </span>
    </div>
    <div class="warn-box">
      ⚠️ <strong>Disclaimer Medis:</strong> Rekomendasi ini adalah output sistem pendukung keputusan akademis
      dan <strong>tidak menggantikan konsultasi dokter.</strong>
      Semua keputusan terapi wajib diverifikasi oleh tenaga medis berlisensi.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  TAB 5 — DATASET & REFERENSI
# ══════════════════════════════════════════════════════
with t5:
    st.markdown("""
    <div style="font-family:'DM Serif Display',serif;font-size:1.85rem;color:#e2e8f0;
                padding-bottom:6px;margin-top:4px">
      Dataset &
      <span style="background:linear-gradient(135deg,#2dd4bf,#f472b6);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
        Referensi Ilmiah
      </span>
    </div>
    """, unsafe_allow_html=True)

    # ── 3 Dataset cards ───────────────────────────────────
    st.markdown(sh("🗄️","Integrasi 3 Dataset — Penjelasan Lengkap","Bagaimana setiap dataset berkontribusi ke sistem SPK ini","teal"),
                unsafe_allow_html=True)

    ds_tab1, ds_tab2, ds_tab3 = st.tabs([
        "📗 DS1 — drugs_side_effects",
        "📘 DS2 — personalized_medication",
        "📙 DS3 — medicine_dataset",
    ])

    with ds_tab1:
        st.markdown("""
        <div class="card c-teal">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
            <span style="font-size:1.8rem">📗</span>
            <div>
              <div style="font-weight:700;color:#2dd4bf;font-size:1rem">drugs_side_effects_drugs_com.csv</div>
              <div style="font-size:.75rem;color:#475569">Sumber: Drugs.com via Kaggle</div>
            </div>
          </div>
          <table style="font-size:.85rem;color:#cbd5e1;width:100%;border-collapse:collapse">
            <tr><td style="color:#475569;padding:4px 0;width:30%">Ukuran</td><td>2.931 entri × 17 kolom</td></tr>
            <tr><td style="color:#475569;padding:4px 0">Penyakit</td><td>47 kondisi medis (Hypertension, Diabetes T2, Cholesterol, dst.)</td></tr>
            <tr><td style="color:#475569;padding:4px 0">Peran dalam SPK</td>
                <td><strong style="color:#2dd4bf">Database utama</strong> — semua obat yang dianalisis berasal dari dataset ini</td></tr>
            <tr><td style="color:#475569;padding:4px 0;vertical-align:top">Kolom Kunci</td>
                <td>
                  <span class="badge bt">drug_name</span>
                  <span class="badge bt">medical_condition</span>
                  <span class="badge bt">drug_classes</span>
                  <span class="badge bt">activity → C1 Efikasi</span>
                  <span class="badge bt">side_effects → C3 (teks)</span>
                  <span class="badge bt">rating → Confidence</span>
                  <span class="badge bt">pregnancy_category → Kontraindikasi</span>
                </td></tr>
            <tr><td style="color:#475569;padding:4px 0">Obat per Penyakit</td>
                <td>Hipertensi: <strong>177</strong> &nbsp;|&nbsp; Diabetes T2: <strong>104</strong> &nbsp;|&nbsp; Kolesterol: <strong>45</strong></td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        show_col = ["drug_name","drug_classes","rating","efikasi","efek_samping","harga","dosis_freq","severity_source"]
        st.dataframe(dbs[disease][show_col].head(30).rename(columns={
            "drug_name":"Nama Obat","drug_classes":"Kelas","rating":"Rating",
            "efikasi":"Efikasi(%)","efek_samping":"Efek Samping","harga":"Harga(Rp)",
            "dosis_freq":"Dosis/Hari","severity_source":"Sumber Severity"}),
            use_container_width=True, height=280, hide_index=True)

    with ds_tab2:
        st.markdown("""
        <div class="card c-blue">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
            <span style="font-size:1.8rem">📘</span>
            <div>
              <div style="font-weight:700;color:#60a5fa;font-size:1rem">personalized_medication_dataset.csv</div>
              <div style="font-size:.75rem;color:#475569">Sumber: Kaggle (data sintetis)</div>
            </div>
          </div>
          <table style="font-size:.85rem;color:#cbd5e1;width:100%;border-collapse:collapse">
            <tr><td style="color:#475569;padding:4px 0;width:30%">Ukuran</td><td>1.000 rekam pasien × 17 kolom</td></tr>
            <tr><td style="color:#475569;padding:4px 0">Peran dalam SPK</td>
                <td><strong style="color:#60a5fa">Validasi & statistik</strong> — distribusi efektivitas terapi dan kondisi pasien</td></tr>
            <tr><td style="color:#475569;padding:4px 0;vertical-align:top">Kolom Kunci</td>
                <td>
                  <span class="badge bb">Age</span>
                  <span class="badge bb">Chronic_Conditions</span>
                  <span class="badge bb">Drug_Allergies</span>
                  <span class="badge bb">Treatment_Effectiveness</span>
                  <span class="badge bb">Adverse_Reactions</span>
                  <span class="badge bb">Recovery_Time_Days</span>
                </td></tr>
            <tr><td style="color:#475569;padding:4px 0">Statistik</td>
                <td>Efek samping dilaporkan: <strong style="color:#f472b6">{adv_pct:.1f}%</strong> pasien</td></tr>
          </table>
        </div>
        """.format(adv_pct=adv_pct), unsafe_allow_html=True)

        p1, p2, p3 = st.columns(3)
        with p1:
            fa = px.histogram(pers_df, x="Age", nbins=18, title="Distribusi Usia",
                              color_discrete_sequence=["#60a5fa"])
            fa.update_layout(plot_bgcolor="#04090f",paper_bgcolor="#0f1623",font_color="#e2e8f0",
                             height=240,margin=dict(t=40,b=10,l=5,r=5))
            st.plotly_chart(fa, use_container_width=True)
        with p2:
            cc_v = pers_df["Chronic_Conditions"].fillna("Tidak Ada").value_counts()
            fc = px.pie(values=cc_v.values,names=cc_v.index,title="Kondisi Kronis",
                        color_discrete_sequence=["#60a5fa","#2dd4bf","#f472b6","#c084fc"],hole=.38)
            fc.update_layout(paper_bgcolor="#0f1623",font_color="#e2e8f0",height=240,
                             margin=dict(t=40,b=10,l=5,r=5))
            st.plotly_chart(fc, use_container_width=True)
        with p3:
            eff_v = pers_df["Treatment_Effectiveness"].value_counts()
            fe = px.bar(x=eff_v.index,y=eff_v.values,title="Efektivitas Terapi",
                        color_discrete_sequence=["#f472b6"],
                        labels={"x":"Efektivitas","y":"Pasien"})
            fe.update_layout(plot_bgcolor="#04090f",paper_bgcolor="#0f1623",font_color="#e2e8f0",
                             height=240,margin=dict(t=40,b=10,l=5,r=5))
            st.plotly_chart(fe, use_container_width=True)

    with ds_tab3:
        st.markdown("""
        <div class="card c-amber">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
            <span style="font-size:1.8rem">📙</span>
            <div>
              <div style="font-weight:700;color:#fbbf24;font-size:1rem">medicine_dataset.csv</div>
              <div style="font-size:.75rem;color:#475569">Sumber: Kaggle — 248.218 obat (India/global)</div>
            </div>
          </div>
          <table style="font-size:.85rem;color:#cbd5e1;width:100%;border-collapse:collapse">
            <tr><td style="color:#475569;padding:4px 0;width:30%">Ukuran</td><td>248.218 entri × 58 kolom</td></tr>
            <tr><td style="color:#475569;padding:4px 0;vertical-align:top">Peran dalam SPK</td>
                <td>
                  <strong style="color:#fbbf24">2 fungsi utama:</strong><br>
                  1. <strong>Pengayaan C3 Efek Samping</strong> — 42 kolom efek samping terpisah
                     (sideEffect0..41) dianalisis per kelas aksi, lalu digabung 60:40 dengan DS1<br>
                  2. <strong>Daftar Substitusi Obat</strong> — substitute0..4 ditampilkan sebagai
                     alternatif untuk obat rekomendasi #1
                </td></tr>
            <tr><td style="color:#475569;padding:4px 0;vertical-align:top">Kolom Kunci</td>
                <td>
                  <span class="badge ba">name</span>
                  <span class="badge ba">sideEffect0..41 (42 kolom)</span>
                  <span class="badge ba">substitute0..4</span>
                  <span class="badge ba">Action Class</span>
                  <span class="badge ba">Therapeutic Class</span>
                  <span class="badge ba">Chemical Class</span>
                  <span class="badge ba">Habit Forming</span>
                </td></tr>
            <tr><td style="color:#475569;padding:4px 0">Cara Integrasi</td>
                <td>Dicocokan via <strong>Action Class</strong> → mapping ke drug_classes DS1<br>
                    Severity per kelas = rata-rata dari semua obat dalam kelas tersebut di DS3</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="teal-box">
          <strong style="color:#2dd4bf">🔬 Detail Teknis Integrasi DS3 → C3 (Efek Samping):</strong><br>
          <ol style="margin:8px 0 0;padding-left:20px;line-height:1.9;color:#cbd5e1;font-size:.86rem">
            <li>DS3 dikelompokkan berdasarkan <code>Action Class</code></li>
            <li>Setiap obat dalam kelompok dihitung severity-nya dari 42 kolom sideEffect</li>
            <li>Severity per kelas = rata-rata seluruh obat dalam kelas tersebut</li>
            <li>Dipetakan ke drug_classes DS1 menggunakan tabel ACTION_TO_DRUGSCOM</li>
            <li>Digabung dengan severity teks DS1: <strong>efek_samping = 0.60 × DS1 + 0.40 × DS3</strong></li>
            <li>Jika kelas tidak ditemukan di DS3 → pakai DS1 saja (kolom "Sumber Severity" = "DS1")</li>
          </ol>
        </div>
        """, unsafe_allow_html=True)

        tc_df = pd.DataFrame({"Action Class": list(ac_severity.keys())[:20],
                              "Severity Rata-rata (DS3)": list(ac_severity.values())[:20]})
        st.markdown("**Sample: Severity per Action Class dari DS3**")
        st.dataframe(tc_df, use_container_width=True, height=300, hide_index=True)

    # ── Dataset explorer ──────────────────────────────────
    st.markdown('<hr style="border-color:var(--border);margin:22px 0">', unsafe_allow_html=True)
    st.markdown(sh("🔎","Explorer Dataset Langsung","Lihat data mentah secara interaktif","blue"), unsafe_allow_html=True)
    ds_sel = st.selectbox("Pilih Dataset", [
        f"DS1 — Hipertensi ({len(dbs['Hipertensi'])} obat)",
        f"DS1 — Diabetes Melitus Tipe 2 ({len(dbs['Diabetes Melitus Tipe 2'])} obat)",
        f"DS1 — Kolesterol ({len(dbs['Kolesterol (Hiperlipidemia)'])} obat)",
        f"DS2 — Personalized Medication ({len(pers_df)} pasien)",
    ])
    if "Hipertensi" in ds_sel:
        exp_df = dbs["Hipertensi"]
    elif "Diabetes" in ds_sel:
        exp_df = dbs["Diabetes Melitus Tipe 2"]
    elif "Kolesterol" in ds_sel:
        exp_df = dbs["Kolesterol (Hiperlipidemia)"]
    else:
        exp_df = pers_df

    if "Personalized" not in ds_sel:
        sc = ["drug_name","drug_classes","rating","no_of_reviews","efikasi",
              "dosis_freq","efek_samping","harga","pregnancy_category","severity_source"]
        st.dataframe(exp_df[sc].rename(columns={
            "drug_name":"Nama Obat","drug_classes":"Kelas Obat",
            "rating":"Rating","no_of_reviews":"Ulasan","efikasi":"Efikasi(%)",
            "dosis_freq":"Dosis/Hari","efek_samping":"Efek Samping(0-10)",
            "harga":"Harga(Rp)","pregnancy_category":"Kategori Hamil",
            "severity_source":"Sumber Severity",
        }), use_container_width=True, height=320, hide_index=True)

        x1, x2 = st.columns(2)
        with x1:
            dc_cnt = exp_df["drug_classes"].str.split(",").explode().str.strip().value_counts().head(10)
            fig_cls = px.bar(x=dc_cnt.values, y=dc_cnt.index, orientation="h",
                             color=dc_cnt.values,
                             color_continuous_scale=[[0,"#1e2d44"],[1,"#2dd4bf"]],
                             title="Top 10 Kelas Obat")
            fig_cls.update_layout(plot_bgcolor="#04090f",paper_bgcolor="#0f1623",
                                  font_color="#e2e8f0",coloraxis_showscale=False,
                                  height=310,margin=dict(l=5,r=5,t=40,b=5),
                                  yaxis=dict(autorange="reversed",tickfont_size=9))
            st.plotly_chart(fig_cls, use_container_width=True)
        with x2:
            fig_rat = px.histogram(exp_df, x="rating", nbins=15,
                                   color_discrete_sequence=["#f472b6"],
                                   title="Distribusi Rating Pengguna")
            fig_rat.update_layout(plot_bgcolor="#04090f",paper_bgcolor="#0f1623",
                                  font_color="#e2e8f0",height=310,
                                  margin=dict(l=5,r=5,t=40,b=5))
            st.plotly_chart(fig_rat, use_container_width=True)
    else:
        st.dataframe(exp_df, use_container_width=True, height=320, hide_index=True)

    # ── Referensi ─────────────────────────────────────────
    st.markdown('<hr style="border-color:var(--border);margin:22px 0">', unsafe_allow_html=True)
    st.markdown(sh("📖","Referensi Ilmiah","Landasan teori, panduan klinis, dan sumber dataset","amber"), unsafe_allow_html=True)

    refs = [
        ("1","Edwards, W. (1977)",
         "How to Use Multi-Attribute Utility Measurement for Social Decision Making.",
         "IEEE Trans. Systems, Man, and Cybernetics, 7(5), 326–340.",
         "Makalah dasar metode SMART — fondasi teoritis ASMART.","bt"),
        ("2","Goodwin, P. & Wright, G. (2014)",
         "Decision Analysis for Management Judgment (5th ed.).", "Wiley & Sons.",
         "Teori normalisasi bobot dan utilitas multi-atribut.","bb"),
        ("3","Whelton, P.K. et al. (2018)",
         "2017 ACC/AHA Guideline for Prevention, Detection, Evaluation, and Management of High Blood Pressure.",
         "JACC, 71(19), e127–e248.",
         "Panduan klinis hipertensi — target < 130/80 mmHg, lini pertama obat.","bp"),
        ("4","American Diabetes Association (2023)",
         "Standards of Medical Care in Diabetes — 2023.",
         "Diabetes Care, 46(Suppl 1), S1–S291.",
         "Panduan terapi DM Tipe 2 — target HbA1c, pemilihan obat lini pertama.","ba"),
        ("5","Grundy, S.M. et al. (2019)",
         "2018 AHA/ACC Guideline on the Management of Blood Cholesterol.",
         "JACC, 73(24), e285–e350.",
         "Indikasi statin intensitas tinggi/sedang berdasarkan risiko CVD 10 tahun.","bt"),
        ("6","Drugs.com Dataset (Kaggle)",
         "Drug Side Effects and Medical Conditions Dataset.",
         "kaggle.com — drugs_side_effects_drugs_com.csv",
         "Dataset 1: 2.931 obat, 47 kondisi medis, rating pengguna.","bb"),
        ("7","Personalized Medication Dataset (Kaggle)",
         "Synthetic Personalized Medical Records (1.000 patients).",
         "kaggle.com — personalized_medication_dataset.csv",
         "Dataset 2: validasi efektivitas terapi dan distribusi kondisi pasien.","bp"),
        ("8","Medicine Dataset (Kaggle)",
         "Indian Medicine Dataset — 248.218 drugs with substitute & side effects.",
         "kaggle.com — medicine_dataset.csv",
         "Dataset 3: 42 kolom efek samping terpisah, 5 substitusi, kelas kimia & aksi.","ba"),
        ("9","Lacy, C.F. et al. (2023)",
         "Drug Information Handbook (32nd ed.).",
         "Lexi-Comp / American Pharmacists Association.",
         "Referensi standar dosis, interaksi, dan kontraindikasi obat.","bt"),
    ]
    clr_map2 = {"bt":"var(--teal)","bb":"var(--blue)","bp":"var(--pink)","ba":"var(--amber)","bpu":"var(--purple)"}
    for num, author, title, journal, note, bc in refs:
        clr = clr_map2.get(bc,"var(--teal)")
        st.markdown(f"""
        <div class="ref-card" style="border-left:4px solid {clr}">
          <span class="badge {bc}">[{num}]</span>
          <strong style="color:#e2e8f0"> {author}</strong>
          <em style="color:#94a3b8"> {title}</em>
          <span style="color:#475569;font-size:.8rem"> {journal}</span>
          <div style="font-size:.78rem;color:{clr};margin-top:5px">↳ {note}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-box" style="margin-top:18px">
      ⚠️ <strong>Disclaimer Medis:</strong>
      Sistem ini merupakan alat bantu pengambilan keputusan akademis (Sistem Pendukung Keputusan / SPK)
      dan <strong>tidak menggantikan konsultasi medis profesional.</strong>
      Seluruh rekomendasi yang dihasilkan wajib diverifikasi oleh dokter atau apoteker berlisensi.
    </div>
    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────
st.markdown("""
<div class="grad-bar" style="margin-top:40px"></div>
<div style="text-align:center;color:#334155;font-size:.74rem;padding:12px 0 20px;line-height:1.9">
  <span style="background:linear-gradient(135deg,#2dd4bf,#f472b6);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;font-weight:800">SPK ASMART</span>
  &nbsp;—&nbsp; Sistem Pendukung Keputusan Terapi Obat Multi-Penyakit<br>
  <span style="color:#2dd4bf">DS1</span> drugs_side_effects_drugs_com.csv &nbsp;·&nbsp;
  <span style="color:#f472b6">DS2</span> personalized_medication_dataset.csv &nbsp;·&nbsp;
  <span style="color:#60a5fa">DS3</span> medicine_dataset.csv<br>
  Metode: <em>Adaptive Simple Multi-Attribute Rating Technique</em>
  &nbsp;|&nbsp; Built with Streamlit + Plotly + Pandas
</div>
""", unsafe_allow_html=True)