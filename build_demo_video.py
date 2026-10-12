import os
import subprocess
import wave
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
artifact_dir = r"C:\Users\ShaikAli\.gemini\antigravity\brain\b0045c3b-77f4-4da5-a6a6-26b824949816"
out_dir = r"C:\Users\ShaikAli\.gemini\antigravity\scratch\paypal_ai_hackathon"

slides = [
    {
        "img": os.path.join(artifact_dir, "demo_slide_1_title_1791816386387.jpg"),
        "text": (
            "Welcome to PayPal AI Checkout, built for the Build What's Next with PayPal and AI Global Hackathon. "
            "Moving from an AI product conversation to an actual purchase usually requires jumping across multiple tabs and checkout forms. "
            "PayPal AI Checkout solves this by combining generative AI product discovery with instant, in-chat PayPal Sandbox payments, "
            "turning a natural language request directly into a verified PayPal transaction."
        )
    },
    {
        "img": os.path.join(artifact_dir, "demo_slide_2_arch_1791816407000.jpg"),
        "text": (
            "Here is our system architecture. "
            "On the frontend, a responsive HTML and JavaScript chat UI integrates the official PayPal JavaScript SDK. "
            "In the center, our Python Flask backend exposes three REST endpoints. "
            "First, api chat sends the user's prompt to OpenAI GPT using a strict system prompt that enforces structured JSON output with product name, description, and price. "
            "Second, api create order communicates with the PayPal Sandbox Orders V2 API to initialize a payment for the quoted price. "
            "Third, api capture order finalizes the payment upon approval."
        )
    },
    {
        "img": os.path.join(artifact_dir, "demo_slide_3_chat_1791816421232.jpg"),
        "text": (
            "Let's see the application in action. "
            "A user asks the assistant: I need a high quality wireless ergonomic mouse under fifty dollars. "
            "The AI assistant responds with a structured recommendation: the AeroGlide Pro Wireless Mouse for thirty-nine ninety-nine, complete with key product specs. "
            "Our frontend parses the JSON price and dynamically renders the official Checkout with PayPal button right inside the chat bubble."
        )
    },
    {
        "img": os.path.join(artifact_dir, "demo_slide_4_checkout_1791816435669.jpg"),
        "text": (
            "When the user clicks Checkout with PayPal, the PayPal Sandbox checkout window launches seamlessly over the chat interface. "
            "Behind the scenes, our Flask server has created the PayPal order for thirty-nine ninety-nine USD. "
            "The buyer reviews their shipping address, selects their linked Visa card or PayPal balance, and clicks Complete Purchase."
        )
    },
    {
        "img": os.path.join(artifact_dir, "demo_slide_5_success_1791816451616.jpg"),
        "text": (
            "Immediately after approval, our capture order endpoint finalizes the sandbox payment and returns a CAPTURED status with Order ID 8XY92041AB. "
            "The chat interface updates in real time with a green verification badge confirming Payment Completed. "
            "You can try out the full open-source code on GitHub at shaikjafar559 slash paypal-ai-checkout. Thank you for watching!"
        )
    }
]

def generate_tts_wav(text, wav_path):
    ps_script = f'''
Add-Type -AssemblyName System.Speech
$Synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$Synth.Volume = 100
$Synth.Rate = 1
$Synth.SetOutputToWaveFile("{wav_path}")
$Synth.Speak("{text.replace('"', "'")}")
$Synth.Dispose()
'''
    subprocess.run(["powershell", "-Command", ps_script], check=True)

def get_wav_duration(wav_path):
    with wave.open(wav_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / float(rate)

segment_files = []
total_dur = 0.0
for idx, slide in enumerate(slides):
    wav_path = os.path.join(out_dir, f"seg_{idx}.wav")
    mp4_path = os.path.join(out_dir, f"seg_{idx}.mp4")
    generate_tts_wav(slide["text"], wav_path)
    dur = get_wav_duration(wav_path) + 1.0  # 1s pause at end of slide
    total_dur += dur
    print(f"Slide {idx+1} exact duration: {dur:.2f}s")
    
    cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1",
        "-framerate", "15",
        "-i", slide["img"],
        "-i", wav_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", f"{dur:.2f}",
        mp4_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    segment_files.append(mp4_path)
    os.remove(wav_path)

concat_list = os.path.join(out_dir, "concat_list.txt")
with open(concat_list, "w") as f:
    for seg in segment_files:
        f.write(f"file '{seg}'\n")

output_mp4 = os.path.join(out_dir, "paypal_ai_checkout_demo.mp4")
subprocess.run([
    ffmpeg_exe, "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_list,
    "-c", "copy",
    output_mp4
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

os.remove(concat_list)
for seg in segment_files:
    os.remove(seg)

print(f"Success! Final video duration: {total_dur:.2f} seconds (~{total_dur/60:.2f} minutes).")
print("Saved to:", output_mp4)
