# scraper-site
Hello, through this code, you can save photos of a specific series of cars on the divar.ir site, which is defined in the code, and save their photos in the system. :)


without docker
(only tested on rockylinux 9)
```bash
sudo dnf install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm -y
pip install -r requirements.txt
python3 scraper.py
```

with docker 
```bash
docker compose up 
```
