# Gemini Knowledge-Based Chatbot (Streamlit)

A simple Streamlit web app version of your command-line Gemini knowledge-based chatbot.

## 1. Install Python
Use Python 3.10 or newer.

## 2. Open the project folder
Open a terminal in this folder.

## 3. Install the packages
```bash
pip install -r requirements.txt
```

## 4. Add your Gemini API key
1. Open the `.streamlit` folder.
2. Rename `secrets.toml.example` to `secrets.toml`.
3. Replace the placeholder with your actual Gemini API key:

```toml
GEMINI_API_KEY = "YOUR_REAL_GEMINI_API_KEY"
```

Keep `secrets.toml` private. Do not upload it to GitHub or share it publicly.

## 5. Run the chatbot
```bash
streamlit run app.py
```

The app will open in your browser. Paste your knowledge/manual and system instruction in the sidebar, then ask questions in the chat box.

## 6. Deploy on Streamlit Community Cloud
1. Upload the project files to a GitHub repository.
2. Create a new app at https://share.streamlit.io/.
3. Select your repository and set the main file path to `app.py`.
4. In the app's **Settings → Secrets**, add:

```toml
GEMINI_API_KEY = "YOUR_REAL_GEMINI_API_KEY"
```

5. Deploy the app.

## Notes
- The default model is `gemini-2.5-flash`. You can change it in the sidebar if your API account supports another model.
- The chatbot uses the manual as its reference material and keeps chat history during the current session.
- Never paste your real API key into `app.py`.
