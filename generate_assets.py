from PIL import Image, ImageDraw
import os

def create_pro_logo():
    # 1. Setup - High Resolution Canvas (1024x1024 for crispness)
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 2. Colors (Catppuccin Mocha Palette + Accents)
    night_color = "#89b4fa"  # Mocha Blue
    day_color = "#fab387"    # Mocha Peach
    bg_circle = "#1e1e2e"    # Dark Base

    # 3. Geometry
    # Define the bounding box for the main circle with padding
    padding = 50
    bbox = [padding, padding, size-padding, size-padding]

    # Draw the Base (The "Planet" or Container)
    draw.ellipse(bbox, fill=bg_circle)

    # 4. The "Day" Slash (Geometric Abstraction)
    # We draw a large rectangle rotated or a chord to slice the circle.
    # Simpler approach: Draw the Day circle, then mask half of it.
    
    # Let's do a "Yin-Yang" style but tech/geometric.
    # Actually, a 45-degree split is very "tech".
    
    # Create a separate layer for the "Day" half
    day_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(day_layer)
    d_draw.ellipse(bbox, fill=day_color)
    
    # Masking: Create a polygon to "cut" the bottom-right half (Night)
    # Points for a diagonal slice from bottom-left to top-right
    # (0, size) -> (size, 0) -> (size, size)
    mask = Image.new('L', (size, size), 0)
    m_draw = ImageDraw.Draw(mask)
    
    # Draw a white triangle for the part we want to KEEP (The top-left day)
    m_draw.polygon([(0, 0), (size, 0), (0, size)], fill=255)
    
    # Apply mask to day layer? No, simpler:
    # Just draw the "Night" half ON TOP of the "Day" circle.
    
    # Draw Night Half (Bottom-Right Triangle intersection)
    # We use a Chord (Pie Slice) approach for cleaner edges.
    
    draw.chord(bbox, start=45, end=225, fill=day_color)  # Day (Top-Left)
    draw.chord(bbox, start=225, end=45, fill=night_color) # Night (Bottom-Right)
    
    # 5. The "Zen" Gap (Negative Space)
    # Draw a thick line separating them to create that "modern logo" gap
    gap_width = 40
    draw.line([(padding, size-padding), (size-padding, padding)], fill=(0,0,0,0), width=gap_width)
    
    # Wait, drawing transparent line on top doesn't "erase" to alpha.
    # We need a proper mask operation for the gap.
    # Instead, let's just draw the line in the BACKGROUND color (matches app bg if round, 
    # but for an icon it needs to be transparent).
    # Since we can't easily erase with basic PIL draw, we'll accept the butt-joint 
    # or add a stylistic element.
    
    # Let's add a "Core" - a small circle in the middle, common in tech logos (lens).
    center_size = 250
    center_bbox = [
        (size/2) - (center_size/2),
        (size/2) - (center_size/2),
        (size/2) + (center_size/2),
        (size/2) + (center_size/2)
    ]
    # Draw a "Lens" hole in the middle (transparent)
    # Actually, let's make it a solid dark core, looks like a shutter.
    draw.ellipse(center_bbox, fill="#11111b") # Mocha Crust (Darker than base)

    # 6. Save
    output_path = os.path.join("gui_app", "assets", "icon.png")
    img.save(output_path, "PNG")
    print(f"Logo generated at {output_path}")

if __name__ == "__main__":
    create_pro_logo()
