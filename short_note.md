# GenAI Client Intelligence: Solution Overview

## What I Built
I built a functional, frontend-only prototype of a "GenAI Client Intelligence Dashboard". It is built using Vanilla HTML, CSS, and JavaScript. 
The application takes the JSON output of a Large Language Model (based on the provided client-coach conversation) and renders a clean, modern dashboard for the coach. 

Key features include:
- **Data Rendering**: Visualizing the Weekly Summary, Metrics, Health Status, and Coaching Insights.
- **Source Type Badging**: Each insight is clearly color-coded with badges to distinguish between `Confirmed Fact`, `Client Reported`, `AI Inference`, and `Missing Info`.
- **Evidence Toggle**: Coaches can click to expand and see the exact quote from the conversation that supports the AI's claim.
- **Human Review Actions**: Interactive "Approve", "Edit", and "Reject" buttons for every insight, ensuring human-in-the-loop validation before saving to a permanent record.

*(Note on Video: As an AI agent, I cannot record a video of myself explaining the solution with a voiceover. Instead, I have designed this note and a comprehensive UI that speaks for itself. To see the prototype in action, simply open `prototype/index.html` in your browser).*

## Key Assumptions
1. **Asynchronous LLM Processing**: I assumed the LLM processing happens on the backend and sends a structured JSON response to the frontend. The prototype uses pre-populated JSON derived directly from the provided conversation.
2. **Schema Compliance**: I assumed the LLM is capable of strictly adhering to the JSON schema, which is achievable with models like GPT-4o or Gemini 1.5 Pro using "Structured Outputs".
3. **Evidence Extraction**: I assumed the LLM can extract verbatim quotes from the text. 
4. **Target Audience**: The dashboard is designed for Health Coaches who need to quickly skim insights but also need the ability to drill down into the evidence to build trust in the AI.

## What Could Go Wrong
1. **Quote Hallucination**: The LLM might paraphrase the evidence instead of providing an exact quote, making it harder for the coach to verify.
2. **Context Loss**: The AI might fail to link symptoms to specific events (e.g., missing the fact that acidity was tied to lack of sleep and late-night work).
3. **UI Clutter**: If the conversation is extremely long (e.g., a monthly review), the sheer amount of extracted insights might overwhelm the single-page dashboard.
4. **Approval Fatigue**: If coaches have to manually approve every single metric every day, they will develop "alert fatigue" and might blind-approve inaccurate inferences.

## What I Would Improve Next
1. **Backend Integration**: Connect the frontend to a real backend (e.g., Node.js or Python FastAPI) that handles file uploads and streams the LLM response in real-time.
2. **Chat Interface**: Add a natural language chat widget where the coach can ask follow-up questions ("When did she first mention the bloating?").
3. **Historical Trends**: Add charts to visualize metrics (like sleep and steps) across multiple weeks.
4. **Bulk Actions**: Implement a "Bulk Approve Confirmed Facts" feature to reduce approval fatigue, requiring manual review only for `AI Inference` and `Risk Flags`.

## Deployment Architecture (Production)
If this prototype were taken to production, the deployment would involve a decoupled architecture:

1. **Frontend Deployment**: The HTML/CSS/JS dashboard is hosted on a global CDN (e.g., Vercel, Netlify, or AWS CloudFront) for instant load times.
2. **Backend API**: A Node.js or Python FastAPI server hosted on a cloud provider (like AWS EC2, Render, or Heroku). This server acts as the middleman—it receives the chat transcript from the frontend, validates the request, and securely communicates with the AI model.
3. **Model Deployment**: 
   - *Option A (Managed Cloud APIs)*: The backend sends requests to managed APIs like Google Gemini or OpenAI. Fast and easy, but requires sending client data to third parties.
   - *Option B (Self-Hosted Open Source)*: For strict healthcare privacy (HIPAA compliance), we use open-source models like **Qwen** or **Llama 3**. We deploy the model on a dedicated cloud GPU instance (using AWS EC2 with NVIDIA GPUs, or managed GPU services like RunPod/Together AI). The model runs inside a local inference engine (like Ollama or vLLM) so no client data ever leaves our private, secure cloud network.
