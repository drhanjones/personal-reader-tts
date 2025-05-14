# PDF-to-HTML Reader & TTS

A simple full-stack app to upload PDFs, convert them into audio using a TTS engine (To be decided, most probably kokoro) and listen to them in the browser. Also convert to HTML, browse pages in a web reader to use Edge's in-built read aloud feature? Also learn Vue + TypeScript (HTML + CSS) on the front-end and FastAPI on the back-end.

---

## 🚀 Why This Project?

I’m a AI Engineer, and I wanted to learn:  
- **Vue 3 + TypeScript** for the front-end creation
- **FastAPI** becuase after Django and Flask I want to learn a new back-end framework
- Real-world file-upload, processing, pagination, and audio streaming  
- Also try a bit of vibecoding(???????) 

---

## 🔧 To Run

1. **Back-end**  
   
       cd backend  
       pip install -r requirements.txt  
       fastapi dev main.py

2. **Front-end**  
   
       cd frontend  
       npm install  
       npm run dev

---

## 🛣️ Roadmap & Learning Plan

- [x] File upload & list  
- [x] On-demand PDF→HTML conversion  
- [x] Paginated HTML reader  
- [x] Stub audio player with `<audio controls>`  
- [x] Custom `LandscapeAudioPlayer.vue` with full UI
- [ ]  Back end TTS engine integration
- [ ]  Change structure of app with a longer potrait mode audio player on left side with a "Reader" in the middle and file management on the right side
- [ ]  Improve HTML generation where instead of one index.html file, generate one file per page


---


