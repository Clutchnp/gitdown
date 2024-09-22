# GitDown CLI Tool

This tool allows users to easily download specific directories from GitHub repositories using the command line.

### Big Change
The commit `#932a6b` introduces a new way to handle API requests. 

**Before:** The number of API requests was dependent on the directories traversed (due to recursion), which increased the chances of hitting the rate limit.

**After:** This commit reduces the number of API requests to just 2 for non-truncated GitHub responses. Handling of truncated responses (seen in large repositories) is still a work in progress.

---

# Installation 

## For Linux Systems

1. Install `python-virtualenv` and `pyinstaller`:
   - For Arch-based systems: `yay -S pyinstaller python-virtualenv` (replace `yay` with your preferred AUR helper).
   
2. Clone the repository:
   - ```bash
     git clone https://github.com/Clutchnp/gitdown.git
     ```

3. Use the install script or install manually.

4. Enjoy!

## For Windows Systems

1. Install Python.

2. Run `install.bat`.

3. Enjoy!

---

# Usage

- **Without installation:**
  - ```bash
    python3 gitdown.py {link} {newname}
    ```

- **With installation:**
  - ```bash
    gitdown {link} {newname}
    ```
# > [!NOTE]
> this will also work for repos themselves provided the tree is provided for eg: "https://github.com/Clutchnp/myvim" **WON'T work** but "https://github.com/Clutchnp/myvim/tree/main" will 

