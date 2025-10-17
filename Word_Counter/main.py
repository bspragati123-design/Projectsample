# Word Counter Program
# Author: Saksham Upadhyay

def count_words(text):
    """Return total words and most frequent words in the text."""
    words = text.lower().split()
    word_count = len(words)

    freq = {}
    for word in words:
        word = word.strip(".,!?;:\"'()[]{}") 
        if word:
            freq[word] = freq.get(word, 0) + 1

    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return word_count, sorted_freq[:5]


def main():
    print("=== Word Counter ===")
    print("1. Enter text manually")
    print("2. Read from a text file")

    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "1":
        text = input("\nEnter your text below:\n")
    elif choice == "2":
        file_path = input("Enter file path: ").strip()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print("File not found. Please check the path.")
            return
    else:
        print("Invalid choice.")
        return

    total_words, top_words = count_words(text)
    print(f"\nTotal words: {total_words}")
    print("\nTop 5 most frequent words:")
    for word, count in top_words:
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
