import streamlit as st
import json
import ollama
import os

# Set up the page layout
st.set_page_config(page_title="VitalCoach Intelligence", layout="wide")

# Custom CSS for Apple-like minimalist aesthetic
st.markdown("""
<style>
    /* Typography and Colors */
    html, body, [class*="css"]  {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        color: #1d1d1f !important;
    }
    
    /* Background */
    .stApp {
        background-color: #fbfbfd;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.015em !important;
        color: #1d1d1f !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 0.2rem !important;
    }
    
    p, .stMarkdown {
        color: #86868b !important;
        font-size: 1rem;
        line-height: 1.5;
    }

    /* Primary Button */
    .stButton>button {
        background-color: #0071e3 !important;
        color: white !important;
        border-radius: 980px !important; /* Pill shape */
        border: none !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        transition: background-color 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #0077ed !important;
    }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.03);
        border: 1px solid #e5e5ea;
    }
    
    /* Expander / Evidence */
    .streamlit-expanderHeader {
        font-size: 0.85rem !important;
        color: #0071e3 !important;
    }
    
    /* Badges */
    .badge {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 2px 6px;
        border-radius: 6px;
        margin-left: 8px;
    }
    .badge-confirmed { background-color: #e5f5ea; color: #008736; }
    .badge-client_reported { background-color: #e8f2ff; color: #0071e3; }
    .badge-ai_inference { background-color: #f4e8fc; color: #8a2be2; }
    .badge-missing_info { background-color: #ffe8e8; color: #e30000; }
    
    hr {
        border-top: 1px solid #d2d2d7;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("VitalCoach Intelligence")
st.markdown("Automated client analysis and telemetry.")

# Layout: Sidebar for inputs
with st.sidebar:
    st.header("Configuration")
    selected_model = st.text_input("Ollama Model", value="qwen3:4b-instruct")
    
    st.header("Input Data")
    # Load default transcript if available
    default_text = ""
    try:
        transcript_path = os.path.join(os.path.dirname(__file__), "transcript.txt")
        with open(transcript_path, "r", encoding="utf-8") as f:
            default_text = f.read()
    except:
        pass
        
    transcript_input = st.text_area("Client Transcript", value=default_text, height=400)
    
    analyze_btn = st.button("Generate Report")

# Main Content Area
if analyze_btn and transcript_input:
    with st.spinner("Processing transcript..."):
        
        # 1. Load the JSON Schema
        schema = {}
        try:
            schema_path = os.path.join(os.path.dirname(__file__), "json_schema.json")
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)
        except Exception as e:
            st.error("Could not load json_schema.json. Please ensure it is in the same directory.")
            st.stop()

        # 2. Construct Prompt
        prompt = f"""
        You are an expert AI health and wellness coaching assistant. Analyze the conversation transcript between a health coach and their client, and generate a structured intelligence report based on the client's progress, adherence, and well-being.
        
        Extract key insights and metrics. For every claim or metric extracted, you MUST classify its source type into one of the following categories:
        1. **confirmed_fact**: Verifiable data, system logs, or coach-verified facts.
        2. **client_reported**: Information directly stated by the client.
        3. **ai_inference**: Conclusions logically deduced by the AI but not explicitly stated.
        4. **missing_info**: Important metrics that were not reported.
        
        ### Conversation Transcript:
        {transcript_input}
        """

        # 3. Call Ollama
        try:
            response = ollama.chat(
                model=selected_model,
                messages=[
                    {'role': 'system', 'content': 'You are a precise data extraction AI. You only output valid JSON.'},
                    {'role': 'user', 'content': prompt}
                ],
                format=schema,
                options={'temperature': 0.1}
            )
            
            # Parse response
            result = json.loads(response['message']['content'])
            
            # --- RENDER THE DASHBOARD ---
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Top Summary
            st.subheader("Weekly Summary")
            st.write(result.get("client_summary", {}).get("weekly_overview", "N/A"))
            
            st.metric("Engagement Level", result.get("client_summary", {}).get("engagement_level", "Unknown"))
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Helper to display a metric card
            def display_card(title, data):
                if not data: return
                
                source_type = data.get("source_type", "unknown")
                source_label = str(source_type).replace("_", " ")
                
                # Render with HTML to apply custom badges
                st.markdown(f"""
                <div style="background-color: #ffffff; padding: 1.25rem; border-radius: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); border: 1px solid #e5e5ea; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <h4 style="margin: 0; color: #1d1d1f; font-size: 1.05rem;">{title}</h4>
                        <span class="badge badge-{source_type}">{source_label}</span>
                    </div>
                    <p style="margin: 0 0 0.5rem 0; color: #1d1d1f; font-weight: 500;">{data.get('status')}</p>
                    <p style="margin: 0 0 1rem 0; color: #86868b; font-size: 0.9rem;">{data.get('details')}</p>
                    <details>
                        <summary style="color: #0071e3; font-size: 0.85rem; cursor: pointer; outline: none;">View Evidence</summary>
                        <p style="margin-top: 0.5rem; padding: 0.75rem; background-color: #f5f5f7; border-radius: 8px; font-style: italic; font-size: 0.85rem; color: #1d1d1f;">"{data.get("evidence")}"</p>
                    </details>
                </div>
                """, unsafe_allow_html=True)

            # Layout metrics into two columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Core Metrics")
                metrics = result.get("metrics", {})
                display_card("Nutrition Adherence", metrics.get("nutrition_adherence"))
                display_card("Exercise & Steps", metrics.get("exercise_steps"))
                display_card("Sleep", metrics.get("sleep"))
                display_card("Water Intake", metrics.get("water_intake"))
                
                st.subheader("Health & Symptoms")
                display_card("Symptoms & Stress", result.get("health_status", {}).get("symptoms_stress"))

            with col2:
                st.subheader("Coaching Insights")
                insights = result.get("coaching_insights", {})
                
                st.markdown("#### Risk & Attention Flags")
                for flag in insights.get("risk_attention_flags", []):
                    display_card("Risk", flag)
                    
                st.markdown("#### Key Barriers")
                for barrier in insights.get("key_barriers", []):
                    display_card("Barrier", barrier)
                    
                st.markdown("#### Pending Actions")
                for action in insights.get("pending_actions", []):
                    display_card("Action", action)

                st.subheader("Recommended Next Action")
                next_action = insights.get("recommended_next_action", {})
                display_card("Coach Recommendation", next_action)
                
        except Exception as e:
            st.error("Error during AI generation. Please check terminal logs.")
            st.write(e)

elif not analyze_btn:
    st.markdown("Enter the transcript in the sidebar and click Generate Report.")
