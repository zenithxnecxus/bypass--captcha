#!/usr/bin/env python3
# universal_captcha_bypass.py
# CAPTCHA Bypass Tool - Auto detect & bypass

import warnings
import requests
import re
import sys
from bs4 import BeautifulSoup
import urllib3

warnings.filterwarnings('ignore')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CaptchaBypass:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def detect_captcha(self, html):
        match = re.search(r'<span[^>]*class="[^"]*btn[^"]*btn-pink[^"]*"[^>]*>(\d+)\s*\+\s*(\d+)\s*=?\s*</span>', html)
        if match:
            return {
                'type': 'btn-pink',
                'num1': int(match.group(1)),
                'num2': int(match.group(2)),
                'expr': f"{match.group(1)} + {match.group(2)}"
            }
        
        match = re.search(r'<div[^>]*class="[^"]*captcha-box[^"]*"[^>]*>(\d+)\s*\+\s*(\d+)\s*=\s*\?</div>', html)
        if match:
            return {
                'type': 'captcha-box',
                'num1': int(match.group(1)),
                'num2': int(match.group(2)),
                'expr': f"{match.group(1)} + {match.group(2)}"
            }
        
        match = re.search(r'(\d+)\s*\+\s*(\d+)\s*=\s*\?', html)
        if match:
            return {
                'type': 'generic',
                'num1': int(match.group(1)),
                'num2': int(match.group(2)),
                'expr': f"{match.group(1)} + {match.group(2)}"
            }
        
        match = re.search(r'(\d+)\s*\+\s*(\d+)\s*=', html)
        if match:
            return {
                'type': 'plain',
                'num1': int(match.group(1)),
                'num2': int(match.group(2)),
                'expr': f"{match.group(1)} + {match.group(2)}"
            }
        
        return None
    
    def detect_login_form(self, html, base_url):
        """Detect login form and extract fields"""
        soup = BeautifulSoup(html, 'html.parser')
        
        forms = soup.find_all('form', method=lambda x: x and x.lower() == 'post')
        
        for form in forms:
            action = form.get('action', '')
            if not action:
                action = base_url
            
]            fields = {}
            for inp in form.find_all('input'):
                name = inp.get('name')
                type_ = inp.get('type', 'text')
                if name and type_ not in ['submit', 'button', 'hidden']:
                    fields[name] = type_
            
            captcha_field = None
            for name, type_ in fields.items():
                if 'captcha' in name.lower():
                    captcha_field = name
                    break
            
            return {
                'action': action,
                'fields': fields,
                'captcha_field': captcha_field
            }
        
        return None
    
    def solve_captcha(self, captcha_data):
        if captcha_data:
            return captcha_data['num1'] + captcha_data['num2']
        return None
    
    def scan(self, target_url):
        print(f" CAPTCHA BYPASS SCANNER")
        print(f"{'-'*60}")
        print(f"Target: {target_url}")
        print(f"{'-'*60}\n")
        
      print("[1] Mengakses halaman")
        try
            r = self.session.get(target_url, timeout=30)
        except Exception as e:
            print(f"[-] Gagal akses: {e}")
            return
        
        html = r.text
        
        print("[2] Mendeteksi CAPTCHA")
        captcha = self.detect_captcha(html)
        
        if captcha:
            print(f"    [+] CAPTCHA ditemukan!")
            print(f"    [+] Type: {captcha['type']}")
            print(f"    [+] Expression: {captcha['expr']}")
            
            result = self.solve_captcha(captcha)
            print(f"    [+] Result: {result}")
        else:
            print("    [-] CAPTCHA tidak ditemukan!")
            return
        
        
        print("\n[3] Mendeteksi form login...")
        form = self.detect_login_form(html, target_url)
        
        if not form:
            print("    [-] Form login tidak ditemukan!")
            return
        
        print(f"    [+] Login URL: {form['action']}")
        print(f"    [+] Fields: {', '.join(form['fields'].keys())}")
        if form['captcha_field']:
            print(f"    [+] CAPTCHA Field: {form['captcha_field']}")
        
        

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description=" CAPTCHA Bypass Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 captcha_bypass.py -u example.com/sim-epk/auth/login/
  python3 ucaptcha_bypass.py -u example.com/login-view
  python3 captcha_bypass.py -f targets.txt
        """
    )
    
    parser.add_argument("-u", "--url", help="Target URL")
    parser.add_argument("-f", "--file", help="File with targets (one per line)")
    
    args = parser.parse_args()
    
    scanner = CaptchaBypass()
    
    if args.file:
        with open(args.file) as f:
            targets = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"[+] Scanning {len(targets)} targets")
        for target in targets:
            scanner.scan(target)
            print("\n")
    elif args.url:
        scanner.scan(args.url)
    else:
        print("Usage:")
        print("  python3 captcha_bypass.py -u https://target.com/login")
        print("  python3 captcha_bypass.py -f targets.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
