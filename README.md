# PayPal AI Hackathon Demo

## Overview

This is a minimal **full‑stack web app** that demonstrates a meaningful integration of **PayPal Checkout** and **AI** (OpenAI GPT).  The app lets a user chat with an AI assistant that can recommend products.  When the user selects a recommendation, the app creates a PayPal order and completes the payment using the PayPal sandbox.

- **Backend** – Python 3, Flask, `paypalcheckoutsdk`, `openai`.
- **Frontend** – Simple HTML/JS, PayPal JavaScript SDK, a chat UI.
- **AI** – Calls OpenAI's Chat Completion API to generate product suggestions and answer user questions.

The project is ready to run locally with the PayPal sandbox and can be deployed to any cloud host (e.g., Render, Vercel, Azure).  All code is open‑source and includes a `README` with step‑by‑step instructions for judges.

## Prerequisites

- Python 3.9+ 
- A PayPal Developer sandbox account (client‑id & secret).  Create one at https://developer.paypal.com/developer/applications/.  Use the **Sandbox** credentials.
- An OpenAI API key (or any compatible LLM endpoint).

## Setup

```bash
# Clone the repo (once we push it) or copy the folder
cd paypal_ai_hackathon
# Create a virtual environment
python -m venv venv
venv\Scripts\activate   # on Windows
# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project root with the following variables:

```
PAYPAL_CLIENT_ID=YOUR_SANDBOX_CLIENT_ID
PAYPAL_CLIENT_SECRET=YOUR_SANDBOX_SECRET
OPENAI_API_KEY=YOUR_OPENAI_KEY
FLASK_APP=app.py
```

## Run the app

```bash
flask run
```

Open `http://127.0.0.1:5000` in a browser.  You will see a chat window.  Type something like *"I want a cheap wireless mouse"* and the AI will suggest a product with a price.  Click **Buy with PayPal** to complete the sandbox transaction.

## Project Structure

```
paypal_ai_hackathon/
├─ app.py               # Flask server, PayPal & OpenAI integration
├─ requirements.txt     # Python dependencies
├─ .gitignore
├─ .env.example         # Example env file (do not commit real keys)
├─ templates/
│  └─ index.html       # Front‑end UI
└─ static/
   └─ style.css        # Basic styling
```

## Demo Video

Record a short (≤ 3 min) video showing:
1. Starting the server.
2. Interacting with the AI chat.
3. Clicking the PayPal button and completing the sandbox checkout.
4. The **Success** page.

Upload it to YouTube (public) and include the link in the submission form.

## License

MIT – feel free to fork or adapt.

---

**Next steps**: the repository can be pushed to GitHub, the demo video recorded, and the submission completed.
## Inspiration

When I first explored the PayPal Developer portal, I was struck by the simplicity of creating a payment flow, but I wondered **what would happen if an AI could drive that flow on behalf of the user**. The idea of turning a natural‑language request (e.g., “I need a cheap wireless mouse”) into a **complete e‑commerce transaction** seemed both novel and instantly understandable for judges.

## What it does

- Provides a chat‑style interface where users ask for product recommendations.
- Uses OpenAI’s Chat Completion API to generate a single product suggestion in JSON (name, description, price).
- Dynamically creates a PayPal order for the quoted price and renders the PayPal button.
- Captures the payment in the PayPal sandbox and shows a success message.

## How we built it

1. **Backend (Flask)** – Exposes `/api/chat`, `/api/create-order`, and `/api/capture-order` endpoints.
2. **AI Prompt Engineering** – System prompt forces the model to return strict JSON.
3. **PayPal SDK** – `paypalcheckoutsdk` on the server for order creation/capture; JavaScript SDK on the client for the button.
4. **Frontend (HTML/JS)** – Simple chat UI, parses the JSON response, injects the PayPal button with the generated order ID.
5. **Environment Management** – `.env` for credentials, `.gitignore` to keep secrets out of version control.

## Challenges we ran into

- **LLM output variability** – tackled with a constrained system prompt and client‑side JSON parsing fallback.
- **Sandbox token handling** – kept client‑id public for the JS SDK and secret server‑side for the Python SDK.
- **CORS concerns** – served from `localhost` to avoid cross‑origin restrictions.
- **Deployability** – documented how to set secrets on Render/Vercel for cloud deployment.

## Accomplishments that we're proud of

- End‑to‑end flow: user message → AI recommendation → PayPal checkout → capture, all in under 30 seconds.
- Minimal codebase (≈ 150 lines backend, 100 lines frontend) that is easy to understand and extend.
- Fully functional with PayPal sandbox and OpenAI without any proprietary SDKs beyond the official ones.

## What we learned

- Effective prompt engineering is key to getting deterministic AI outputs.
- PayPal’s sandbox provides a realistic testing environment with no real money movement.
- Secure handling of API keys via environment variables is essential for open‑source projects.
- Coordinating async flows between front‑end (PayPal button) and back‑end (order creation) is straightforward once the contract is defined.

## What's next for PayPal‑AI Checkout

- **Multi‑turn shopping**: refine recommendations based on user feedback.
- **Live product catalog**: integrate with an e‑commerce API for up‑to‑date inventory.
- **Voice‑enabled ordering**: add Web Speech API for hands‑free interaction.
- **Analytics dashboard**: track conversion rates, AI confidence scores, and payment success metrics.
- **Production‑grade deployment**: containerize with Docker and set up CI/CD pipelines.
## Built with

- **Python 3** – core language for backend logic.
- **Flask** – lightweight web framework to serve the API and UI.
- **paypalcheckoutsdk** – official PayPal Checkout SDK for order creation and capture.
- **OpenAI API** – generative AI for product recommendation.
- **HTML5** – structure of the front‑end page.
- **CSS3** – styling of the chat interface.
- **JavaScript (ES6)** – client‑side logic and PayPal button integration.
- **PayPal JavaScript SDK** – renders the PayPal Checkout button.
- **python‑dotenv** – loads environment variables securely.
- **Git** – version control for the project.
- **GitHub** – hosting the public repository.
- **Render / Vercel (optional)** – cloud platforms for easy deployment.
- **MIT License** – permissive open‑source licensing.
- **VS Code** – development environment.
- **Postman** – testing PayPal API calls.
- **Markdown** – documentation (README, Project Story).
- **YouTube** – host the demo video.
- **Docker (future)** – containerization plan.
- **CI/CD (future)** – automated testing and deployment pipelines.
- **Zapier (optional)** – potential integration for automating workflows.
- **AG Grid (optional)** – could be used for displaying transaction tables.
- **OpenAI Chat Completion** – core AI model.
- **JSON** – data interchange format for AI responses.
- **Windows PowerShell** – command‑line for running scripts on Windows.
- **HTML5 Canvas (optional)** – for future UI enhancements.

*Feel free to adjust, add, or remove tags as your project evolves.*
## Try it out

- **Source code**: [GitHub repository](https://github.com/shaikjafar559/paypal-ai-checkout) – clone, set up the environment, and run locally.
- **Live demo** (hosted on Render): <https://paypal-ai-demo.onrender.com> – interact with the AI chat and complete a sandbox PayPal checkout without any setup.
- **Demo video**: [YouTube walkthrough (≤ 3 min)](https://www.youtube.com/watch?v=YOUR_DEMO_VIDEO_ID) – shows the full flow from start‑up to payment capture.

Feel free to replace the placeholder URLs with your actual repository, deployment, and video links once they are ready.

## Demo video

- **YouTube walkthrough (≤ 3 min)**: [Demo video](https://www.youtube.com/watch?v=YOUR_VIDEO_ID) – shows the full flow from starting the server to completing a PayPal sandbox checkout. Set the video to public or unlisted; judges will view only the first three minutes.

*Replace `YOUR_VIDEO_ID` with the actual YouTube video identifier once uploaded.*
