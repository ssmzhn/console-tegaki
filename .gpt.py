import re
import time
import threading
from queue import Queue
from colorama import init, Fore, Back, Style
from wcwidth import wcwidth
import pygame

init()

# 初始化 pygame 音频系统
pygame.mixer.init()

def parse_lrc(lrc_text):
    pattern = re.compile(r'\[(\d{2}):(\d{2}\.\d{2,3})\](.*)')
    parsed_lines = []
    for line in lrc_text.split('\n'):
        match = pattern.match(line)
        if match:
            minutes = int(match.group(1))
            seconds = float(match.group(2))
            timestamp = minutes * 60 + seconds
            lyric = match.group(3)
            parsed_lines.append((timestamp, lyric))
    return parsed_lines

def display(text: str, end="\n", fore=Fore.RESET, back=Back.RESET, prompt=Style.DIM):
    print(fore, back, end="")
    is_in_prompt = False
    char_width_in_prompt = 0

    def backspace_and_clear(num):
        for _ in range(num):
            print("\b \b", end="")
    
    for x in text:
        if x == "{":
            is_in_prompt = True
            print(prompt, end="")
            char_width_in_prompt = 0
        elif x == "}":
            backspace_and_clear(char_width_in_prompt)
            is_in_prompt = False
            print(Style.RESET_ALL, end="")
        else:
            width = wcwidth(x)
            if is_in_prompt:
                char_width_in_prompt += width
            print(x, end="", flush=True)
            time.sleep(0.05)
    print(Style.RESET_ALL, end=end)

def display_lyrics_worker(queue):
    while True:
        timestamp, lyric = queue.get()
        if timestamp is None:
            break
        current_time = time.perf_counter()
        sleep_time = timestamp - (current_time - start_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
        line_start_time = time.perf_counter()
        display(lyric)
        display_time = time.perf_counter() - line_start_time
        start_time += display_time  # Adjust start time to compensate for display execution time
        queue.task_done()

def producer_thread(queue, lyrics):
    global start_time
    start_time = time.perf_counter()
    for timestamp, lyric in lyrics:
        queue.put((timestamp, lyric))
    queue.put((None, None))  # Signal the consumer thread to stop

def audio_thread(filename, delay):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    time.sleep(delay)
    while pygame.mixer.music.get_busy():
        time.sleep(1)  # Check every second if music is still playing

# 示例 LRC 歌词
lrc_content = """
[00:00.00] {しんだ}死んだ{へんすう}変数で{く}繰り{かえ}返す
[00:05.00] {かぞ}数え{ごと}事が{はら}孕んだ{ねつ}熱
[00:10.00] どこに{おく}送るあてもなく
[00:15.00] {あわ}哀れな{ひと}独り{ごと}言を{しる}記している
"""

parsed_lyrics = parse_lrc(lrc_content)

# 创建队列和线程
queue = Queue()
display_thread = threading.Thread(target=display_lyrics_worker, args=(queue,))
producer = threading.Thread(target=producer_thread, args=(queue, parsed_lyrics))
audio_filename = "your_audio_file.mp3"  # 替换为你的 MP3 文件路径
audio_delay = 0  # 设置音频播放的延迟时间（秒）
audio_playback_thread = threading.Thread(target=audio_thread, args=(audio_filename, audio_delay))

# 启动线程
display_thread.start()
producer.start()
audio_playback_thread.start()

# 等待线程完成
producer.join()
queue.join()  # 确保队列中的所有项目都已处理
display_thread.join()
audio_playback_thread.join()

