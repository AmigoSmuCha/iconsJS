"""iconJS icon designs: one source for the SVG previews and the Android drawables.

Every icon is drawn on a 24-unit grid (the glyph box), which sits in the middle
of a 108 dp adaptive-icon canvas: unit = 2 dp, offset 30 dp, so the glyph stays
inside the 66 dp safe zone that launchers keep when they mask icons to a shape.

Material: the lockJS icon's. A dark ground, sand-coloured lines of one weight,
and at most one hot orange element per icon. Shapes say what the app does,
never the brand's own logo.
"""
import math
import re

GROUND = "#201d1b"
COLOURS = {"s": "#d5c4a1", "o": "#fd4a00", "g": GROUND}
W = 2.0            # line weight in grid units
UNIT, OFF = 2.0, 30.0


def T(v):          # grid -> canvas coordinate
    return round(v * UNIT + OFF, 3)


def S(v):          # grid -> canvas length
    return round(v * UNIT, 3)


# Accents, rotated across the set: Parchment Gruvbox's red, orange, blue and
# olive, plus the rest of the stock Gruvbox bright set.
ACCENTS = ["#fe8019", "#83a598", "#b8bb26", "#d3869b", "#fabd2f", "#8ec07c", "#fb4934", "#458588", "#98971a"]


class Icon:
    def __init__(self, accent="#fd4a00"):
        self.parts = []          # (path_d_in_canvas, fill, stroke, width, cap, join)
        self.accent = accent

    def _add(self, d, c, filled, w=W, cap="square", join="miter"):
        col = self.accent if c == "o" else COLOURS[c]
        if filled:
            self.parts.append((d, col, None, 0, cap, join))
        else:
            self.parts.append((d, None, col, S(w), cap, join))
        return self

    # filled shapes
    def rect(self, x, y, w, h, c="s"):
        return self._add("M%s %sh%sv%sh%sz" % (T(x), T(y), S(w), S(h), S(-w)), c, True)

    def dot(self, cx, cy, r, c="s"):
        return self._add(circle_d(cx, cy, r), c, True)

    def poly(self, pts, c="s"):
        return self._add(poly_d(pts, True), c, True)

    def path(self, d, c="s"):
        return self._add(grid_path(d), c, True)

    # strokes
    def line(self, pts, c="s", w=W, closed=False, cap="square", join="miter"):
        return self._add(poly_d(pts, closed), c, False, w, cap, join)

    def box(self, x, y, w, h, c="s", lw=W):
        return self.line([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], c, lw, closed=True)

    def ring(self, cx, cy, r, c="s", w=W):
        return self._add(circle_d(cx, cy, r), c, False, w, "butt")

    def arc(self, cx, cy, r, a0, a1, c="s", w=W, cap="butt"):
        """Degrees, 0 = right, clockwise on screen, from a0 to a1 (a1 > a0)."""
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        large = 1 if (a1 - a0) % 360 > 180 else 0
        d = "M%s %sA%s %s 0 %d 1 %s %s" % (T(x0), T(y0), S(r), S(r), large, T(x1), T(y1))
        return self._add(d, c, False, w, cap)

    def stroke_path(self, d, c="s", w=W, cap="square", join="miter"):
        return self._add(grid_path(d), c, False, w, cap, join)


def circle_d(cx, cy, r):
    return "M%s %sa%s %s 0 1 0 %s 0a%s %s 0 1 0 %s 0z" % (
        T(cx - r), T(cy), S(r), S(r), S(2 * r), S(r), S(r), S(-2 * r))


def poly_d(pts, closed):
    d = "M%s %s" % (T(pts[0][0]), T(pts[0][1]))
    for x, y in pts[1:]:
        d += "L%s %s" % (T(x), T(y))
    return d + ("z" if closed else "")


def grid_path(d):
    """Absolute M L H V A C Z commands, in grid units -> canvas."""
    out = []
    for cmd, args in re.findall(r"([MLHVACZ])([^MLHVACZ]*)", d):
        n = [float(v) for v in re.findall(r"-?\d*\.?\d+", args)]
        if cmd in "ML":
            out.append(cmd + " ".join("%s" % (T(v)) for v in n))
        elif cmd in "HV":
            out.append(cmd + "%s" % T(n[0]))
        elif cmd == "C":
            out.append("C" + " ".join("%s" % T(v) for v in n))
        elif cmd == "A":
            rx, ry, rot, la, sw, x, y = n
            out.append("A%s %s %g %d %d %s %s" % (S(rx), S(ry), rot, la, sw, T(x), T(y)))
        else:
            out.append("z")
    return "".join(out)


# ---------------------------------------------------------------------------
# The designs: each app reduced to the one thing it is about, everything else
# taken away (like the Honza Tracker dot, or lockJS's panel rectangles).
# key -> (label, concept, draw function). Glyphs stay within about 5..19.
# ---------------------------------------------------------------------------
ICONS = {}


def icon(key, label, concept):
    def wrap(fn):
        ICONS[key] = (label, fn, concept)
        return fn
    return wrap


@icon("phone", "Phone", "two people")
def _(i):
    i.dot(7.8, 12, 3.2); i.dot(16.2, 12, 3.2, "o")


@icon("messages", "Messages", "one line from them, one from you")
def _(i):
    i.rect(4.5, 8, 10, 3.2); i.rect(9.5, 12.8, 10, 3.2, "o")


@icon("contacts", "Contacts", "someone")
def _(i):
    i.dot(12, 8.5, 3.2); i.rect(7, 14.5, 10, 3.5)


@icon("camera", "Camera", "the lens and the moment")
def _(i):
    i.ring(12, 12, 6.5); i.dot(12, 12, 2.2, "o")


@icon("photos", "Photos", "the grid")
def _(i):
    i.rect(5.5, 5.5, 5.7, 5.7); i.rect(12.8, 5.5, 5.7, 5.7, "o")
    i.rect(5.5, 12.8, 5.7, 5.7); i.rect(12.8, 12.8, 5.7, 5.7)


@icon("gmail", "Gmail", "a letter")
def _(i):
    i.rect(5, 7.5, 14, 9)


@icon("seznam_email", "Seznam Email", "a letter, in colour")
def _(i):
    i.rect(5, 7.5, 14, 9, "o")


@icon("firefox", "Firefox", "a world, filled in")
def _(i):
    i.accent = "#fe8019"
    i.dot(12, 12, 6, "o")


@icon("chrome", "Chrome", "an open world")
def _(i):
    i.ring(12, 12, 6.5)


@icon("maps", "Maps", "heading somewhere")
def _(i):
    i.poly([(7, 18.5), (17, 18.5), (12, 9.5)])
    i.dot(12, 5.8, 1.8, "o")


@icon("clock", "Clock", "the hands")
def _(i):
    i.rect(6.5, 5, 3, 9.5); i.rect(11, 15.5, 8.5, 3, "o")


@icon("calendar", "Calendar", "the day")
def _(i):
    calendar_day(i, 31)


@icon("calculator", "Calculator", "equals")
def _(i):
    i.rect(6, 8.5, 12, 3); i.rect(6, 12.5, 12, 3, "o")


@icon("settings", "Settings", "a switch")
def _(i):
    i.line([(6.3, 12), (11.3, 12)], w=5, cap="round")
    i.dot(17.6, 12, 2.3, "o")


@icon("recorder", "Recorder", "recording")
def _(i):
    i.dot(7.5, 12, 3, "o"); i.rect(12.5, 10.8, 7, 2.4)


@icon("playstore", "Play Store", "play, in colour")
def _(i):
    i.poly([(8, 6), (8, 18), (18, 12)], "o")


@icon("libretube", "LibreTube", "play")
def _(i):
    i.poly([(8, 6), (8, 18), (18, 12)])


@icon("vlc", "VLC", "play and stop")
def _(i):
    i.poly([(5, 7), (5, 17), (12, 12)]); i.rect(14.5, 9.5, 5, 5, "o")


@icon("crunchyroll", "Crunchyroll", "an episode, partly watched")
def _(i):
    i.rect(4.5, 6.5, 15, 8.5); i.rect(4.5, 17, 8, 2, "o")


@icon("files", "Files", "a tab and what is behind it")
def _(i):
    i.rect(5, 5, 5, 2.5, "o"); i.rect(5, 9.5, 14, 9)


@icon("materialfiles", "Material Files", "a branch of files")
def _(i):
    i.rect(5, 5, 2.5, 14)
    i.rect(9.5, 6.5, 9.5, 2.5); i.rect(9.5, 15, 9.5, 2.5, "o")


@icon("keep", "Keep", "an idea")
def _(i):
    i.dot(12, 10, 4, "o"); i.rect(10, 16, 4, 2)


@icon("translate", "Translate", "two languages")
def _(i):
    i.dot(7.5, 12, 3.4); i.ring(16.5, 12, 3, "o")


@icon("findmydevice", "Find My Device", "your phone, found")
def _(i):
    i.rect(9, 9, 6, 10.5); i.dot(12, 5.5, 1.8, "o")


@icon("safety", "Safety", "help")
def _(i):
    i.rect(10.5, 6, 3, 12, "o"); i.rect(6, 10.5, 12, 3, "o")


@icon("wallet", "Wallet", "cards")
def _(i):
    i.rect(5, 6.5, 11, 2.6); i.rect(6.5, 10.7, 11, 2.6); i.rect(8, 14.9, 11, 2.6, "o")


@icon("lawnchair", "Lawnchair", "the app grid")
def _(i):
    for y in (7, 12, 17):
        for x in (7, 12, 17):
            i.dot(x, y, 1.4, "o" if (x, y) == (12, 12) else "s")


@icon("sysmanager", "System Manager", "mostly full")
def _(i):
    i.rect(4.5, 10.4, 10, 3.2, "o"); i.rect(16.2, 10.4, 3.3, 3.2)


@icon("game", "Game mode", "the pad and a button")
def _(i):
    i.rect(4.5, 10.7, 8, 2.6); i.rect(7.2, 8, 2.6, 8)
    i.dot(16.5, 12, 2.8, "o")


@icon("nfc", "NFC", "a touch")
def _(i):
    i.dot(7, 12, 2.5, "o"); i.arc(7, 12, 6.5, -45, 45, w=2.4)


@icon("student", "Student mode", "the cap")
def _(i):
    i.poly([(12, 7.5), (19.5, 11.5), (12, 15.5), (4.5, 11.5)])


@icon("toolbox", "Toolbox", "level")
def _(i):
    i.rect(5, 14, 14, 2.6); i.dot(12, 9.5, 2.2, "o")


@icon("radio", "FM Radio", "tuned in")
def _(i):
    i.rect(4.5, 11, 5, 2); i.rect(11, 7.5, 2, 9, "o"); i.rect(14.5, 11, 5, 2)


@icon("feedback", "Feedback", "something to say")
def _(i):
    i.rect(10.75, 5.5, 2.5, 9, "o"); i.rect(10.75, 16.5, 2.5, 2.5, "o")


@icon("remote", "IR Remote", "a beam")
def _(i):
    i.dot(6.5, 12, 2.8, "o"); i.rect(11, 10.8, 3.4, 2.4); i.rect(16, 10.8, 3.4, 2.4)


@icon("spotify", "Spotify", "the levels")
def _(i):
    for x, h, c in ((7, 7, "s"), (12, 13, "o"), (17, 10, "s")):
        i.rect(x - 1.6, 18.5 - h, 3.2, h, c)


@icon("shazam", "Shazam", "a sound, caught")
def _(i):
    for x, h, c in ((6.2, 4, "s"), (9.1, 8, "s"), (12, 12, "o"), (14.9, 8, "s"), (17.8, 4, "s")):
        i.rect(x - 0.8, 12 - h / 2, 1.6, h, c)


@icon("ra", "Resident Advisor", "a record")
def _(i):
    i.ring(12, 12, 7, w=1.8); i.ring(12, 12, 3, "o", w=1.8)


@icon("discord", "Discord", "in voice")
def _(i):
    i.arc(12, 13, 6.5, 180, 360)
    i.rect(4.5, 15, 3, 4); i.rect(16.5, 15, 3, 4)


@icon("pinterest", "Pinterest", "uneven columns")
def _(i):
    i.rect(5.5, 5, 5.5, 8); i.rect(5.5, 14.5, 5.5, 4.5)
    i.rect(13, 5, 5.5, 4.5, "o"); i.rect(13, 11, 5.5, 8)


@icon("playgames_sword", "Shakes & Fidget", "a blade")
def _(i):
    i.line([(9, 15), (19, 5)], w=2.6, cap="butt"); i.dot(6, 18, 1.8, "o")


@icon("anki", "AnkiDroid", "a card and its other side")
def _(i):
    i.rect(5, 11.5, 7.5, 7.5); i.rect(13.5, 5, 5.5, 5.5, "o")


@icon("obsidian", "Obsidian", "a crystal")
def _(i):
    i.poly([(12, 4.5), (17, 8.5), (17, 15.5), (12, 19.5), (7, 15.5), (7, 8.5)])


@icon("github", "GitHub", "a branch")
def _(i):
    i.dot(8, 6.5, 2.2); i.dot(8, 17.5, 2.2); i.dot(16, 10, 2.2, "o")


@icon("claude", "Claude", "an asterisk")
def _(i):
    i.accent = "#fe8019"
    for deg in (90, 30, 150):
        dx, dy = 6.8 * math.cos(math.radians(deg)), 6.8 * math.sin(math.radians(deg))
        i.line([(12 - dx, 12 - dy), (12 + dx, 12 + dy)], "o", w=2.8, cap="butt")


@icon("revolut", "Revolut", "a card")
def _(i):
    i.rect(4.5, 6.5, 15, 2.5); i.rect(4.5, 11, 15, 6.5)


@icon("kb", "KB+", "a roof and pillars")
def _(i):
    i.rect(5, 6, 14, 2.5, "o")
    for x in (6, 10.8, 15.6):
        i.rect(x, 10, 2.4, 8)


@icon("isic", "ISIC", "a face beside the details")
def _(i):
    i.dot(7.5, 12, 2.6, "o"); i.rect(11.5, 8, 8, 8)


@icon("authenticator", "Authenticator", "a code")
def _(i):
    for n, c in enumerate(("s", "s", "o")):
        i.rect(4.6 + n * 5.2, 10, 4, 4, c)


@icon("vpn", "Proton VPN", "inside")
def _(i):
    i.stroke_path("M6 18.5V12A6 6 0 0 1 18 12V18.5", cap="butt")
    i.dot(12, 14.5, 2, "o")


@icon("protonpass", "Proton Pass", "a key")
def _(i):
    i.ring(7.5, 12, 3.5, "o", w=2.2); i.rect(13.2, 10.9, 6.5, 2.2)


@icon("pid", "PID Lítačka", "stops on a line")
def _(i):
    i.dot(6, 12, 2.4); i.dot(12, 12, 2.4, "o"); i.dot(18, 12, 2.4)


@icon("jizdnirady", "Jízdní řády", "times in rows")
def _(i):
    i.rect(6, 6.5, 12, 2.6); i.rect(6, 10.7, 12, 2.6, "o"); i.rect(6, 14.9, 12, 2.6)


@icon("zasilkovna", "Zásilkovna", "a parcel, taped")
def _(i):
    i.rect(6, 6, 4.2, 12); i.rect(11.2, 6, 1.6, 12, "o"); i.rect(13.8, 6, 4.2, 12)


@icon("smartlife", "Smart Life", "home, the light on")
def _(i):
    i.poly([(5, 11), (19, 11), (12, 5)]); i.rect(10.5, 13.5, 3, 3, "o")


@icon("lockjs", "lockJS", "the lock screen's panels")
def _(i):
    i.rect(7, 6, 10, 3, "o")
    i.rect(7, 11, 10, 7)


@icon("notejs", "noteJS", "a list, one ticked")
def _(i):
    for y, c in ((6, "o"), (10.5, "s"), (15, "s")):
        i.rect(5, y, 3, 3, c); i.rect(10, y + 0.5, 9, 2)


@icon("honzatx", "honzaTX", "the dot, sending")
def _(i):
    i.dot(9.5, 14.5, 3.5); i.dot(17, 7, 1.8, "o")


@icon("honzatracker", "Honza Tracker", "you are here")
def _(i):
    i.dot(12, 12, 6.3)


# ---------------------------------------------------------------------------
# The calendar's day icons: the day in the block digits of the clock (focus's G3).
# ---------------------------------------------------------------------------
G3 = {
    "0": ("###", "# #", "# #", "# #", "###"), "1": (" # ", "## ", " # ", " # ", "###"),
    "2": ("###", "  #", "###", "#  ", "###"), "3": ("###", "  #", "###", "  #", "###"),
    "4": ("# #", "# #", "###", "  #", "  #"), "5": ("###", "#  ", "###", "  #", "###"),
    "6": ("###", "#  ", "###", "# #", "###"), "7": ("###", "  #", "  #", "  #", "  #"),
    "8": ("###", "# #", "###", "# #", "###"), "9": ("###", "# #", "###", "  #", "###"),
}


def calendar_day(i, day):
    """Just the day, centred, in the clock's block digits."""
    digits = str(day)
    px = 2.0
    width = len(digits) * 3 * px + (len(digits) - 1) * px
    x0, y0 = 12 - width / 2, 12 - 2.5 * px
    for n, ch in enumerate(digits):
        for r, row in enumerate(G3[ch]):
            for c, cell in enumerate(row):
                if cell == "#":
                    i.rect(x0 + n * 4 * px + c * px, y0 + r * px, px, px)


# ---------------------------------------------------------------------------
# Which app gets which icon (full component names, as the launcher reports them)
# ---------------------------------------------------------------------------
# Left out on purpose (they keep their own icons): com.aphexspin.chrome,
# com.aphexspin.wallpaper, com.chromesigil.icons, com.cornholio.ncs, cz.studio9.sa
APPS = """
com.agui.systemmanager/.ui.activity.MainActivity sysmanager
com.android.chrome/com.google.android.apps.chrome.Main chrome
com.android.deskclock/.DeskClock clock
com.android.settings/.Settings settings
com.android.soundrecorder/.SoundRecorder recorder
com.android.vending/.AssetBrowserActivity playstore
com.google.android.apps.maps/com.google.android.maps.MapsActivity maps
com.google.android.apps.messaging/.ui.ConversationListActivity messages
com.google.android.apps.photos/.home.HomeActivity photos
com.google.android.calculator/com.android.calculator2.Calculator calculator
com.google.android.calendar/com.android.calendar.AllInOneActivity calendar
com.google.android.contacts/com.android.contacts.activities.PeopleActivity contacts
com.google.android.dialer/.extensions.GoogleDialtactsActivity phone
com.google.android.gm/.ConversationListActivityGmail gmail
com.mediatek.camera/.CameraLauncher camera
app.lawnchair.nightly/app.lawnchair.LawnchairLauncher lawnchair
com.crunchyroll.crunchyroid/com.ellation.crunchyroll.presentation.startup.StartupActivity crunchyroll
com.google.android.apps.walletnfcrel/com.google.commerce.tapandpay.android.wallet.WalletActivity wallet
com.pinterest/.activity.PinterestActivity pinterest
com.shazam.android/.activities.SplashActivity shazam
com.spotify.music/.MainActivity spotify
cz.seznam.email/.HomeActivity seznam_email
com.agui.game/.ui.PrepareEnteringGameModeActivity game
com.agui.nfc/.MainActivity nfc
com.agui.studentmodel/.StudentModelActivity student
com.agui.toolbox/.EntryActivity toolbox
com.android.fmradio/.FmMainActivity radio
com.example.feedback/.MainActivity feedback
com.google.android.apps.adm/.activities.MainActivity findmydevice
com.google.android.apps.nbu.files/.home.HomeActivity files
com.google.android.apps.safetyhub/.LauncherActivity safety
com.google.android.keep/.activities.BrowseActivity keep
com.tiqiaa.icontrol/.WelcomeActivity remote
ch.protonvpn.android/.RoutingActivity vpn
com.anthropic.claude/.mainactivity.MainActivity claude
com.azure.authenticator/.ui.LaunchActivity authenticator
com.bootiq2.gtsisic/app.futured.aliveapp.AppActivity isic
com.discord/.main.MainDefault discord
com.github.android/.main.MainActivity github
com.github.libretube/.Default libretube
com.google.android.apps.translate/.TranslateActivity translate
com.honzatracker/.MainActivity honzatracker
com.honzatx/.MainActivity honzatx
com.ichi2.anki/.IntentHandler anki
com.lockjs/.MainActivity lockjs
com.notejs/.MainActivity notejs
com.playagames.shakesfidget/com.unity3d.player.UnityPlayerActivity playgames_sword
com.revolut.revolut/com.revolut.ui.login.pin.LoginActivity revolut
com.tuya.smartlife/com.smart.ThingSplashActivity smartlife
cz.dpp.praguepublictransport/.activities.GuideActivity pid
cz.kb.ndb/kb.ndb.app.system.MainActivity kb
cz.mafra.jizdnirady/.activity.SplashActivity jizdnirady
cz.zasilkovna.app/.MainActivity zasilkovna
md.obsidian/.MainActivity obsidian
me.zhanghai.android.files/.filelist.FileListActivity materialfiles
net.residentadvisor.raguide/.view.main.MainActivity ra
org.mozilla.firefox/.App firefox
org.videolan.vlc/.StartActivity vlc
proton.android.pass/.ui.MainActivity protonpass
"""


def apps():
    out = []
    for line in APPS.strip().splitlines():
        comp, key = line.split()
        pkg, act = comp.split("/")
        if act.startswith("."):
            act = pkg + act
        out.append((pkg + "/" + act, key))
    return out


ORDER = []      # icon keys in the order the accents are dealt out


def accent_for(key):
    keys = ORDER or list(ICONS)
    return ACCENTS[keys.index(key) % len(ACCENTS)] if key in keys else ACCENTS[0]


def build(key):
    i = Icon(accent_for(key))
    ICONS[key][1](i)
    return i


def svg(i, size=108, masked=False):
    body = []
    for d, fill, stroke, w, cap, join in i.parts:
        if fill:
            body.append('<path d="%s" fill="%s"/>' % (d, fill))
        else:
            body.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s" '
                        'stroke-linecap="%s" stroke-linejoin="%s"/>' % (d, stroke, w, cap, join))
    if masked:      # how a launcher shows it: masked to a rounded square
        bg = '<rect x="0" y="0" width="108" height="108" rx="30" fill="%s"/>' % GROUND
    else:
        bg = '<rect width="108" height="108" fill="%s"/>' % GROUND
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 108 108">'
            '%s%s</svg>' % (size, size, bg, "".join(body)))


if __name__ == "__main__":
    used = {k for _, k in apps()}
    missing = used - set(ICONS)
    unused = set(ICONS) - used
    print(len(apps()), "apps,", len(ICONS), "designs; missing:", missing, "unused:", unused)
