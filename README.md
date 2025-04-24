> [!IMPORTANT]  
> This tool may no longer be actively maintained, as Ive mostly switched to Roo Code with Gemini 2.5 Pro _:3_

# Cursor Shadow Patch

Patch `out/main.js` to force diffferent machine ids.

**Disclaimer: This tool is intended solely to fix issues preventing you from using your own Cursor account due to internal machine ID retrieval problems. It must not be used for automated account registration or trials. Please do not violate Cursor's terms of service.**

- Platform: Win32 / Darwin / Linux, with Python 3.10+
- Version: 0.45 ~ 0.49

#### Installation

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

#### Usage

1. Clone this project (or [download zip](https://github.com/zetaloop/cursor-shadow-patch/archive/refs/heads/main.zip)) and run `patcher.py`.
2. <kbd>Enter</kbd> * 5.
3. If it shows all green and no red, youre done.
4. Next time when you need a new machine id or when youve just updated cursor, run it again.

#### Building executable

To build standalone executable:
```
python build.py
```
The executable will be generated in the `dist` directory.

#### Note

Changing the machine ID may not be enough to resolve all issues.<br>
Cursor can still block you based on your **email** and **IP address**.
