import curses
import time
import random

SENTENCES = [
    "The coffee on the table has already turned cold.",
    "Birds were flying high above the mountain peaks.",
    "She found an old diary hidden inside the drawer.",
    "The train arrived at the station exactly on time.",
    "A gentle breeze moved through the tall trees.",
    "He bought fresh fruits and vegetables from the market.",
    "The puppy barked loudly when the doorbell rang.",
    "Clouds covered the sky before the rain began to fall.",
    "They decided to go for a long walk after dinner.",
    "The library was silent except for the sound of turning pages."
]

def typing_test(stdscr):
    # Initialize colors and settings
    curses.curs_set(1)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)  # correct chars
    curses.init_pair(2, curses.COLOR_RED, -1)    # wrong chars

    random_sentences = random.sample(SENTENCES, len(SENTENCES))

    total_time = 0.0
    total_words = 0
    total_correct_chars = 0
    total_chars = 0

    for idx, target_text in enumerate(random_sentences, start=1):
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()

        stdscr.addstr(0, 0, f"Typing Test — Sentence {idx}/{len(random_sentences)} (Press ESC to quit)")
        stdscr.addstr(2, 0, "Type this:")
        stdscr.addstr(3, 0, target_text, curses.A_BOLD)
        stdscr.addstr(5, 0, "Your input:")
        stdscr.refresh()

        current_text = []
        start_time = None
        input_row = 6

        while True:
            try:
                key = stdscr.get_wch()  # returns str for printable, int for special keys
            except Exception:
                key = stdscr.getch()

            # Detect ESC (either as int or str)
            if (isinstance(key, int) and key == 27) or (isinstance(key, str) and ord(key) == 27):
                return  # quit the entire test

            # Normalize input: determine if backspace or printable character
            backspace = False
            char = None

            if isinstance(key, str):
                if key in ("\b", "\x7f"):
                    backspace = True
                elif key == "\n":
                    # ignore Enter (we want to type the full sentence)
                    continue
                else:
                    char = key
            elif isinstance(key, int):
                if key in (curses.KEY_BACKSPACE, 127, 8):
                    backspace = True
                elif 32 <= key <= 126:
                    char = chr(key)

            # Start timer on first real typed character
            if start_time is None and char is not None:
                start_time = time.time()

            # Update current_text
            if backspace:
                if current_text:
                    current_text.pop()
            elif char is not None:
                current_text.append(char)

            # Render the typed line with color feedback
            stdscr.move(input_row, 0)
            stdscr.clrtoeol()
            for i, typed_char in enumerate(current_text):
                # avoid indexing target_text out of range
                correct_char = target_text[i] if i < len(target_text) else None
                if correct_char is not None and typed_char == correct_char:
                    # correct
                    if i < max_x - 1:
                        stdscr.addstr(input_row, i, typed_char, curses.color_pair(1))
                else:
                    # wrong or extra chars
                    if i < max_x - 1:
                        stdscr.addstr(input_row, i, typed_char, curses.color_pair(2))

            stdscr.refresh()

            # Completed this sentence?
            if "".join(current_text) == target_text:
                elapsed = (time.time() - start_time) if start_time else 0.0
                words = len(target_text.split())
                total_time += elapsed
                total_words += words

                correct_chars = sum(
                    1 for i, typed_char in enumerate(current_text)
                    if i < len(target_text) and typed_char == target_text[i]
                )
                total_correct_chars += correct_chars
                total_chars += len(target_text)

                wpm = round(words / (elapsed / 60) if elapsed > 0 else 0.0, 2)
                acc = round((correct_chars / len(target_text)) * 100, 2) if len(target_text) > 0 else 0.0

                stdscr.addstr(input_row + 2, 0, f"Completed sentence {idx}. Time: {elapsed:.2f}s   WPM: {wpm}   Accuracy: {acc}%")
                stdscr.addstr(input_row + 4, 0, "Press any key to continue...")
                stdscr.refresh()
                stdscr.getch()
                break

    # Final aggregated results
    avg_wpm = round(total_words / (total_time / 60) if total_time > 0 else 0.0, 2)
    overall_accuracy = round((total_correct_chars / total_chars) * 100, 2) if total_chars > 0 else 0.0

    stdscr.clear()
    stdscr.addstr(0, 0, "✅ Typing Test Completed!\n\n")
    stdscr.addstr(2, 0, f"Total time: {total_time:.2f} seconds\n")
    stdscr.addstr(3, 0, f"Average WPM: {avg_wpm}\n")
    stdscr.addstr(4, 0, f"Accuracy: {overall_accuracy}%\n")
    stdscr.addstr(6, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(typing_test)