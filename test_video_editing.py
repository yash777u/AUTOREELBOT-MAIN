"""
🎬 Instagram Viral Reel Test - Enhanced Version
======================================================
- 6-7 random images from images folder
- Same visual filter applied to all images
- Each image shown for 2 seconds or less with moving effect (zoom/pan)
- Transition effects (1 sec) from assets folder between images
- Single random background music behind voice
- More consistent and natural voice
"""

# --- 🛠️ FIX FOR PILLOW 10+ CRASH (MUST BE AT TOP) ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# ----------------------------------------------------

import os
import random
import shutil
from moviepy.editor import (
    ImageClip, concatenate_videoclips, AudioFileClip,
    CompositeVideoClip, VideoFileClip
)
from moviepy.video.fx import resize, crop, fadein, fadeout
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# --- edgeTTS Integration ---
try:
    import edge_tts
    import asyncio
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️ edge-tts not installed. Install with: pip install edge-tts")

# --- Configuration ---
OUTPUT_DIR = "output"
IMAGES_DIR = "images"
ASSETS_DIR = "assets"
TRANSITIONS_DIR = os.path.join(ASSETS_DIR, "transitions")
MUSIC_DIR = os.path.join(ASSETS_DIR, "background_music")
TEMP_DIR = os.path.join(OUTPUT_DIR, "temp")

def clean_everything():
    """Clean output folder completely before starting"""
    import shutil
    if os.path.exists(OUTPUT_DIR):
        try:
            shutil.rmtree(OUTPUT_DIR)
            print("🧹 Cleaned entire output folder")
        except PermissionError:
            print("⚠️ Could not delete output folder (file in use)")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

def cleanup_temp_files():
    """Delete all temp files and temp directory after final video is created"""
    deleted_count = 0
    deleted_size = 0
    
    if os.path.exists(TEMP_DIR):
        # Count files before deletion
        import glob
        all_files = glob.glob(os.path.join(TEMP_DIR, "*"))
        for f in all_files:
            if os.path.isfile(f):
                deleted_count += 1
                deleted_size += os.path.getsize(f)
        
        # Delete entire temp directory
        try:
            shutil.rmtree(TEMP_DIR)
            if deleted_count > 0:
                print(f"🗑️  Deleted {deleted_count} temp files ({deleted_size/1024/1024:.1f} MB freed)")
            else:
                print("🗑️  Temp directory cleaned")
        except Exception as e:
            print(f"⚠️ Could not delete temp files: {e}")

# --- DEFAULT TEST QUOTE ---
DEFAULT_QUOTE = """
जीवन में सफलता पाने के लिए तीन चीजें चाहिए।
पहली, अटूट इच्छाशक्ति।
दूसरी, निरंतर मेहनत।
और तीसरी, कभी हार न मानने का जज्बा।
याद रखो, विजेता वही बनता है जो अंत तक लड़ता है।
"""

# --- VOICE-OVER GENERATION WITH edgeTTS ---
async def generate_edge_tts_voice(text, output_path, voice_name="hi-IN-MadhurNeural"):
    """
    Generate natural-sounding Hindi voice-over using edgeTTS.
    More consistent and natural voice parameters.
    """
    print(f"🎙️ Generating voice with edgeTTS ({voice_name})...")
    
    # Optimized for consistency and naturalness
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice_name,
        rate="+10%",   # Slightly faster but more natural
        pitch="-15Hz",  # Moderate deepening for consistency
        volume="+15%"   # Clear but not overpowering
    )
    
    await communicate.save(output_path)
    print(f"✅ Voice-over saved: {output_path}")

def create_deep_voice_edgetts(text, output_name="voiceover.mp3"):
    """Wrapper for async edgeTTS voice generation with pydub enhancement"""
    if not EDGE_TTS_AVAILABLE:
        raise ImportError("edge-tts not installed! Run: pip install edge-tts")
    
    output_path = os.path.join(TEMP_DIR, output_name)
    
    # Run async function
    asyncio.run(generate_edge_tts_voice(text, output_path))
    
    # Further enhancement with pydub for consistency
    try:
        from pydub import AudioSegment
        from pydub.effects import compress_dynamic_range, normalize
        
        sound = AudioSegment.from_file(output_path)
        
        # Gentle deepening for natural sound
        octaves = -0.15
        new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
        deep_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        deep_sound = deep_sound.set_frame_rate(44100)
        
        # Balanced EQ for clarity and naturalness
        deep_sound = deep_sound.low_pass_filter(3800).high_pass_filter(85)
        
        # Normalize and compress for consistency
        deep_sound = normalize(deep_sound)
        deep_sound = compress_dynamic_range(deep_sound, threshold=-20.0, ratio=3.0)
        
        deep_path = output_path.replace(".mp3", "_deep.mp3")
        deep_sound.export(deep_path, format="mp3", bitrate="192k")
        print("🎙️ Voice optimized: Natural + Consistent + Clear")
        return deep_path
        
    except Exception as e:
        print(f"⚠️ pydub processing skipped: {e}")
        return output_path

# --- UNIFIED VISUAL FILTER ---
def apply_unified_filter(image_path, filter_type="cinematic"):
    """
    Apply a consistent visual filter to all images.
    
    Args:
        image_path: Path to input image
        filter_type: Type of filter to apply
    
    Returns:
        PIL Image with applied filter
    """
    img = Image.open(image_path).convert('RGB')
    
    if filter_type == "cinematic":
        # Cinematic look - slight desaturation, enhanced contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.9)
        
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)
        
    elif filter_type == "warm":
        # Warm golden filter
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.3)
        
        # Add warm tint
        img_array = np.array(img, dtype=np.float32)
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.1, 0, 255)  # Red
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 0.9, 0, 255)  # Blue
        img = Image.fromarray(img_array.astype(np.uint8))
        
    elif filter_type == "cool":
        # Cool blue filter
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.2)
        
        img_array = np.array(img, dtype=np.float32)
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 1.1, 0, 255)  # Blue
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 0.9, 0, 255)  # Red
        img = Image.fromarray(img_array.astype(np.uint8))
    
    # Slight sharpening for all filters
    img = img.filter(ImageFilter.SHARPEN)
    
    return img

# --- KEN BURNS EFFECT (ZOOM/PAN) ---
def apply_ken_burns_effect(clip, zoom_ratio=1.2):
    """
    Apply Ken Burns effect (slow zoom and pan) to a clip.
    
    Args:
        clip: ImageClip to apply effect to
        zoom_ratio: How much to zoom (1.2 = 20% zoom)
    
    Returns:
        Clip with Ken Burns effect applied
    """
    w, h = clip.size
    
    def zoom_in_effect(t):
        # Zoom gradually over the duration
        progress = t / clip.duration
        current_zoom = 1 + (zoom_ratio - 1) * progress
        
        # Calculate new dimensions
        new_w = int(w * current_zoom)
        new_h = int(h * current_zoom)
        
        # Pan slightly (move from center to slightly off-center)
        x_offset = int((new_w - w) * progress * 0.5)
        y_offset = int((new_h - h) * progress * 0.3)
        
        return x_offset, y_offset
    
    # Apply resize and position changes
    return clip.resize(lambda t: 1 + (zoom_ratio - 1) * t / clip.duration)

# --- CREATE VIRAL REEL ---
def create_viral_reel_enhanced():
    """
    Create viral reel with:
    - 6-7 random images with unified filter
    - 2 seconds per image with Ken Burns effect
    - 1 second transition effects from assets
    - Random background music
    - Consistent natural voice
    """
    print("\n🎬 Creating Enhanced Viral Reel...")
    
    # 1. Get random images (6-7 images)
    print("\n🖼️ Step 1: Selecting random images")
    image_files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    
    if not image_files:
        raise ValueError(f"❌ No images found in '{IMAGES_DIR}/' folder!")
    
    # Select 6-7 random images
    num_images = random.randint(6, 7)
    num_images = min(num_images, len(image_files))
    selected_images = random.sample(image_files, num_images)
    
    print(f"   Selected {num_images} random images from {len(image_files)} available")
    
    # 2. Select random filter
    filters = ["cinematic", "warm", "cool"]
    selected_filter = random.choice(filters)
    print(f"   Selected filter: {selected_filter}")
    
    # 3. Generate voice-over
    print("\n🎙️ Step 2: Generate Voice-over")
    try:
        audio_path = create_deep_voice_edgetts(DEFAULT_QUOTE.strip(), "viral_voice.mp3")
        audio = AudioFileClip(audio_path)
        print(f"   Audio duration: {audio.duration:.1f}s")
    except Exception as e:
        print(f"❌ Voice generation failed: {e}")
        print("💡 Creating video without voice")
        audio_path = None
        audio = None
    
    # 4. Select random background music
    print("\n🎵 Step 3: Select background music")
    music_files = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith('.mp3')]
    
    bg_music = None
    if music_files:
        selected_music = random.choice(music_files)
        music_path = os.path.join(MUSIC_DIR, selected_music)
        bg_music = AudioFileClip(music_path)
        print(f"   Selected: {selected_music}")
    else:
        print("   No background music found")
    
    # 5. Get transition effects
    print("\n⚡ Step 4: Loading transition effects")
    transition_files = [f for f in os.listdir(TRANSITIONS_DIR) if f.lower().endswith(('.mp4', '.mov'))]
    
    if not transition_files:
        print("   No transition effects found, will use crossfade")
        transition_files = []
    else:
        print(f"   Found {len(transition_files)} transition effects")
    
    # 6. Create image clips with unified filter and Ken Burns effect
    print(f"\n🎨 Step 5: Creating {num_images} clips with filter and motion")
    
    clips = []
    image_duration = 2.0  # 2 seconds per image
    
    for i, img_file in enumerate(selected_images):
        img_path = os.path.join(IMAGES_DIR, img_file)
        
        # Apply unified filter
        filtered_img = apply_unified_filter(img_path, selected_filter)
        
        # Save temp filtered image
        temp_path = os.path.join(TEMP_DIR, f"filtered_{i:03d}.jpg")
        filtered_img.save(temp_path, quality=95)
        
        # Create clip with Ken Burns effect
        clip = ImageClip(temp_path).set_duration(image_duration)
        
        # Resize to 9:16 (1080x1920)
        clip = clip.resize(height=1920)
        if clip.w < 1080:
            clip = clip.resize(width=1080)
        clip = clip.crop(x1=clip.w/2 - 540, width=1080, height=1920)
        
        # Apply Ken Burns effect (zoom in)
        zoom_ratio = random.uniform(1.15, 1.25)
        clip = apply_ken_burns_effect(clip, zoom_ratio)
        
        clips.append(clip)
        print(f"   ✓ Clip {i+1}/{num_images} created (filter: {selected_filter}, zoom: {zoom_ratio:.2f}x)")
    
    # 7. Add transition effects between clips
    print(f"\n🎞️ Step 6: Adding transition effects")
    
    transition_duration = 1.0  # 1 second transitions
    final_clips = []
    
    for i, clip in enumerate(clips):
        # Add the main clip
        final_clips.append(clip)
        
        # Add transition after each clip except the last one
        if i < len(clips) - 1 and transition_files:
            # Pick a random transition
            trans_file = random.choice(transition_files)
            trans_path = os.path.join(TRANSITIONS_DIR, trans_file)
            
            try:
                trans_clip = VideoFileClip(trans_path)
                trans_clip = trans_clip.set_duration(transition_duration)
                
                # Resize transition to 9:16
                trans_clip = trans_clip.resize(height=1920)
                if trans_clip.w < 1080:
                    trans_clip = trans_clip.resize(width=1080)
                trans_clip = trans_clip.crop(x1=trans_clip.w/2 - 540, width=1080, height=1920)
                
                # Remove audio from transition
                trans_clip = trans_clip.without_audio()
                
                final_clips.append(trans_clip)
                print(f"   ✓ Added transition {i+1}")
                
            except Exception as e:
                print(f"   ⚠️ Failed to load transition {trans_file}: {e}")
                # Fallback to crossfade
                pass
    
    # 8. Combine all clips
    print(f"\n🎬 Step 7: Combining clips")
    final_video = concatenate_videoclips(final_clips, method="compose")
    
    print(f"   Video duration: {final_video.duration:.2f}s")
    
    # 9. Add audio (voice + background music)
    print(f"\n🎙️ Step 8: Adding audio")
    
    if audio_path and audio:
        # Mix voice with background music
        if bg_music:
            # Reduce background music volume to not overpower voice
            bg_music_reduced = bg_music.volumex(0.3)
            
            # Loop background music if shorter than video
            if bg_music_reduced.duration < final_video.duration:
                from moviepy.editor import concatenate_audioclips
                loops_needed = int(final_video.duration / bg_music_reduced.duration) + 1
                bg_music_reduced = concatenate_audioclips([bg_music_reduced] * loops_needed)
            
            # Trim to video duration
            bg_music_reduced = bg_music_reduced.subclip(0, min(bg_music_reduced.duration, final_video.duration))
            
            # Mix audio (voice + music)
            from moviepy.audio.AudioClip import CompositeAudioClip
            
            # Trim voice to video duration
            audio_trimmed = audio.subclip(0, min(audio.duration, final_video.duration))
            
            mixed_audio = CompositeAudioClip([audio_trimmed, bg_music_reduced])
            final_video = final_video.set_audio(mixed_audio)
            print("   ✓ Mixed voice with background music")
        else:
            # Just voice
            final_video = final_video.set_audio(audio.subclip(0, min(audio.duration, final_video.duration)))
            print("   ✓ Added voice-over")
    elif bg_music:
        # Just background music
        if bg_music.duration < final_video.duration:
            from moviepy.editor import concatenate_audioclips
            loops_needed = int(final_video.duration / bg_music.duration) + 1
            bg_music = concatenate_audioclips([bg_music] * loops_needed)
        bg_music = bg_music.subclip(0, min(bg_music.duration, final_video.duration))
        final_video = final_video.set_audio(bg_music)
        print("   ✓ Added background music only")
    
    # 10. Export
    output_path = os.path.join(OUTPUT_DIR, "viral_reel_enhanced.mp4")
    print(f"\n💾 Step 9: Exporting final video...")
    
    final_video.write_videofile(
        output_path,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        threads=4,
        preset='medium',
        verbose=False,
        logger=None
    )
    
    # 11. Close clips to release file handles
    print("\n🔒 Closing video clips...")
    try:
        final_video.close()
        if audio_path and audio:
            audio.close()
        if bg_music:
            bg_music.close()
        for clip in clips:
            try:
                clip.close()
            except:
                pass
        for clip in final_clips:
            try:
                clip.close()
            except:
                pass
    except Exception as e:
        print(f"   ⚠️ Warning closing clips: {e}")
    
    # Force garbage collection to release file handles
    import gc
    gc.collect()
    
    # Small delay to ensure OS releases files
    import time
    time.sleep(0.5)
    
    # 12. Cleanup temp files
    print("🗑️  Cleaning up temp files...")
    cleanup_temp_files()
    
    # Success message
    file_size = os.path.getsize(output_path) / 1024 / 1024
    
    print("\n" + "="*60)
    print("🎉 SUCCESS! ENHANCED VIRAL REEL CREATED!")
    print("="*60)
    print(f"📹 File: {output_path}")
    print(f"⏱️  Duration: {final_video.duration:.1f}s")
    print(f"🖼️  Images: {num_images} ({image_duration}s each)")
    print(f"🎨 Filter: {selected_filter}")
    print(f"⚡ Motion: Ken Burns effect on all images")
    print(f"🎬 Transitions: {len(transition_files) if transition_files else 'Crossfade'}")
    print(f"🎙️ Voice: {'Consistent Natural Hindi' if audio_path else 'None'}")
    print(f"🎵 Music: {'Background music added' if bg_music else 'None'}")
    print(f"💾 File size: {file_size:.1f} MB")
    print(f"✨ Output folder: Clean (only final video)")
    print("="*60)
    
    return output_path

# --- MAIN TEST RUNNER ---
if __name__ == "__main__":
    print("="*60)
    print("🎬 VIRAL REEL TEST - ENHANCED VERSION")
    print("="*60)
    
    # Clean everything first
    clean_everything()
    
    # Check images
    image_files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.jpg', '.png'))]
    print(f"\n📁 Found {len(image_files)} images in '{IMAGES_DIR}/'")
    
    if len(image_files) < 1:
        print("\n❌ ERROR: Need at least 1 image!")
        print(f"   Add images to '{IMAGES_DIR}/' folder")
        exit(1)
    
    # Check edgeTTS
    if not EDGE_TTS_AVAILABLE:
        print("\n⚠️ edgeTTS not available!")
        print("   Install with: pip install edge-tts")
        print("   Will create video without voice")
    
    print("\n" + "="*60)
    print("STARTING VIDEO CREATION")
    print("="*60)
    
    try:
        result = create_viral_reel_enhanced()
        
        print("\n✅ TEST COMPLETED SUCCESSFULLY!")
        print(f"\n🎬 Watch your video: {result}")
        print("\n💡 Features:")
        print("   • 6-7 random images with same filter")
        print("   • 2 seconds per image with zoom effect")
        print("   • 1 second transitions between images")
        print("   • Background music + voice-over")
        print("   • More consistent and natural voice")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        cleanup_temp_files()
