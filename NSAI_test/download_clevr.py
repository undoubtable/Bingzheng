#!/usr/bin/env python3
"""
download_clevr.py

下载并解压 CLEVR 数据集到指定目录的脚本。

默认 URL 使用常见的 CLEVR 数据托管地址，但如果这些链接不可用，
可以通过命令行参数传入自定义的 images/questions URL。

示例：
python download_clevr.py --dest data/clevr
python download_clevr.py --dest data/clevr --images-url <URL> --questions-url <URL>

"""
import argparse
import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path


DEFAULT_IMAGES_URL = "http://dl.caffe.berkeleyvision.org/clevr/CLEVR_v1.0_images.zip"
DEFAULT_QUESTIONS_URL = "http://dl.caffe.berkeleyvision.org/clevr/CLEVR_v1.0_questions.zip"


def download_url(url: str, out_path: Path):
    """Download a URL to out_path with a simple progress indicator."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url}\n  -> {out_path}")

    def _reporthook(block_num, block_size, total_size):
        if total_size <= 0:
            return
        downloaded = block_num * block_size
        pct = downloaded / total_size * 100
        pct = min(100.0, pct)
        end = "\r" if downloaded < total_size else "\n"
        print(f"  {pct:5.1f}% ({downloaded}/{total_size} bytes)", end=end)

    try:
        urllib.request.urlretrieve(url, filename=str(out_path), reporthook=_reporthook)
    except Exception as e:
        print(f"ERROR: failed to download {url}: {e}")
        return False
    return True


def extract_zip(zip_path: Path, dest: Path):
    print(f"Extracting {zip_path} -> {dest}")
    try:
        with zipfile.ZipFile(str(zip_path), 'r') as z:
            z.extractall(path=str(dest))
    except zipfile.BadZipFile:
        print(f"ERROR: Bad zip file: {zip_path}")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Download and extract CLEVR dataset")
    parser.add_argument("--dest", required=True, help="Destination directory to place CLEVR data")
    parser.add_argument("--images-url", default=DEFAULT_IMAGES_URL, help="CLEVR images zip URL")
    parser.add_argument("--questions-url", default=DEFAULT_QUESTIONS_URL, help="CLEVR questions zip URL")
    parser.add_argument("--no-extract", action="store_true", help="Do not extract zip files")
    parser.add_argument("--keep-zip", action="store_true", help="Keep zip files after extraction")
    args = parser.parse_args()

    dest_dir = Path(args.dest).expanduser().resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)

    images_url = args.images_url
    questions_url = args.questions_url

    images_zip = dest_dir / "CLEVR_images.zip"
    questions_zip = dest_dir / "CLEVR_questions.zip"

    ok = download_url(images_url, images_zip)
    if not ok:
        print("Failed to download images. You can pass a different --images-url.")
        sys.exit(1)

    ok = download_url(questions_url, questions_zip)
    if not ok:
        print("Failed to download questions. You can pass a different --questions-url.")
        sys.exit(1)

    if not args.no_extract:
        # extract both zips
        ok1 = extract_zip(images_zip, dest_dir)
        ok2 = extract_zip(questions_zip, dest_dir)
        if not ok1 or not ok2:
            print("Extraction failed for one or more archives. Please check the zip files.")
            sys.exit(2)

        if not args.keep_zip:
            try:
                images_zip.unlink()
                questions_zip.unlink()
            except Exception:
                pass

    print("CLEVR download + extraction finished.")
    print("目录内容示例:")
    for p in sorted(dest_dir.iterdir()):
        print("  -", p.name)
    print("\n注意：如果默认 URL 无法访问，请到 https://cs.stanford.edu/people/jcjohns/clevr/ 查找替代下载地址，或通过 --images-url/--questions-url 指定。")


if __name__ == '__main__':
    main()
