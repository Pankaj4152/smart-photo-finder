# 📖 Usage Guide - Smart Photo Finder

Complete guide to using Smart Photo Finder effectively.

---

## Table of Contents

1. [First-Time Setup](#first-time-setup)
2. [Processing Images](#processing-images)
3. [Searching Images](#searching-images)
4. [Understanding Results](#understanding-results)
5. [Advanced Usage](#advanced-usage)
6. [Best Practices](#best-practices)

---

## First-Time Setup

### 1. Verify Installation

After installing dependencies, verify everything works:

```bash
# Test NexaAI
python -c "from nexaai.vlm import VLM; print('✅ NexaAI ready')"

# Test Sentence Transformers
python -c "from sentence_transformers import SentenceTransformer; print('✅ Embeddings ready')"

# Test all imports
python -c "import config, logger; print('✅ All modules ready')"
```

### 2. Prepare Your Images

Organize your photos in a folder:

```
my_photos/
├── vacation/
│   ├── beach.jpg
│   ├── mountains.png
│   └── sunset.jpeg
├── family/
│   └── birthday.jpg
└── pets/
    ├── dog.jpg
    └── cat.png
```

**Supported formats:**
- `.jpg`, `.jpeg`
- `.png`
- `.webp`
- `.bmp`

---

## Processing Images

### Basic Processing

1. **Start the app:**
```bash
python app.py
```

2. **Select option 1 (Process images)**

3. **Enter folder path:**
```
Enter the folder path to process: my_photos/
```

4. **Wait for processing:**
```
Processing: 100%|████████████| 42/42 [02:15<00:00,  3.21s/img]
✅ Processed 42 images successfully
💾 Database saved to: data/image_database.json
```

### What Happens During Processing?

1. **Image Discovery** - Scans folder recursively for supported formats
2. **VLM Analysis** - Generates detailed descriptions
3. **Embedding Creation** - Converts descriptions to 384D vectors
4. **Database Storage** - Saves metadata as JSON

### Processing Time Estimates

**CPU Mode:**
- Small batch (10 images): ~3-5 minutes
- Medium batch (50 images): ~15-20 minutes
- Large batch (200 images): ~1-2 hours

**GPU Mode** (if configured):
- ~5x faster than CPU
- Small batch: ~1 minute
- Large batch: ~15-20 minutes

### First Run Notes

**Models will download automatically (~5GB):**
- `NexaAI/Qwen3-VL-4B-Instruct-GGUF` (~3.7GB)
- `sentence-transformers/all-MiniLM-L6-v2` (~80MB)

This happens only once. Subsequent runs use cached models.

---

## Searching Images

### Basic Search

1. **Start the app and select option 2**

2. **Enter your query:**
```
 Enter search query: sunset on beach
```

3. **View results:**
<!-- ```
🔥 Rank 1 | Score: 0.8521 (85.2% match)
📸 File: vacation/beach_sunset.jpg
📁 Path: /home/user/my_photos/vacation/beach_sunset.jpg
💬 Description: A beautiful sunset over ocean waters with orange and 
   pink hues reflecting on the calm sea surface...
────────────────────────────────────────────────────

🔥 Rank 2 | Score: 0.7843 (78.4% match)
📸 File: vacation/evening_beach.jpg
📁 Path: /home/user/my_photos/vacation/evening_beach.jpg
💬 Description: Evening scene at a sandy beach with golden light...
────────────────────────────────────────────────────
``` -->

### Search Query Examples

**Natural Language:**
```
✅ "person holding camera"
✅ "sunset on beach"
✅ "colorful bird"
✅ "group of friends laughing"
✅ "red car on street"
```

**Descriptive Phrases:**
```
✅ "outdoor landscape with mountains"
✅ "indoor scene with furniture"
✅ "food on a plate"
✅ "architectural building"
```

**Avoid:**
```
❌ "IMG_1234" (filenames)
❌ "#vacation" (hashtags)
❌ "2024-05-20" (dates)
```

### Understanding Similarity Scores

| Score Range | Match Quality | Description |
|-------------|---------------|-------------|
| 0.85 - 1.0 | Excellent ✨ | Very close semantic match |
| 0.70 - 0.84 | Good ✓ | Strong relevance |
| 0.50 - 0.69 | Moderate ~ | Some relevance |
| < 0.50 | Weak ✗ | Low relevance |

---

## Understanding Results

### Result Format

Each result shows:

```
[0.8521]    images/photo.jpg
   ↑              ↑  
Cosine Score  Filepath
```

### Similarity Score Calculation

**How it works:**
1. Your query is converted to a 384D vector
2. Each image's description has a 384D vector
3. Cosine similarity measures angle between vectors
4. Score = 1 - (angle / π)

**Range:** -1.0 to 1.0 (we show 0.0 to 1.0)

---

## Advanced Usage

### Adjusting Search Sensitivity

Edit `config.py`:

```python
# Show more results (lower threshold)
min_similarity = 0.3  # Default: 0.5

# Show fewer results (higher threshold)
min_similarity = 0.7

# Show more top results
top_k = 10  # Default: 5
```
<!-- 
### Batch Processing Multiple Folders

Create a script:

```python
from services.image_processor_service import ImageProcessorService

folders = [
    "photos/2023",
    "photos/2024", 
    "downloads/images"
]

processor = ImageProcessorService()

for folder in folders:
    print(f"Processing: {folder}")
    processor.process_images(folder)
```

### Export Search Results

Modify `search/search_engine.py` to save results:

```python
import json

def search_and_export(query, output_file="results.json"):
    results = search_images(query)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved to {output_file}")
```

--- -->

## Best Practices

### 📸 For Better Image Descriptions

**Good:**
- ✅ Clear, well-lit images
- ✅ Single subject/scene
- ✅ High resolution (>500px)

**Avoid:**
- ❌ Very blurry images
- ❌ Extremely dark photos
- ❌ Heavily corrupted files

###  For Better Search Results

**Do:**
- ✅ Use descriptive phrases ("person running in park")
- ✅ Describe visual content, not metadata
- ✅ Try different phrasings if results are poor
- ✅ Process images in batches (not all at once)

**Don't:**
- ❌ Use only single words ("dog", "car")
- ❌ Search for filenames or dates
- ❌ Expect perfect results for abstract concepts
- ❌ Mix multiple unrelated concepts

<!-- ### 💾 Database Management

**Regular maintenance:**
```bash
# Check database size
ls -lh data/image_database.json

# Backup before reprocessing
cp data/image_database.json data/backup_$(date +%Y%m%d).json
``` -->

**When to reprocess:**
- Added many new images
- Changed VLM model
- Updated embedding model
- Database seems corrupted

---

## Performance Tips

### For Faster Processing

1. **Use GPU** (if available)
   - Install CUDA + PyTorch with GPU support
   - 5x faster than CPU

2. **Batch Smaller Folders**
   - Process 50-100 images at a time
   - Prevents memory issues

3. **Close Other Apps**
   - Free up RAM
   - Especially during VLM inference

### For Better Search Speed

**Current: JSON Database**
- Good for: <5,000 images
- Search time: <0.1s

**Future: FAISS Index**
- Good for: 10,000+ images
- Search time: <0.01s
- Planned for v2.0

---

## Workflow Examples

### Example 1: Vacation Photos

```bash
# 1. Process vacation folder
python app.py
> 1 (Process images)
> vacation_2024/

# 2. Search for beach scenes
python app.py
> 2 (Search images)
> sunset on beach

# 3. Search for activities
python app.py
> 2 (Search images)
> people swimming in ocean
```
<!-- 
### Example 2: Pet Photos

```bash
# Process
python app.py
> 1
> pets/

# Search
python app.py
> 2
> dog playing with ball

python app.py
> 2
> cat sleeping on couch
``` -->

---

## Next Steps

- ✅ Processed your images
- ✅ Learned to search effectively
- ✅ Understood results

**Now try:**
- Experimenting with different queries
- Processing more image folders
- Adjusting search thresholds
<!-- - Reading [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for issues -->

---

**Need help?** Open an issue on GitHub or check the troubleshooting guide.

**Want to contribute?** See main README for contribution guidelines.

---

[← Back to Main README](../README.md)