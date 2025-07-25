import streamlit as st
import pandas as pd
import joblib
import os
import streamlit.components.v1 as components
import csv
import json
from datetime import datetime

# Set Streamlit cache directory to 'log'
st.cache_data.clear()
st.cache_resource.clear()
os.environ['STREAMLIT_CACHE_DIR'] = os.path.abspath('log')

LOG_DIR = 'log'
PREDICTION_LOG = os.path.join(LOG_DIR, 'predictions.csv')

# Path constants
DATA_PATH = 'transformed_data/Processed_Auto_Insurance_Fraud_Claims_File03.csv'
MODELS_DIR = 'models'
LOGO_PATH = 'public/logo.jpg'
EDA_REPORT_PATH = 'EDA/report.html'

# Data dictionary (from txt file, manually extracted for form fields)
FIELD_DESCRIPTIONS = {
    'Claim_ID': 'Unique identifier for each claim submitted by the policyholder',
    'Bind_Date1': 'Policy bind date',
    'Customer_Life_Value1': 'Estimated lifetime value of the customer',
    'Age_Insured': 'Age of the insured person',
    'Policy_Num': 'Policy number',
    'Policy_State': 'State of policy',
    'Policy_Start_Date': 'Policy start date',
    'Policy_Expiry_Date': 'Policy expiry date',
    'Policy_BI': 'Bodily Injury liability coverage limit',
    'Policy_Ded': 'Deductible amount',
    'Policy_Premium': 'Total premium amount (6 months)',
    'Umbrella_Limit': 'Additional liability coverage',
    'Insured_Zip': 'Zip code of the insured',
    'Gender': 'Gender',
    'Education': 'Education level',
    'Occupation': 'Occupation',
    'Hobbies': 'Hobbies',
    'Insured_Relationship': 'Relationship status',
    'Capital_Gains': 'Capital gains',
    'Capital_Loss': 'Capital losses',
    'Garage_Location': 'Garage location',
    'Accident_Date': 'Accident date',
    'Accident_Type': 'Type of accident',
    'Collision_Type': 'Nature of collision',
    'Accident_Severity': 'Severity of accident',
    'authorities_contacted': 'Authorities contacted',
    'Acccident_State': 'Accident state',
    'Acccident_City': 'Accident city',
    'Accident_Location': 'Accident location',
    'Accident_Hour': 'Hour of accident',
    'Num_of_Vehicles_Involved': 'Number of vehicles involved',
    'Property_Damage': 'Property damage',
    'Bodily_Injuries': 'Bodily injuries count',
    'Witnesses': 'Number of witnesses',
    'Police_Report': 'Police report filed',
    'DL_Expiry_Date': 'Driver’s license expiry',
    'Claims_Date': 'Claim date',
    'Auto_Make': 'Vehicle make',
    'Auto_Model': 'Vehicle model',
    'Auto_Year': 'Vehicle year',
    'Vehicle_Color': 'Vehicle color',
    'Vehicle_Cost': 'Vehicle cost',
    'Annual_Mileage': 'Annual mileage',
    'DiffIN_Mileage': 'Difference in mileage',
    'Low_Mileage_Discount': 'Low mileage discount',
    'Commute_Discount': 'Commute discount',
    'Total_Claim': 'Total claim amount',
    'Injury_Claim': 'Injury claim amount',
    'Property_Claim': 'Property claim amount',
    'Vehicle_Claim': 'Vehicle claim amount',
    'Vehicle_Registration': 'Vehicle registration',
    'Check_Point': 'Internal check point',
}

# --- Custom CSS for black, light green, and orange theme ---
st.markdown('''
    <style>
    body, .stApp, .main {
        background-color: #000 !important;
    }
    .stApp {
        background-color: #000 !important;
    }
    .st-bb, .st-cg {
        background: #000 !important;
    }
    .stSidebar {
        background-color: #18181b !important;
        color: #f59e42 !important;
    }
    .sidebar-content {
        color: #f59e42 !important;
    }
    .stButton>button {
        background-color: #f59e42;
        color: #000;
        font-weight: bold;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(251,191,36,0.08);
    }
    .stButton>button:hover {
        background-color: #bbf7d0;
        color: #000;
    }
    .stTextInput>div>input {
        background-color: #bbf7d0;
        color: #000;
        border-radius: 6px;
        border: 1px solid #f59e42;
    }
    .stSelectbox>div>div {
        background-color: #bbf7d0 !important;
        color: #f59e42 !important;
    }
    /* Sidebar selectbox dropdown menu background and options */
    section[data-testid="stSidebar"] div[data-baseweb="select"] div[role="listbox"] {
        background-color: #18181b !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] div[role="option"] {
        background-color: #18181b !important;
        color: #f59e42 !important;
    }
    /* Main selectbox dropdown menu background and options */
    div[data-baseweb="select"] div[role="listbox"] {
        background-color: #bbf7d0 !important;
    }
    div[data-baseweb="select"] div[role="option"] {
        background-color: #bbf7d0 !important;
        color: #f59e42 !important;
    }
    .footer {
        text-align: center;
        color: #bbf7d0;
        font-size: 0.9em;
        margin-top: 2em;
    }
    /* Make selectbox options orange */
    div[data-baseweb="select"] span {
        color: #f59e42 !important;
    }
    select {
        color: #f59e42 !important;
        background-color: #bbf7d0 !important;
    }
    /* Card style containers */
    .card {
        background: #bbf7d0;
        border-radius: 16px;
        box-shadow: 0 2px 16px rgba(44,62,80,0.08);
        padding: 2em 2em 1em 2em;
        margin-bottom: 2em;
    }
    .centered-title {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 1.5em;
    }
    /* Sidebar text color to orange */
    section[data-testid="stSidebar"] *, .stSidebar, .sidebar-content, .stSelectbox label, .stSelectbox span, .stSelectbox div {
        color: #f59e42 !important;
    }
    .sidebar-nav {
        margin-top: 1.5em;
        margin-bottom: 2em;
    }
    .sidebar-nav .nav-btn {
        display: block;
        width: 100%;
        padding: 0.75em 1em;
        margin-bottom: 0.5em;
        background: #18181b;
        color: #f59e42;
        border: none;
        border-radius: 8px;
        font-size: 1.1em;
        text-align: left;
        cursor: pointer;
        transition: background 0.2s, color 0.2s;
    }
    .sidebar-nav .nav-btn.selected {
        background: #f59e42;
        color: #18181b;
        font-weight: bold;
        border-left: 6px solid #bbf7d0;
    }
    </style>
''', unsafe_allow_html=True)

# --- Sidebar: Custom navigation and Model selection ---
if 'page' not in st.session_state:
    st.session_state['page'] = 'EDA Report'

with st.sidebar:
    st.image(LOGO_PATH, width=600)
    st.markdown('<h2 style="color:#f59e42;">Navigation</h2>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    eda_btn = st.button('EDA Report', key='nav_eda', help='Go to EDA Report page')
    pred_btn = st.button('Prediction', key='nav_pred', help='Go to Prediction page')
    bench_btn = st.button('Benchmarks', key='nav_bench', help='Go to Benchmarks page')
    st.markdown('</div>', unsafe_allow_html=True)
    if eda_btn:
        st.session_state['page'] = 'EDA Report'
    if pred_btn:
        st.session_state['page'] = 'Prediction'
    if bench_btn:
        st.session_state['page'] = 'Benchmarks'
    # Highlight the selected nav
    st.markdown(f'''
        <script>
        var btns = window.parent.document.querySelectorAll('.sidebar-nav .nav-btn');
        if (btns.length > 0) {{
            btns[0].classList.remove('selected');
            btns[1].classList.remove('selected');
            btns[2].classList.remove('selected');
            btns[{['EDA Report','Prediction','Benchmarks'].index(st.session_state['page'])}].classList.add('selected');
        }}
        </script>
    ''', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#f59e42;">Model Selection</h2>', unsafe_allow_html=True)
    def get_model_files():
        if not os.path.exists(MODELS_DIR):
            return []
        files = [f for f in os.listdir(MODELS_DIR) if f.endswith('_pipeline.pkl')]
        display_names = [f.replace('_pipeline.pkl', '').replace('_', ' ').title() for f in files]
        return files, display_names
    model_files, model_display_names = get_model_files()
    if model_files:
        selected_model_display = st.selectbox('Choose a model:', model_display_names, label_visibility='visible')
        selected_model_file = model_files[model_display_names.index(selected_model_display)]
        MODEL_PATH = os.path.join(MODELS_DIR, selected_model_file)
    else:
        st.warning('No model files found in models directory.')
        MODEL_PATH = None
    st.markdown('<hr style="border:1px solid #f59e42;">', unsafe_allow_html=True)
    st.markdown('<span style="color:#f59e42;">Powered by Learnathon 4.0</span>', unsafe_allow_html=True)

# --- Multipage logic ---
page = st.session_state['page']
if page == 'Prediction':
    # --- Main Title and Description ---
    st.markdown('<div class="centered-title">', unsafe_allow_html=True)
    st.markdown('<h1 style="color:#f59e42;display:inline;margin-bottom:0;">Auto Insurance Fraud Prediction</h1>', unsafe_allow_html=True)
    st.markdown('''<p style="font-size:1.1em; color:#bbf7d0; margin-top:0.5em;">Select a <b>Claim ID</b> to auto-fill, or enter data manually if not available.<br>Choose your model from the sidebar and click <b>Predict Fraud</b> to see the result.</p>''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Load only the header and Claim_IDs for selection ---
    @st.cache_data
    def get_claim_ids_and_columns():
        df = pd.read_csv(DATA_PATH, usecols=['Claim_ID'], dtype=str)
        all_data = pd.read_csv(DATA_PATH, nrows=1)
        columns = all_data.columns.tolist()
        return df['Claim_ID'].tolist(), columns

    claim_ids, columns = get_claim_ids_and_columns()
    if 'shuffled_claim_ids' not in st.session_state:
        import random
        shuffled = claim_ids.copy()
        random.shuffle(shuffled)
        st.session_state['shuffled_claim_ids'] = shuffled
    claim_ids = st.session_state['shuffled_claim_ids']

    # --- Claim ID Selection ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader('Claim Selection')
        selected_id = st.selectbox('Select Claim ID (or leave blank for manual entry):', [''] + claim_ids, help='Choose a Claim ID to auto-fill the form, or leave blank to enter data manually.')
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Try to load the row for the selected Claim_ID ---
    row_data = None
    if selected_id:
        try:
            for chunk in pd.read_csv(DATA_PATH, dtype=str, chunksize=10000):
                match = chunk[chunk['Claim_ID'] == selected_id]
                if not match.empty:
                    row_data = match.iloc[0].to_dict()
                    break
        except Exception as e:
            st.error(f'Error loading data for Claim_ID {selected_id}: {e}')

    # --- Build the form in columns for better layout ---
    with st.form('fraud_form'):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader('Claim Details')
        form_data = {}
        col1, col2 = st.columns(2)
        for idx, col in enumerate(columns):
            if col == 'Fraud_Ind':
                continue  # Don't show target
            label = FIELD_DESCRIPTIONS.get(col, col)
            default = row_data[col] if row_data and col in row_data else ''
            helptext = FIELD_DESCRIPTIONS.get(col, '')
            with (col1 if idx % 2 == 0 else col2):
                form_data[col] = st.text_input(label, value=default, help=helptext)
        submitted = st.form_submit_button('Predict Fraud')
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Prediction and Result ---
    if submitted:
        features = [
            'Customer_Life_Value1','Age_Insured','Policy_State','Policy_Ded','Policy_Premium','Gender','Education',
            'Property_Damage','Bodily_Injuries','Witnesses','Auto_Model','Vehicle_Cost','Annual_Mileage','DiffIN_Mileage',
            'Total_Claim','Injury_Claim','Property_Claim','License_Validity','Claim_Intensity','Vehicle_Claim',
            'Wait_Policy_BI','Indemnity_Policy_BI','Policy_Duration','Claim_Duration'
        ]
        input_data = {f: form_data.get(f, '') for f in features}
        input_df = pd.DataFrame([input_data])

        # Add shake animation CSS
        st.markdown('''
        <style>
        @keyframes shake {
            0% { transform: translateX(0); }
            20% { transform: translateX(-10px); }
            40% { transform: translateX(10px); }
            60% { transform: translateX(-10px); }
            80% { transform: translateX(10px); }
            100% { transform: translateX(0); }
        }
        .shake-effect {
            animation: shake 0.5s;
        }
        </style>
        ''', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color:#f59e42; margin-bottom:0.5em;">Prediction Result</h3>', unsafe_allow_html=True)
        if not MODEL_PATH or not os.path.exists(MODEL_PATH):
            st.error(f'Model file not found: {MODEL_PATH}')
        else:
            model = joblib.load(MODEL_PATH)
            try:
                pred = model.predict(input_df)[0]
                pred_label = 'FRAUD' if pred else 'NOT FRAUD'
                if pred:
                    st.markdown('<div id="fraud-shake" class="shake-effect" style="background:#f59e42;padding:1em;border-radius:8px;"><h3 style="color:#000;">🚨 FRAUD DETECTED</h3></div>', unsafe_allow_html=True)
                    # JavaScript to re-trigger the shake effect
                    st.markdown('''
                    <script>
                    const el = window.parent.document.getElementById('fraud-shake');
                    if (el) {
                        el.classList.remove('shake-effect');
                        void el.offsetWidth;
                        el.classList.add('shake-effect');
                    }
                    </script>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="background:#bbf7d0;padding:1em;border-radius:8px;"><h3 style="color:#000;">✅ NOT FRAUD</h3></div>', unsafe_allow_html=True)
                # --- Log the prediction ---
                os.makedirs(LOG_DIR, exist_ok=True)
                log_exists = os.path.exists(PREDICTION_LOG)
                with open(PREDICTION_LOG, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    if not log_exists:
                        writer.writerow(['timestamp', 'model', 'input_json', 'prediction'])
                    writer.writerow([
                        datetime.now().isoformat(),
                        os.path.basename(MODEL_PATH) if MODEL_PATH else '',
                        json.dumps(input_data, ensure_ascii=False),
                        pred_label
                    ])
            except Exception as e:
                st.error(f'Prediction error: {e}')
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Footer ---
    st.markdown('<div class="footer">&copy; 2025 Learnathon 4.0 &mdash; Auto Insurance Fraud Detection App</div>', unsafe_allow_html=True)

elif page == 'EDA Report':
    st.markdown('<div class="centered-title">', unsafe_allow_html=True)
    st.markdown('<h1 style="color:#f59e42;display:inline;margin-bottom:0;">EDA Report</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if os.path.exists(EDA_REPORT_PATH):
        with open(EDA_REPORT_PATH, 'r', encoding='utf-8') as f:
            report_html = f.read()
        components.html(report_html, height=900, scrolling=True)
    else:
        st.error(f'EDA report not found at {EDA_REPORT_PATH}')

elif page == 'Benchmarks':
    st.markdown('<div class="centered-title">', unsafe_allow_html=True)
    st.markdown('<h1 style="color:#f59e42;display:inline;margin-bottom:0;">Benchmarks</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#f59e42; margin-bottom:1em;">Model Benchmark Results</h3>', unsafe_allow_html=True)
    img_path = 'models/benchmark_results_heatmap.png'
    if os.path.exists(img_path):
        st.image(img_path, use_column_width=True, caption='Model Performance Heatmap')
    else:
        st.error(f'Benchmark heatmap not found at {img_path}')
    st.markdown('</div>', unsafe_allow_html=True)
