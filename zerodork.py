import random
import time
import requests
import os
import re

user_agent = [
    # Chrome on Windows 11
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36",
    # Firefox on Windows 10
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    # Edge on Windows 11
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36 Edg/123.0.2420.53",
    # Safari on macOS 13
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    # Chrome on Android 13
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Mobile Safari/537.36",
    # Safari on iPhone 14 Pro (iOS 17)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
]

def fetch_urls(domain, dorks, output_file):
    found = set()
    try:
        for dork in dorks:
            headers = {"User-Agent": random.choice(user_agent)}
            query = f"site:{domain} {dork}"
            print(f"[+] Dorking: {query}")
            url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
            try:
                res = requests.get(url, headers=headers, timeout=5)
                links = set(re.findall(r"https://[^\"'>\s]+", res.text))
                filtered_links = {link for link in links if domain in link}
                if filtered_links:
                    new_links = filtered_links - found
                    found.update(new_links)
                    with open(output_file, "a") as out:
                        for link in new_links:
                            out.write(link + "\n")
                            print(f" -> {link}")
                else:
                    print(" [-] No results.")
            except Exception as e:
                print(f"[!] Error: {e}")
            time.sleep(random.uniform(1, 2))  # Sleep to avoid blocking
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting and saving collected URLs...")
    return found


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(r'''
_______                                 _______                       __       
|      \                               |       \                     |  \      
 \$$$$$$$$ ______    ______    ______  | $$$$$$$\  ______    ______  | $$   __ 
    /  $$ /      \  /      \  /      \ | $$  | $$ /      \  /      \ | $$  /  \
   /  $$ |  $$$$$$\|  $$$$$$\|  $$$$$$\| $$  | $$|  $$$$$$\|  $$$$$$\| $$_/  $$
  /  $$  | $$    $$| $$   \$$| $$  | $$| $$  | $$| $$  | $$| $$   \$$| $$   $$ 
 /  $$___| $$$$$$$$| $$      | $$__/ $$| $$__/ $$| $$__/ $$| $$      | $$$$$$\ 
|  $$    \\$$     \| $$       \$$    $$| $$    $$ \$$    $$| $$      | $$  \$$\
 \$$$$$$$$ \$$$$$$$ \$$        \$$$$$$  \$$$$$$$   \$$$$$$  \$$       \$$   \$$ 

                    Welcome to Zero Dork
                    Author: MrV3rus
                    Team: Unr3veledTr4netra
                    About : It is used to find hidden urls.
    ''')

    domain = input("Enter a domain (e.g. google.com): ").strip()
    wordlist_file = input("Enter the path of dorks file (e.g. googledork.txt): ").strip()
    output_file = input("Enter the path to save the output file (e.g. fuzzedurls.txt): ").strip()

    if not os.path.isfile(wordlist_file):
        print("[!] Wordlist not found.")
        return

    with open(wordlist_file, "r") as f:
        dorks = [line.strip() for line in f if line.strip()]

    results = fetch_urls(domain, dorks, output_file)
    print(f"\n[✓] Finished! {len(results)} URLs saved to '{output_file}'")


if __name__ == "__main__":
    main()
