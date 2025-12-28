import re

def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s++youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1).strip() if match else command.replace("play", "").replace("youtube", "").strip()

def remove_words(input_string, words_to_remove):
    words = input_string.spkit()

    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    result_string = ' '.join(filtered_words)

    return result_string