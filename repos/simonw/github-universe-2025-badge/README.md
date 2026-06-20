# BADGER - GitHub Universe 2025 Badge

See https://github.com/badger/home for offical information on the badge.

(Readme generated from the source code [using Claude Code](https://gistpreview.github.io/?871aaa17667c8616950c195e6eec37dc).)

A custom firmware collection for the Badger2040 badge featuring multiple interactive apps and games, all starring Mona (GitHub's Octocat mascot).

## Overview

This project contains a complete MicroPython-based application suite designed for the Badger2040 e-ink badge. The badge features a launcher menu and 9 apps including games, utilities, diagnostics, and interactive experiences centered around GitHub and the Mona character.

## Setup

Modify `secrets.py` (not included in this repo) to add these values:

```python
WIFI_SSID = "..."
WIFI_PASSWORD = "..."
GITHUB_USERNAME = "..." # No @ sign, just the username
```

## Apps

### 1. Badge (`apps/badge/`)
**Your GitHub Profile on a Badge**

Displays your GitHub profile statistics on the badge screen, including:
- GitHub username and full name
- Contribution graph (full year visualization with color-coded activity levels)
- Follower count
- Total contributions
- Public repository count
- GitHub avatar (75x75 pixels)

**Setup:**
1. Edit `secrets.py` and add:
   - `WIFI_SSID` - WiFi network name
   - `WIFI_PASSWORD` - WiFi password
   - `GITHUB_USERNAME` - Your GitHub username
2. The app automatically fetches data from GitHub's API on first run
3. Hold A+C buttons together to force refresh the data

### 2. Flappy Mona (`apps/flappy/`)
**Classic Flappy Bird with Mona**

A Flappy Bird-style game featuring Mona dodging obstacles:
- Press A to make Mona jump
- Avoid pipes to increase your score
- Parallax scrolling background with clouds and grass
- Game Over screen shows your final score

### 3. Mona Pet (`apps/monapet/`)
**Virtual Pet Tamagotchi-Style Game**

Take care of your very own Mona pet:
- **3 Stats to manage:**
  - Happiness (decreases over 30 minutes)
  - Hunger (decreases over 20 minutes)
  - Cleanliness (decreases over 40 minutes)
- **Controls:**
  - A - Play with Mona (increases happiness)
  - B - Feed Mona (decreases hunger)
  - C - Clean Mona (increases cleanliness)
- Mona walks around and changes animations based on her mood
- If all stats drop below 30%, Mona gets worried
- If stats reach 0%, Mona dies (press B to reset)
- State is automatically saved when you exit the app

### 4. Mona's Quest (`apps/quest/`)
**IR Beacon Scavenger Hunt**

A conference scavenger hunt game using IR beacons:
- Find 9 different locations at GitHub Universe
- Each location has an IR beacon that unlocks when you get close
- **Locations:**
  1. Hack Your Badge
  2. What's up Docs
  3. Stars Lounge
  4. GitHub Next
  5. Open Source Zone
  6. Demos & Donuts
  7. GitHub Learn
  8. Octocat Generator
  9. Makerspace
- Progress is saved automatically
- Complete all 9 to finish the side quest!

### 5. MonaSketch (`apps/sketch/`)
**Drawing Application**

A simple drawing app with animated elements:
- Use buttons to move cursor:
  - A - Move left
  - C - Move right
  - UP - Move up
  - DOWN - Move down
- Drawing automatically appears where the cursor moves
- Mona appears at the bottom and runs away if you get too close
- Animated dials show cursor position

### 6. Gallery (`apps/gallery/`)
**Image Viewer**

Browse images stored on the badge.

### 7. Debug Info (`apps/debug/`)
**System Diagnostics and Network Status**

A comprehensive system information and debugging tool with 4 pages:

**Page 1 - Network Info:**
- Connection status (Connected/Disconnected)
- WiFi SSID
- IP address, netmask, gateway, DNS
- MAC address
- Signal strength (RSSI in dBm)

**Page 2 - Memory Info:**
- Free, used, and total RAM
- Memory usage percentage
- Visual memory usage bar graph
- Press B to run garbage collection

**Page 3 - System Info:**
- Platform information
- MicroPython version
- CPU frequency
- Screen dimensions (width x height)
- System uptime
- Unique device ID

**Page 4 - Storage Info:**
- Total, used, and free storage
- Storage usage percentage
- Visual storage usage bar graph
- Current working directory

**Controls:**
- A - Previous page
- C - Next page
- B - Run garbage collection (on Memory page)

### 8. Menu (`apps/menu/`)
**Application Launcher**

The main menu system:
- Grid layout showing all installed apps with icons
- Use A/C to move left/right
- Use UP/DOWN to move up/down
- Press B to launch the selected app
- Press HOME button during any app to return to menu

### 9. Startup (`apps/startup/`)
**Animated Boot Sequence**

An animated intro that plays when the badge boots:
- 159 frame animation
- Fades in on boot
- Press any button to skip to menu
- Skipped automatically on watchdog wake

## File Structure

```
BADGER/
├── main.py              # Main entry point that runs at boot
├── secrets.py           # WiFi and GitHub credentials
├── apps/                # Application directory
│   ├── badge/           # GitHub profile stats app
│   ├── debug/           # System diagnostics and debug info
│   ├── flappy/          # Flappy bird game
│   ├── gallery/         # Image gallery
│   ├── menu/            # App launcher
│   ├── monapet/         # Virtual pet game
│   ├── quest/           # IR beacon scavenger hunt
│   ├── sketch/          # Drawing app
│   └── startup/         # Boot animation
└── assets/              # Shared assets
    ├── fonts/           # Custom fonts (.ppf format)
    ├── icons.png        # Menu icons
    └── mona-sprites/    # Mona character sprites
```

## Setup Instructions

### Initial Setup

1. **Put Badge in Disk Mode:**
   - Tap the RESET button twice quickly
   - Badge will appear as USB drive

2. **Copy Files:**
   - Copy all files and folders to the badge
   - The badge filesystem should have `/system/` directory structure

3. **Configure WiFi (for Badge app):**
   - Edit `secrets.py`:
   ```python
   WIFI_SSID = "your-wifi-network"
   WIFI_PASSWORD = "your-wifi-password"
   GITHUB_USERNAME = "your-github-username"
   ```

4. **Restart:**
   - Eject the USB drive
   - Press RESET once to boot

### Customization

#### Add/Remove Apps from Menu

Edit `apps/menu/__init__.py` and modify the `apps` list:

```python
apps = [
    ("mona's quest", "quest"),
    ("mona pet", "monapet"),
    ("monasketch", "sketch"),
    ("flappy mona", "flappy"),
    ("gallery", "gallery"),
    ("badge", "badge"),
    ("debug info", "debug"),
]
```

Each entry is a tuple of `(display_name, folder_name)`.

#### Create Your Own App

1. Create a new folder in `apps/`
2. Add an `__init__.py` file with:
   - `update()` function - called every frame
   - Optional `init()` function - called once at startup
   - Optional `on_exit()` function - called when returning to menu
3. Add an `icon.png` (32x32 pixels)
4. Add your app to the menu list (see above)

Example minimal app:

```python
from badgeware import screen, brushes, shapes, run

def update():
    screen.brush = brushes.color(255, 255, 255)
    screen.draw(shapes.rectangle(0, 0, 160, 120))
    screen.text("Hello World!", 10, 50)

if __name__ == "__main__":
    run(update)
```

## Technical Details

### Hardware
- **Device:** Badger2040 (Raspberry Pi RP2040)
- **Display:** 296x128 e-ink screen (rendered at 160x120)
- **Buttons:** A, B, C, UP, DOWN, HOME
- **IR Receiver:** Pin 21 (for Quest app)
- **WiFi:** Built-in (for Badge app)

### Software
- **Language:** MicroPython
- **Framework:** badgeware library (custom)
- **Graphics:** Pixel fonts, sprites, shapes API
- **Storage:** State persistence for save games

### Main Loop

The `main.py` file:
1. Shows startup animation (skippable)
2. Launches menu
3. User selects app
4. App runs until HOME button pressed
5. Returns to menu

### Button Handling
- HOME button triggers hardware interrupt to quit any app
- Each app implements its own button handling via `io.pressed` and `io.held`

### State Persistence

Apps can save state using the `State` API:

```python
from badgeware import State

# Save
State.save("app_name", {"key": "value"})

# Load
data = {}
State.load("app_name", data)
```

## Mona Character

The project features "Mona" - GitHub's Octocat mascot - in various sprite forms:
- `mona-default.png` - Normal standing/walking
- `mona-dance.png` - Dancing animation
- `mona-dead.png` - Dead/ghost form
- `mona-eating.png` - Eating animation
- `mona-heart.png` - Happy/love animation
- `mona-love.png` - In love
- `mona-notify.png` - Alert/notification
- `mona-code.png` - Coding

## Credits

Built for GitHub Universe 2025 conference attendees.

## License

This code appears to be part of the GitHub Universe conference materials. Check with GitHub for specific licensing terms.
