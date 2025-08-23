#!/usr/bin/env python3

from PIL import Image
from colorama import Fore, Style, init
import exifread
import folium
import os
import sys
import readline
import glob

# TAB Autocomplete Setup
def complete_path(text, state):
    """Autocomplete file paths when pressing TAB"""
    line = readline.get_line_buffer().split()
    if not line:
        return [c + os.sep if os.path.isdir(c) else c for c in glob.glob(text + '*')][state]
    else:
        return [c + os.sep if os.path.isdir(c) else c for c in glob.glob(text + '*')][state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete_path)

#  Convert GPS to Degrees 
def convert_to_degrees(value):
    d, m, s = value.values
    return float(d.num / d.den) + float(m.num / m.den) / 60 + float(s.num / s.den) / 3600

# Extract Metadata Function 
def extract_metadata(file_path):
    report_lines = []

    # --- File Information ---
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)  # in bytes
    file_size_kb = round(file_size / 1024, 2)

    # Open image to get width, height, color mode
    image = Image.open(file_path)
    width, height = image.size
    megapixels = round((width * height) / 1_000_000, 3)
    color_space = "sRGB" if image.mode == "RGB" else image.mode

    report_lines.append("\n=== File Information ===")
    report_lines.append(f"Name:\t{file_name}")
    report_lines.append(f"File size:\t{file_size_kb} KB ({file_size} bytes)")
    report_lines.append("File type:\tJPEG/PNG")
    report_lines.append("MIME type:\timage/jpeg or image/png")
    report_lines.append(f"Image size:\t{width} x {height} ({megapixels} megapixels)")
    report_lines.append(f"Color space:\t{color_space}")

    # Metadata Extraction
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)

    report_lines.append("\n=== Privacy-Sensitive Metadata ===")

    device_tags = {
        "Image Make": "Camera Make",
        "Image Model": "Camera Model",
        "Image Orientation": "Orientation",
        "Image XResolution": "X Resolution",
        "Image YResolution": "Y Resolution",
        "Image ResolutionUnit": "Resolution Unit",
        "Image Software": "Software",
        "Image DateTime": "Date/Time",
        "Image YCbCrPositioning": "YCbCr Positioning",
    }

    for tag, label in device_tags.items():
        if tag in tags:
            report_lines.append(f"{label}: {tags[tag]}")

    # Collect GPS data
    gps_tags = [
        "GPS GPSLatitudeRef",
        "GPS GPSLatitude",
        "GPS GPSLongitudeRef",
        "GPS GPSLongitude",
        "GPS GPSAltitudeRef",
        "GPS GPSTimeStamp",
        "GPS GPSSatellites",
        "GPS GPSImgDirectionRef",
        "GPS GPSMapDatum",
        "GPS GPSDate",
        "Image GPSInfo"
    ]

    gps_data = {}
    for tag in gps_tags:
        if tag in tags:
            gps_data[tag] = tags[tag]

    if gps_data:
        report_lines.append("\n[!] GPS Data Found:")
        for tag, value in gps_data.items():
            report_lines.append(f"{tag}: {value}")

        if "GPS GPSLatitude" in gps_data and "GPS GPSLongitude" in gps_data:
            lat = convert_to_degrees(gps_data["GPS GPSLatitude"])
            lon = convert_to_degrees(gps_data["GPS GPSLongitude"])

            if str(tags.get("GPS GPSLatitudeRef")) != "N":
                lat = -lat
            if str(tags.get("GPS GPSLongitudeRef")) != "E":
                lon = -lon

            report_lines.append(f"[+] Coordinates: {lat}, {lon}")

            # Create and save map
            map_osm = folium.Map(location=[lat, lon], zoom_start=15)
            folium.Marker([lat, lon], popup=file_name).add_to(map_osm)

            html_map = os.path.splitext(file_name)[0] + "_location.html"
            map_osm.save(html_map)
            report_lines.append(f"[+] Location map saved as: {html_map}")
    else:
        report_lines.append("\n[!] No GPS data found.")

    print("\n".join(report_lines))

    # Save report to file
    report_file = os.path.splitext(file_name)[0] + "_metadata_report.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"\n[+] Metadata report saved as: {report_file}")

#Remove Metadata Function
def remove_metadata(file_path):
    image = Image.open(file_path)
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)

    clean_path = "clean_" + os.path.basename(file_path)
    image_without_exif.save(clean_path)
    print(f"[+] Metadata removed. Clean image saved as: {clean_path}")

# Main Program
init(autoreset=True)

if __name__ == "__main__":
    print("\n" + Fore.GREEN + Style.BRIGHT + "="*60)
    print(Fore.GREEN + Style.BRIGHT + "      Image Metadata Extractor & Remover     ")
    print(Fore.GREEN + Style.BRIGHT + "="*60 + "\n")

    # File path input (BOLD)
    file_path = input(Fore.YELLOW + Style.BRIGHT + "\nEnter image file path: " + Style.RESET_ALL)

    # File extension validation
    valid_exts = [".jpg", ".jpeg", ".png"]
    if not any(file_path.lower().endswith(ext) for ext in valid_exts):
        print(Fore.RED + Style.BRIGHT + f"\n[!] Unsupported file type. Only {valid_exts} are allowed.")
        sys.exit(1)

    # Options (BOLD)
    print("\n" + Fore.CYAN + Style.BRIGHT + "Choose an option:")
    print(Fore.CYAN + Style.BRIGHT + "1. Extract privacy-sensitive metadata")
    print(Fore.CYAN + Style.BRIGHT + "2. Remove all metadata")
    choice = input(Fore.YELLOW + Style.BRIGHT + "Enter choice (1 or 2): " + Style.RESET_ALL)

    if choice == "1":
        extract_metadata(file_path)
    elif choice == "2":
        remove_metadata(file_path)
    else:
        print(Fore.RED + "[!] Invalid choice")
