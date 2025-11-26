# 🖼️ Smart Photo Finder

**AI-powered semantic image search that runs 100% offline**

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NexaAI](https://img.shields.io/badge/Powered%20by-NexaAI-green)](https://nexa.ai)
[![Project Status](https://img.shields.io/badge/status-prototype-orange.svg)](https://github.com)

> Find images by describing what you're looking for, not by filename or tags. Powered by vision-language models and semantic embeddings.

<!-- [Demo](#-demo) • [Features](#-features) • [Quick Start](#-quick-start) • [Documentation](docs/USAGE.md) -->
[Documentation](docs/USAGE.md)
---

## 📊 Quick Stats

- ⚡ **Search Speed**: <0.1s per query (1000 images)
- 🎯 **Accuracy**: Semantic understanding via 384D embeddings
- 💾 **Storage**: ~50KB per image (description + embedding)
- 🔒 **Privacy**: 100% local, zero cloud APIs
- 💰 **Cost**: $0 (no API fees)

---

## 🎯 Why This Project?

Traditional photo apps search by:
- ❌ Filename ("IMG_1234.jpg")
- ❌ Manual tags (tedious)
- ❌ Date/location only

**This app searches by meaning:**
- ✅ "person holding camera" → finds photographer photos
- ✅ "sunset on beach" → understands context
- ✅ "colorful bird" → semantic understanding
- ✅ Works 100% offline, completely private

---

## ✨ Features

### Core Functionality
- 🤖 **AI Vision**: Generates detailed image descriptions using NexaAI VLM
- 🔢 **Semantic Embeddings**: Converts descriptions to 384D vectors
- 🔍 **Smart Search**: Find images by meaning, not keywords
- 💾 **Local Storage**: All data stays on your device (JSON database)

### Technical Features
- 🏗️ **Modular Architecture**: Clean separation of concerns
- 📝 **Logging**: Track processing and debug easily
- ⚡ **Efficient**: Batch processing with progress tracking
- 🔒 **Privacy-First**: Zero cloud APIs, 100% offline
- 💰 **Cost-Free**: No API keys or subscriptions needed

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Vision AI** | NexaAI Qwen3-VL-4B (Q4_0 GGUF) | Describes images in natural language |
| **Embeddings** | all-MiniLM-L6-v2 | Converts text to 384D vectors |
| **Search** | Cosine Similarity | Finds semantically similar images |
| **Storage** | JSON | Local, private database |
| **Language** | Python 3.10 | Core implementation |

---

## 📋 Requirements

### System Requirements
- **Python**: 3.10 (recommended for NexaAI compatibility)
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: ~5GB for model downloads
- **OS**: Windows/Linux/macOS
- **CPU/GPU**: CPU works fine (GPU optional but faster)

<!-- ### Python Dependencies
- **NexaAI SDK**: ≥ 0.5.x
- **sentence-transformers**: ≥ 2.6.x
- **numpy**: ≥ 1.24.0
- **Pillow**: ≥ 10.0.0
- **tqdm**: ≥ 4.66.0 -->

### GPU (Optional)
- CUDA 12+ with compatible PyTorch build
- Significantly faster processing (~5x speed improvement)
- Works perfectly fine in CPU-only mode

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone <repo-url>
cd <folder-name>
```

### 2. Create virtual environment (Python 3.10 required!)

**Option A — Using Conda (Recommended)**
```bash
# Create environment
conda create -n photofinder python=3.10

# Activate
conda activate photofinder
```

**Option B — Using venv**
```bash
# Create environment
python3.10 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify installation
```bash
python -c "from nexaai.vlm import VLM; print('✅ NexaAI installed')"
python -c "from sentence_transformers import SentenceTransformer; print('✅ Embeddings ready')"
```

### 5. Run the app
```bash
python app.py
```

You'll see:
```
1. Process images
2. Search images
3. Exit
```

---

## 💡 Usage Examples

### Process Your Images
1. Select "Process images" from menu
2. Enter folder path (e.g., `my_photos/`)
<!-- 3. Wait for processing (first time downloads models ~5GB) -->
3. Wait for processing (first time downloads models)
4. Database created at `data/image_database.json`

### Search Your Photos
```
Menu > Search images

🔍 Search: sunset on beach
# Returns ranked results with similarity scores

🔍 Search: person smiling
# Finds photos matching the description

🔍 Search: red car
# Semantic understanding of objects and colors
```

**For detailed usage guide, see [USAGE.md](docs/USAGE.md)**

---

<!-- ## 🎬 Demo

**Search Example:**
```
🔍 Search: person with camera

Results:
🔥 Rank 1 | 85.2% match
   📸 photographer.jpeg
   💬 A person holding a professional camera in outdoor setting...

🔥 Rank 2 | 78.9% match
   📸 wedding_shoot.jpg
   💬 Photographer capturing moments at an event...
``` -->

---

## 📁 Folder Structure

```
smart-photo-finder/
│
├── app.py                          # Main CLI application
├── config.py                       # Configuration settings
├── logger.py                       # Logging setup
├── requirements.txt                # Python dependencies
│
├── services/                       # Core services
│   ├── vlm_service.py             # Vision-Language Model
│   ├── embedder_service.py        # Embedding generation
│   └── image_processor_service.py # Image processing pipeline
│
├── utils/                          # Utility functions
│   ├── file_utils.py              # File operations
│   └── json_db.py                 # JSON database handler
│
├── search/                         # Search functionality
│   ├── indexer.py                 # Index builder
│   └── search_engine.py           # Search logic
│
├── data/                           # Data storage
│   └── image_database.json        # Image metadata + embeddings
│
└── docs/                           # Documentation
    ├── USAGE.md                   # Detailed usage guide
    └── TROUBLESHOOTING.md         # Common issues & solutions
```

---

## 🔧 Quick Troubleshooting

**Models not downloading?**
```bash
# Manual download
nexa pull NexaAI/Qwen3-VL-4B-Instruct-GGUF
```

**Python version issues?**
```bash
# Check version (must be 3.10.x)
python --version
```

**Out of memory?**
- Process images in smaller batches
- Close other applications
- Try GPU if available

**For complete troubleshooting guide, see [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**

---

## ⚠️ Known Limitations

- **VLM Processing**: CPU inference is slow (~20–30s per image)
- **GPU Support**: Requires CUDA + PyTorch setup
- **Database**: JSON not ideal for >5k images (FAISS recommended for larger collections)
- **First Run**: Models download automatically ( one-time)
<!-- - **First Run**: Models download automatically (~5GB, one-time) -->

---

## 🗺️ Roadmap

### v1.0 (Current) ✅
- [x] Image description generation
- [x] Semantic embeddings
- [x] JSON database
- [x] CLI interface
- [x] Modular architecture

### v1.1 (In Progress) 🚧
- [ ] Gradio web UI
- [ ] Batch processing improvements
- [ ] Progress bars & better UX
- [ ] GPU acceleration docs

### v2.0 (Planned) 📋
- [ ] FAISS for faster search (10K+ images)
- [ ] Benchmarking script
- [ ] Image clustering & auto-albums
- [ ] Android mobile app
- [ ] Multi-language support

---

## 📚 Documentation

- [Detailed Usage Guide](docs/USAGE.md) - Step-by-step instructions
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues & fixes
- [NexaAI Builder Bounty](https://docs.nexa.ai/community/builder-bounty) - About the program

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Open issues for bugs or feature requests.

---

## 🙏 Credits

Built as part of the [NexaAI Builder Bounty Program](https://docs.nexa.ai/community/builder-bounty)

**Powered by:**
- [NexaAI](https://nexa.ai) - Local AI inference
- [Sentence Transformers](https://www.sbert.net/) - Text embeddings
- [Qwen3-VL](https://huggingface.co/Qwen) - Vision-language model

**Inspired by:** The need for private, offline photo search without cloud dependencies

---

## 📄 License

MIT License - Free to use for learning and personal projects.

See [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

Built by **Pankaj Kumar Goyal**

- 🐙 GitHub: [Pankaj4152](https://github.com/pankaj4152)
- 🐦 Twitter/X: [@Pankaj4152](https://x.com/Pankaj41521)
- 💼 LinkedIn: [Pankaj4152](https://www.linkedin.com/in/pankaj4152)

---

## 🌟 Support

If you find this project helpful:
- ⭐ Star this repo
- 🐛 Report bugs via Issues
- 💡 Suggest features
- 🔀 Submit PRs

---

## 📈 Project Status

**Early Prototype** - Core pipeline works (caption → embedding → search).

Actively improving and adding new features. Follow the repo for updates!

---

**#buildinpublic** | **#NexaAI** | **#LocalAI** | **#ComputerVision**

---

Made with ❤️ using NexaAI • 100% Offline • Zero Cloud APIs