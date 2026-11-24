# iconJS

An icon pack for Lawnchair: each app reduced to one or two plain shapes, beige
on a dark ground, one Gruvbox accent each. The designs live in
`tools/icons.py`; `build.sh` turns them into Android icons. Every push builds
`iconJS.apk` and publishes it under Releases.

To add an app: put its component name (from
`adb shell cmd package query-activities --components -a android.intent.action.MAIN -c android.intent.category.LAUNCHER`)
and a design in `tools/icons.py`.
