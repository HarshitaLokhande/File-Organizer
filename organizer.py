import os
import shutil
from datetime import datetime

categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Audio": [".mp3", ".wav"],
    "Code": [".py", ".java", ".cpp", ".c", ".html", ".css", ".js"],
    "Archives": [".zip", ".rar"],
    "Spreadsheets": [".xlsx", ".xls", ".csv"],
    "Presentations": [".ppt", ".pptx"],
    "Applications": [".exe", ".msi"]
}

UNDO_LOG = "undo_log.txt"


# ==============================
# ORGANIZE FILES (GUI VERSION)
# ==============================
def organize_files(folder_path):

    if not os.path.exists(folder_path):
        return "❌ Folder does not exist!"

    stats = {
        "Images": 0,
        "Documents": 0,
        "Videos": 0,
        "Audio": 0,
        "Code": 0,
        "Archives": 0,
        "Spreadsheets": 0,
        "Presentations": 0,
        "Applications": 0,
        "Others": 0
    }

    organized_count = 0

    log_path = os.path.join(folder_path, UNDO_LOG)

    with open(log_path, "w", encoding="utf-8") as log:

        for item in os.listdir(folder_path):

            full_path = os.path.join(folder_path, item)

            if os.path.isdir(full_path):
                continue

            if item in ["report.txt", UNDO_LOG]:
                continue

            ext = os.path.splitext(item)[1].lower()
            destination = "Others"

            for cat, exts in categories.items():
                if ext in exts:
                    destination = cat
                    break

            dest_folder = os.path.join(folder_path, destination)
            os.makedirs(dest_folder, exist_ok=True)

            filename, file_ext = os.path.splitext(item)
            new_path = os.path.join(dest_folder, item)

            counter = 1
            while os.path.exists(new_path):
                new_name = f"{filename}_{counter}{file_ext}"
                new_path = os.path.join(dest_folder, new_name)
                counter += 1

            try:
                shutil.move(full_path, new_path)
                log.write(f"{new_path}|{full_path}\n")

                organized_count += 1
                stats[destination] += 1

            except Exception as e:
                return f"❌ Error: {e}"

    # REPORT
    report_path = os.path.join(folder_path, "report.txt")

    with open(report_path, "w", encoding="utf-8") as report:
        report.write("SMART FILE ORGANIZER REPORT\n")
        report.write("=" * 40 + "\n\n")
        report.write(f"Date: {datetime.now()}\n\n")

        for k, v in stats.items():
            report.write(f"{k}: {v}\n")

        report.write(f"\nTotal Files: {organized_count}")

    return f"✅ Organized {organized_count} files successfully"


# ==============================
# UNDO FUNCTION (GUI VERSION)
# ==============================
def undo_organization(folder_path):

    log_path = os.path.join(folder_path, UNDO_LOG)

    if not os.path.exists(log_path):
        return "❌ No undo log found!"

    restored = 0

    with open(log_path, "r", encoding="utf-8") as log:
        lines = log.readlines()

    for line in reversed(lines):

        try:
            moved_path, original_path = line.strip().split("|")

            if os.path.exists(moved_path):
                shutil.move(moved_path, original_path)
                restored += 1

        except:
            continue

    return f"✅ Restored {restored} files"