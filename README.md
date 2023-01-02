# "kǎoyā", a translation software that will:

1. Take a screenshot of any area on your screen,
2. Detect the text and language from screenshot,
3. Return the fully translated text.

## Dependencies

To build kǎoyā on Fedora GNU/Linux, you may follow these commands: 

```bash
git clone https://github.com/0xMarius/kaoya.git
sudo dnf install -y gtk4 libadwaita python3 python3-pip
pip install Pillow, pytesseract, libretranslate
```
Upgrades and Windows version expected in the future
