"""
Quick script to download and install PohLang v0.5.0 official release
"""
import os
import sys
import zipfile
from pathlib import Path
from urllib.request import urlopen, Request

def download_official_release():
    """Download and install PohLang v0.5.0 from official GitHub release"""
    
    plhub_root = Path(__file__).parent
    runtime_dir = plhub_root / "Runtime" / "bin"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    
    # Official release URL
    url = "https://github.com/AlhaqGH/PohLang/releases/download/v0.5.0/pohlang-v0.5.0-windows-x64.zip"
    
    print("Downloading PohLang v0.5.0 official release...")
    print(f"URL: {url}")
    
    try:
        # Download
        req = Request(url, headers={'User-Agent': 'PLHub-Installer'})
        with urlopen(req, timeout=60) as response:
            zip_data = response.read()
        
        print(f"✅ Downloaded {len(zip_data)} bytes")
        
        # Extract
        print("Extracting runtime...")
        import io
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
            # List contents
            print("Archive contents:")
            for name in zf.namelist():
                print(f"  - {name}")
            
            # Extract pohlang.exe
            if 'pohlang.exe' in zf.namelist():
                exe_data = zf.read('pohlang.exe')
                exe_path = runtime_dir / 'pohlang.exe'
                exe_path.write_bytes(exe_data)
                print(f"✅ Extracted to {exe_path}")
            else:
                # Try to find it in a subdirectory
                for name in zf.namelist():
                    if name.endswith('pohlang.exe'):
                        exe_data = zf.read(name)
                        exe_path = runtime_dir / 'pohlang.exe'
                        exe_path.write_bytes(exe_data)
                        print(f"✅ Extracted {name} to {exe_path}")
                        break
                else:
                    print("❌ Error: pohlang.exe not found in archive")
                    return 1
        
        # Update metadata
        import json
        import datetime
        metadata = {
            "pohlang_version": "0.5.0",
            "source_repo": "https://github.com/AlhaqGH/PohLang",
            "build_profile": "release",
            "installed_at": datetime.datetime.now().isoformat(),
            "source": "official_release",
            "release_url": url
        }
        
        metadata_path = plhub_root / "Runtime" / "pohlang_metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2))
        print(f"✅ Updated metadata: {metadata_path}")
        
        # Test runtime
        import subprocess
        print("\nTesting runtime...")
        result = subprocess.run([str(exe_path), '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Runtime working: {result.stdout.strip() if result.stdout else 'OK'}")
        else:
            print(f"⚠️  Runtime test returned code {result.returncode}")
        
        print("\n🎉 PohLang v0.5.0 installed successfully!")
        print(f"Location: {exe_path}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(download_official_release())
