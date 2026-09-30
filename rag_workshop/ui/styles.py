import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
            :root {
                --canvas: #f4f6f1;
                --surface: #ffffff;
                --ink: #17231f;
                --muted: #718079;
                --line: #e1e8e2;
                --green: #187a58;
                --green-deep: #12563f;
                --green-soft: #e8f3ec;
                --shadow: 0 8px 24px rgba(28, 51, 41, 0.055);
            }

            .stApp {
                background-color: var(--canvas);
                background-image: radial-gradient(#dfe8df 0.65px, transparent 0.65px);
                background-size: 18px 18px;
                color: var(--ink);
            }

            [data-testid="stAppViewContainer"] {
                background: linear-gradient(115deg, rgba(244, 246, 241, 0.97), rgba(249, 250, 247, 0.94));
            }

            .main .block-container {
                padding: 1.35rem 2.4rem 3rem;
                max-width: 1280px;
            }

            h1, h2, h3, h4, h5, h6 {
                color: var(--ink) !important;
                letter-spacing: 0;
            }

            p, label {
                color: var(--muted);
            }

            .workspace-header {
                min-height: 52px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 1px solid var(--line);
                margin-bottom: 2.3rem;
                padding-bottom: 0.9rem;
            }

            .brand-lockup {
                display: flex;
                align-items: center;
                gap: 0.65rem;
            }

            .brand-mark {
                width: 34px;
                height: 34px;
                display: grid;
                place-items: center;
                border-radius: 10px;
                background: var(--green-deep);
                color: #ffffff;
                font-size: 1.25rem;
                font-weight: 800;
            }

            .brand-name {
                color: var(--ink);
                font-size: 1.17rem;
                font-weight: 750;
                letter-spacing: 0;
            }

            .brand-name span {
                color: var(--green);
            }

            .workspace-mode {
                color: #607168;
                font-size: 0.67rem;
                font-weight: 700;
                letter-spacing: 0.08em;
            }

            .mode-dot, .model-indicator {
                width: 7px;
                height: 7px;
                display: inline-block;
                border-radius: 50%;
                background: #3aa878;
                margin-right: 0.4rem;
            }

            .welcome-row {
                margin-bottom: 1.2rem;
            }

            .welcome-row h1 {
                margin: 0.25rem 0 0.45rem;
                font-size: 2rem;
                font-weight: 720;
                line-height: 1.2;
            }

            .welcome-row p {
                margin: 0;
                font-size: 0.96rem;
            }

            .eyebrow, .section-kicker {
                color: var(--green);
                font-size: 0.67rem;
                font-weight: 800;
                letter-spacing: 0.11em;
            }

            .model-line {
                min-height: 40px;
                display: flex;
                align-items: center;
                gap: 0.45rem;
                padding: 0.55rem 0.8rem;
                margin: 1rem 0 1.65rem;
                border: 1px solid var(--line);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.72);
                color: var(--muted);
                font-size: 0.78rem;
            }

            .model-line strong {
                overflow: hidden;
                color: var(--ink);
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            .model-line .offline {
                background: #d5a340;
            }

            .model-label {
                color: #89978f;
                font-size: 0.62rem;
                font-weight: 750;
                letter-spacing: 0.08em;
            }

            .model-divider {
                width: 1px;
                height: 16px;
                margin: 0 0.5rem;
                background: var(--line);
            }

            .section-kicker {
                margin: 0.35rem 0 0.65rem;
            }

            .upload-kicker {
                margin-top: 1.5rem;
            }

            .stat-card {
                min-height: 98px;
                padding: 0.78rem 0.9rem;
                border: 1px solid var(--line);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.88);
                box-shadow: var(--shadow);
            }

            .stat-label {
                color: #829088;
                font-size: 0.61rem;
                font-weight: 800;
                letter-spacing: 0.09em;
            }

            .stat-value {
                overflow: hidden;
                margin-top: 0.35rem;
                color: var(--ink);
                font-size: 1.23rem;
                font-weight: 730;
                line-height: 1.2;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            .stat-detail {
                overflow: hidden;
                margin-top: 0.2rem;
                color: var(--muted);
                font-size: 0.7rem;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            .conversation-kicker {
                margin-top: 2rem;
            }

            section[data-testid="stSidebar"] {
                background: #edf2ec;
                border-right: 1px solid #dce5dc;
            }

            section[data-testid="stSidebar"] .block-container {
                padding-top: 1.5rem;
            }

            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] label {
                color: var(--ink) !important;
            }

            .stTextInput input,
            .stTextArea textarea,
            [data-testid="stChatInput"] textarea {
                border-color: #d8e2da !important;
                border-radius: 8px !important;
                background: #ffffff !important;
                color: var(--ink) !important;
            }

            [data-testid="stFileUploaderDropzone"] {
                border: 1px dashed #aabbb0;
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.75);
            }

            [data-testid="stFileUploaderDropzone"] button {
                border: 1px solid #cbd8ce;
                border-radius: 6px;
                background: #ffffff;
                color: var(--green-deep);
            }

            .stButton > button {
                min-height: 2.5rem;
                border: 1px solid var(--green-deep);
                border-radius: 7px;
                background: var(--green-deep);
                color: #ffffff;
                font-weight: 650;
            }

            .stButton > button:hover {
                border-color: var(--green);
                background: var(--green);
                color: #ffffff;
            }

            [data-testid="stChatMessage"] {
                border: 1px solid var(--line);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.83);
            }

            .stAlert, .stExpander {
                border-radius: 8px;
            }

            .stExpander {
                border: 1px solid var(--line);
                background: #ffffff;
            }

            @media (max-width: 700px) {
                .main .block-container {
                    padding: 1rem 1rem 2rem;
                }

                .workspace-header {
                    margin-bottom: 1.5rem;
                }

                .workspace-mode {
                    font-size: 0.56rem;
                }

                .welcome-row h1 {
                    font-size: 1.65rem;
                }

                .model-line {
                    flex-wrap: wrap;
                }

                .stat-card {
                    min-height: 86px;
                    padding: 0.65rem;
                }

                .stat-value {
                    font-size: 1.05rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
