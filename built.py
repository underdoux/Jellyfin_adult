import os
import shutil
import subprocess
import sys

# Konfigurasi path
SOURCE_DIR = "Jellyfin.Plugin.PhoenixAdult"
BUILD_DIR = os.path.join(SOURCE_DIR, "bin", "Release", "net8.0")
PLUGIN_ZIP = "Jellyfin.Plugin.PhoenixAdult.zip"
SITE_LIST_SRC = "SiteList_updated.json"
SITE_LIST_DEST = os.path.join("data", "SiteList.json")

def check_dotnet():
    """Periksa apakah .NET SDK sudah terinstal"""
    try:
        subprocess.run(["dotnet", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ .NET SDK terdeteksi!")
        return True
    except subprocess.CalledProcessError:
        print("❌ .NET SDK tidak ditemukan! Silakan install .NET SDK dulu.")
        return False

def copy_site_list():
    """Salin file SiteList.json yang sudah diperbarui ke dalam source code"""
    if os.path.exists(SITE_LIST_SRC):
        shutil.copy(SITE_LIST_SRC, SITE_LIST_DEST)
        print("✅ SiteList.json diperbarui!")
    else:
        print("❌ SiteList_updated.json tidak ditemukan!")
        sys.exit(1)

def build_plugin():
    """Menjalankan build menggunakan .NET SDK"""
    try:
        subprocess.run(["dotnet", "build", "--configuration", "Release"], cwd=SOURCE_DIR, check=True)
        print("✅ Build selesai!")
    except subprocess.CalledProcessError:
        print("❌ Build gagal! Periksa error pada output.")
        sys.exit(1)

def package_plugin():
    """Mengemas hasil build menjadi ZIP"""
    if not os.path.exists(BUILD_DIR):
        print("❌ Direktori hasil build tidak ditemukan!")
        sys.exit(1)

    shutil.make_archive("Jellyfin.Plugin.PhoenixAdult", 'zip', BUILD_DIR)
    print(f"✅ Plugin berhasil dikemas ulang: {PLUGIN_ZIP}")

def main():
    """Fungsi utama untuk menjalankan semua langkah"""
    if not check_dotnet():
        sys.exit(1)

    copy_site_list()
    build_plugin()
    package_plugin()

if __name__ == "__main__":
    main()
