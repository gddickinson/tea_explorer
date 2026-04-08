"""
Screenshot Generator for Tea Explorer
Launches the app, navigates to each tab, and saves screenshots
using macOS Quartz CoreGraphics.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
import time as time_mod
from pathlib import Path
from PIL import Image
import io

# Ensure we're in the project directory
os.chdir(Path(__file__).parent)

from main import TeaExplorerEnhanced


def capture_window(root, filename):
    """Capture the main window using Quartz CoreGraphics."""
    import Quartz.CoreGraphics as CG

    root.update_idletasks()
    root.update()
    time_mod.sleep(0.4)
    root.update()

    # Get window geometry
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    w = root.winfo_width()
    h = root.winfo_height()

    # Account for title bar
    title_bar = 28

    # Capture the screen region
    # CGWindowListCreateImage captures a rectangular region
    region = CG.CGRectMake(x, y - title_bar, w, h + title_bar)
    image = CG.CGWindowListCreateImage(
        region,
        CG.kCGWindowListOptionOnScreenOnly,
        CG.kCGNullWindowID,
        CG.kCGWindowImageDefault
    )

    if image is None:
        print(f"  Error: Could not capture {filename}")
        return

    img_w = CG.CGImageGetWidth(image)
    img_h = CG.CGImageGetHeight(image)

    # Convert CGImage to PNG data
    bitmap_rep = CG.CGBitmapContextCreate(
        None, img_w, img_h, 8, 0,
        CG.CGColorSpaceCreateDeviceRGB(),
        CG.kCGImageAlphaPremultipliedFirst | CG.kCGBitmapByteOrder32Little
    )
    CG.CGContextDrawImage(bitmap_rep, CG.CGRectMake(0, 0, img_w, img_h), image)

    # Use a different approach - save via NSBitmapImageRep
    import Quartz
    from Cocoa import NSBitmapImageRep, NSPNGFileType

    # Create NSBitmapImageRep from CGImage
    bitmap = NSBitmapImageRep.alloc().initWithCGImage_(image)
    png_data = bitmap.representationUsingType_properties_(NSPNGFileType, None)
    png_data.writeToFile_atomically_(filename, True)

    # Resize for README if needed
    img = Image.open(filename)
    max_width = 1400
    if img.width > max_width:
        ratio = max_width / img.width
        new_h = int(img.height * ratio)
        img = img.resize((max_width, new_h), Image.Resampling.LANCZOS)
        img.save(filename)

    final = Image.open(filename)
    print(f"  Saved: {filename} ({final.width}x{final.height})")


def generate_screenshots():
    """Generate all screenshots for the README."""
    print("Starting Tea Explorer for screenshots...")

    root = tk.Tk()
    app = TeaExplorerEnhanced(root)

    # Bring window to front
    root.lift()
    root.attributes('-topmost', True)
    root.update_idletasks()
    root.update()
    time_mod.sleep(0.5)
    root.attributes('-topmost', False)
    root.update()

    # Wait for full render
    time_mod.sleep(1)
    root.update()

    screenshots_dir = Path("screenshots")

    print("Capturing screenshots...")

    # 1. Tea Browser tab (default) - select a tea to show details
    if app.tea_listbox.size() > 0:
        app.tea_listbox.selection_set(0)
        app.tea_listbox.event_generate("<<ListboxSelect>>")
        root.update_idletasks()
        root.update()
    capture_window(root, str(screenshots_dir / "tea_browser.png"))

    # 2. Blends tab
    app.notebook.select(1)
    root.update_idletasks()
    root.update()
    if app.blend_listbox.size() > 0:
        app.blend_listbox.selection_set(0)
        app.blend_listbox.event_generate("<<ListboxSelect>>")
        root.update_idletasks()
        root.update()
    capture_window(root, str(screenshots_dir / "blends_browser.png"))

    # 3. Cultivars tab
    app.notebook.select(2)
    root.update_idletasks()
    root.update()
    if app.cultivar_listbox.size() > 0:
        app.cultivar_listbox.selection_set(0)
        app.cultivar_listbox.event_generate("<<ListboxSelect>>")
        root.update_idletasks()
        root.update()
    capture_window(root, str(screenshots_dir / "cultivars_browser.png"))

    # 4. Brands tab
    app.notebook.select(3)
    root.update_idletasks()
    root.update()
    if app.company_listbox.size() > 0:
        app.company_listbox.selection_set(0)
        app.company_listbox.event_generate("<<ListboxSelect>>")
        root.update_idletasks()
        root.update()
    capture_window(root, str(screenshots_dir / "brands_browser.png"))

    # 5. Tisanes tab
    app.notebook.select(4)
    root.update_idletasks()
    root.update()
    if app.tisane_listbox.size() > 0:
        app.tisane_listbox.selection_set(0)
        app.tisane_listbox.event_generate("<<ListboxSelect>>")
        root.update_idletasks()
        root.update()
    capture_window(root, str(screenshots_dir / "tisanes_browser.png"))

    # 6. Journal tab
    app.notebook.select(5)
    root.update_idletasks()
    root.update()
    capture_window(root, str(screenshots_dir / "journal.png"))

    # 7. Brewing timer tab
    app.notebook.select(6)
    root.update_idletasks()
    root.update()
    app.set_timer(180)
    root.update_idletasks()
    root.update()
    capture_window(root, str(screenshots_dir / "brewing_timer.png"))

    # 8. Dashboard tab
    app.notebook.select(8)
    root.update_idletasks()
    root.update()
    capture_window(root, str(screenshots_dir / "dashboard.png"))

    # 9. Map tab
    app.notebook.select(11)
    root.update_idletasks()
    root.update()
    capture_window(root, str(screenshots_dir / "world_map.png"))

    print(f"\nAll screenshots saved to {screenshots_dir}/")
    print("Done!")

    root.destroy()


if __name__ == "__main__":
    generate_screenshots()
