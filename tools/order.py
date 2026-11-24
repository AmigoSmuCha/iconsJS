SECTIONS = [
    ("Everyday", ["phone", "messages", "contacts", "camera", "photos", "gmail", "seznam_email", "firefox",
                  "chrome", "maps", "clock", "calendar", "calculator", "settings", "recorder", "playstore",
                  "files", "materialfiles", "keep", "translate", "findmydevice", "safety", "wallet", "lawnchair"]),
    ("Unihertz tools", ["sysmanager", "game", "nfc", "student", "toolbox", "radio", "feedback", "remote"]),
    ("Music, video and the rest", ["spotify", "shazam", "ra", "vlc", "libretube", "crunchyroll", "discord",
                                   "pinterest", "playgames_sword", "anki", "obsidian", "github", "claude"]),
    ("Money, ID and security", ["revolut", "kb", "isic", "authenticator", "vpn", "protonpass"]),
    ("Getting around and home", ["pid", "jizdnirady", "zasilkovna", "smartlife"]),
    ("Your own apps", ["lockjs", "notejs", "honzatx", "honzatracker"]),
    ("Calendar: the date changes every day", ["cal:1", "cal:9", "cal:24", "cal:31"]),
]

icons.ORDER[:] = [k for _, ks in SECTIONS for k in ks if not k.startswith("cal:")]
