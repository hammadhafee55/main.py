name: Build APK

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          sudo apt update
          sudo apt install -y python3-pip python3-setuptools python3-wheel
          pip3 install --upgrade Cython
          pip3 install buildozer
      
      - name: Build APK
        run: |
          cd path/to/your/project
          buildozer init
          buildozer android debug
          
      - name: Upload APK
        uses: actions/upload-artifact@v2
        with:
          name: my-app.apk
          path: main.py/Recipe.py.py
