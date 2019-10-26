# wannapay
WanaPay 和你Pay - A robot application which can pay Gov. bills dollar by dollar with PPSHK

Build Procedure:
1. python3 db.py
   to create 3 json files
2. pyuic5 wannapay.ui -x -o wannapay_ui.py
3. pyuic5 position.ui -x -o position_ui.py

Run:
python3 wannapay.py

The wannapay.exe can be created by:
pyinstaller --noconsole wannapay.py
