#!/usr/bin/env python3

from PIL import Image
from colorama import Fore, Style, init
import exifread
import folium
import os
import readline
import glob

# Enable TAB autocompletion for file paths
def complete(text, state):
    return (glob.glob(text + '*') + [None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)


# Helper: Convert GPS to Degrees
def convert_to_degrees(value):
    d, m, s = value.values
    return float(d.num / d.den) + float(m.num / m.den) / 60 + float(s.num / s.den) / 3600


# Extract Metadata Function
def extract_metadata(file_path):
    report_lines = []  # Collect output for saving into a file

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
    report_lines.append("File type:\tJPEG")
    report_lines.append("MIME type:\timage/jpeg")
    report_lines.append(f"Image size:\t{width} x {height} ({megapixels} megapixels)")
    report_lines.append(f"Color space:\t{color_space}")

    # --- Metadata Extraction ---
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)

    report_lines.append("\n=== Privacy-Sensitive Metadata ===")

    # Only show important camera/device properties
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

    # Show GPS info
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

    # Print report
    print("\n".join(report_lines))

    # Save report to file
    report_file = os.path.splitext(file_name)[0] + "_metadata_report.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"\n[+] Metadata report saved as: {report_file}")


# Remove Metadata Function
def remove_metadata(file_path):
    image = Image.open(file_path)
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)

    clean_path = "clean_" + os.path.basename(file_path)
    image_without_exif.save(clean_path)
    print(f"[+] Metadata removed. Clean image saved as: {clean_path}")


# Initialize colorama
init(autoreset=True)

# Main Program
if __name__ == "__main__":
    # Big Green Title
    print("\n" + Fore.GREEN + Style.BRIGHT + "="*60)
    print(Fore.GREEN + Style.BRIGHT + "      Image Metadata Extractor & Remover     ")
    print(Fore.GREEN + Style.BRIGHT + "="*60 + "\n")

    file_path = input("\nEnter image file path: ")

    print("\nChoose an option:")
    print("1. Extract privacy-sensitive metadata")
    print("2. Remove all metadata")
    choice = input("Enter choice (1 or 2): ")

    if choice == "1":
        extract_metadata(file_path)
    elif choice == "2":
        remove_metadata(file_path)
    else:
        print(Fore.RED + "[!] Invalid choice")

