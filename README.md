# 🛡️ IMER – Image Metadata Extractor & Remover
A lightweight Python toolkit to **extract** and **remove** image metadata (EXIF, GPS, privacy-sensitive information).  
Also generates an **interactive map (.html)** from GPS coordinates if found in the image.

---

## 🚀 Features  
- 🔍 Extracts **all EXIF metadata** from images (JPEG, PNG, etc.)
- 🌍 Detects **GPS coordinates** and saves an interactive **map (HTML)** with the image’s location
- 🧹 Removes **all metadata** (privacy protector) and saves a clean copy
- 📷 Displays **image details** like file size, type, resolution, and color space
---

## 📦 Installation  

### Requirements  
This project needs Python 3 and the following libraries:  

- pillow
- exifread
- piexif
- folium


Install them with:  
```bash
pip install -r requirements.txt
 ```

## ⚡ Run the Tool

Option 1: Direct Python
```bash
python3 imer.py
```
Option 2: As a Linux Command

1. Rename the file to imer (remove .py)
2.Add shebang at the top:
```bash
#!/usr/bin/env python3
```
3. Make it executable:
```bash
chmod +x imer
```
Move to system path:
```bash
sudo mv imer /usr/local/bin/
```
✅ Now run from anywhere:
```bash
imer
```
## 🛠️ Usage
When you run imer, choose one of the options:
```bash
=== Digital Forensics Image Metadata Toolkit ===

Enter image file path: example.jpg

Choose an option:
1. Extract privacy-sensitive metadata
2. Remove all metadata

```
Option 1 → Extracts metadata + saves GPS map if found (image_location.html)

Option 2 → Removes all metadata and saves as clean_example.jpg

## 📂 Project Structure

```bash

image-metadata-tool/
│── main.py              # Main program file
│── requirements.txt     # Dependencies list
│── README.md            # Documentation (this file)
│── .gitignore           # Ignore unnecessary files
```


## 🔒 Why This Project?

Digital photos often contain hidden metadata (EXIF, GPS, IPTC).
This can reveal sensitive details such as your location or device information when sharing online.
This tool helps protect your privacy by cleaning or extracting that data safely

## 🤝 Contributing

Pull requests and suggestions are welcome!
If you find a bug, open an issue on GitHub.


## License

[MIT](https://github.com/Kirtan7/Image-Metadata-Extractor-Remover?tab=MIT-1-ov-file#)


