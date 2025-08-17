# 🛡️ IMER – Image Metadata Extractor & Remover
A lightweight Python toolkit to **extract** and **remove** image metadata (EXIF, GPS, privacy-sensitive information).  
Also generates an **interactive map (.html)** from GPS coordinates if found in the image.

---
## 🔒 Why This Project?

Digital photos often contain hidden metadata (EXIF, GPS, IPTC).
This can reveal sensitive details such as your location or device information when sharing online.
This tool helps protect your privacy by cleaning or extracting that data safely

---
## 🚀 Features  
- 🔍 Extracts **all EXIF metadata** from images (JPEG, PNG, etc.)
- 🌍 Detects **GPS coordinates** and saves an interactive **map (HTML)** with the image’s location
- 🧹 Removes **all metadata** (privacy protector) and saves a clean copy
- 📷 Displays **image details** like file size, type, resolution, and color space
- 🎨 Colorful terminal output for better readability  
- ⚡ Run directly with `imer` command (after setup)  




## 🛠️ Installation  

### Option 1: For **Linux Users** 🐧


1.You don’t need to run pip manually. Just run the install.sh script and everything will be set up automatically.
```bash
git clone https://github.com/yourusername/imer.git
cd imer
chmod +x install.sh
./install.sh
```
✅ After installation, you can run the tool directly with:
```bash
imer
```
### Option 2: For **For Other Systems (Windows / macOS) 💻**
1.Clone the repository:
```bash
git clone https://github.com/yourusername/imer.git
cd imer
```
2.Install dependencies using ```bashrequirements.txt```:
```bash
pip install -r requirements.txt
```
3.Run the tool manually:
```bash
python3 imer.py
```

## 🛠️ Usage

You’ll see:

```bash
===  Image Metadata Extractor & Remover  ===

Enter image file path: example.jpg

Choose an option:
1. Extract privacy-sensitive metadata
2. Remove all metadata
Enter choice (1 or 2):

```
Option 1 → Extracts metadata + saves GPS map if found (image_location.html)

Option 2 → Removes all metadata and saves as clean_example.jpg






## 📜 License

[MIT](https://github.com/Kirtan7/Image-Metadata-Extractor-Remover?tab=MIT-1-ov-file#)

## 🤝 Contributing

Pull requests and suggestions are welcome!
If you find a bug, open an issue on GitHub.




