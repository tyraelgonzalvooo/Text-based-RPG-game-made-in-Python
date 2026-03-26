# UI/portraits.py
import ascii_magic
from ascii_magic import AsciiArt
from pathlib import Path
from PIL import Image, ImageEnhance, ImageStat
import colorama
import io
import tempfile

# Initialize colorama for Windows color support
colorama.init(autoreset=True)

ENEMY_IMAGE_PATH = Path(__file__).parent / "enemy_images"

def get_image_brightness(image: Image.Image) -> float:
    """
    Calculate the average brightness of an image (0 = dark, 255 = bright).
    """
    grayscale = image.convert("L")
    stat = ImageStat.Stat(grayscale)
    return stat.mean[0]

def auto_enhance_image(image_path: Path) -> Image.Image:
    """
    Automatically enhance brightness/contrast based on image brightness.
    Dark images get boosted; bright ones are left mostly untouched.
    """
    img = Image.open(image_path)
    brightness = get_image_brightness(img)

    # Compute enhancement based on brightness
    if brightness < 60:
        factor = 2.2  # very dark image → strong enhancement
    elif brightness < 100:
        factor = 1.6  # moderately dark → mild enhancement
    elif brightness < 150:
        factor = 1.3
    else:
        factor = 1.1  # barely adjust bright images

    # Apply brightness & contrast
    img = ImageEnhance.Brightness(img).enhance(factor)
    img = ImageEnhance.Contrast(img).enhance(factor * 0.9)
    return img

def show_enemy(enemy_name: str):
    """
    Display the ASCII art portrait of an enemy using adaptive enhancement
    and color rendering.
    """
    filename = f"{enemy_name.lower()}.png"
    image_path = ENEMY_IMAGE_PATH / filename

    if not image_path.exists():
        print(f"[Missing ASCII image for {enemy_name}]")
        return

    # Enhance dynamically based on brightness
    enhanced_img = auto_enhance_image(image_path)

    # Store temporarily in memory (no file writes)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        enhanced_img.save(tmp.name)
        temp_path = tmp.name

    # Convert to ASCII with colors
    art = AsciiArt.from_image(temp_path)
    art.to_terminal(
        columns=60,
        width_ratio=2.2,
        enhance_image=False,  # we handled this manually
        monochrome=False
    )

    # Clean up
    Path(temp_path).unlink(missing_ok=True)

# UI/portraits.py (add below show_enemy)
PUZZLE_IMAGE_PATH = Path(__file__).parent / "puzzle_images"

def show_puzzle_art(image_name: str):
    """
    Display a puzzle-related or environment ASCII image.
    Looks for images in /UI/puzzle_images directory.
    """
    filename = f"{image_name.lower()}.png"
    image_path = PUZZLE_IMAGE_PATH / filename

    if not image_path.exists():
        print(f"[Missing ASCII image for puzzle: {image_name}]")
        return

    # Auto-enhance brightness/contrast
    enhanced_img = auto_enhance_image(image_path)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        enhanced_img.save(tmp.name)
        temp_path = tmp.name

    # Render the art
    art = AsciiArt.from_image(temp_path)
    art.to_terminal(
        columns=60,
        width_ratio=2.2,
        enhance_image=False,
        monochrome=False
    )

    Path(temp_path).unlink(missing_ok=True)
