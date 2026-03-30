# 🐾 Dr. Paws – Real-Time AI Veterinary Voice Agent

## 🚀 Overview
Dr. Paws is a real-time AI-powered veterinary voice assistant designed to handle emergency triage and appointment scheduling seamlessly. It leverages LLM-based reasoning, real-time communication, and automated workflows to deliver fast and intelligent responses.

---

## 🧠 Key Features
- 🎙️ Real-time voice interaction using WebRTC
- ⚡ Sub-2s latency (speech → response)
- 🧠 LLM-based reasoning for clinical scenarios
- 🔄 Dynamic context switching (triage ↔ scheduling)
- 📅 Automated appointment booking system
- 🤖 Fully autonomous agent (no human intervention)

---

## 🏗️ Architecture Highlights
- Architected real-time voice agent swarm with LiveKit WebRTC, async tool-calling, and LLM-based reasoning; achieved sub-2s end-to-end speech-to-response latency across 6 clinical emergency scenarios.
- Orchestrated n8n webhooks + Supabase PostgreSQL for real-time slot booking; agent handles mid-conversation context switching between triage and scheduling modes with zero human intervention.

---

## 🛠️ Tech Stack
- **AI/LLM:** OpenAI / LLM APIs  
- **Voice:** LiveKit (WebRTC)  
- **Automation:** n8n  
- **Backend:** Node.js / Python  
- **Database:** Supabase (PostgreSQL)  

---

---

## ⚙️ Setup & Usage
1. Activate the virtual environment (venv)
2. Clone the repository  
3. Import workflow.json into n8n  
4. Configure API keys (Groq, LIvekit, etc.)  
5. Start LiveKit server  
6. Run the agent (python agent.py dev)

---

## 📸 Workflow
![Workflow](/images/)


---

## 🔮 Future Improvements
- Multi-language support 🌍  
- Advanced diagnostics models 🧬  
- Mobile app integration 📱  

---

## 🤝 Contributing
Pull requests are welcome!

---

## ⭐ Show Your Support
If you like this project, give it a ⭐ on GitHub!