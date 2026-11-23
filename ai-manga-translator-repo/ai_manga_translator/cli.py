import argparse
import sys
from .client import MangaTranslatorClient

def main():
    parser = argparse.ArgumentParser(description="AI Manga Translator CLI")
    parser.add_argument("file", help="Path to manga image or document")
    parser.add_argument("-t", "--target", default="en", help="Target language (en, ja, ko, zh)")
    parser.add_argument("-s", "--style", default="standard", help="Translation style")
    parser.add_argument("--api-key", default=None, help="API key")

    args = parser.parse_args()
    client = MangaTranslatorClient(api_key=args.api_key)

    print(f"Processing: {args.file} -> {args.target}")
    try:
        res = client.translate_image(args.file, target_lang=args.target, style=args.style)
        if res.status.value == "completed":
            print(f"Success! Output: {res.translated_url}")
        else:
            print(f"Task status: {res.status.value}, Error: {res.error_message}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
