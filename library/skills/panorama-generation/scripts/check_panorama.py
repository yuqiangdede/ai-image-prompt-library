#!/usr/bin/env python3
"""检查全景图片几何规格，并给出左右接缝差异预警。

依赖：Pillow（pip install Pillow）。像素差异不能证明是否真的为球面全景。
用法：python scripts/check_panorama.py path/to/panorama.jpg
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageStat
except ImportError:
    print("缺少 Pillow：请执行 python -m pip install Pillow", file=sys.stderr)
    sys.exit(2)


def main() -> int:
    parser = argparse.ArgumentParser(description="检查等距柱状全景宽高与左右边缘差异")
    parser.add_argument("image", type=Path, help="全景图路径")
    parser.add_argument("--min-width", type=int, default=2048, help="建议的最小宽度，默认 2048")
    parser.add_argument("--seam-threshold", type=float, default=30.0, help="左右首尾列平均 RGB 差异提醒阈值")
    args = parser.parse_args()

    if not args.image.is_file():
        print(f"FAIL: 文件不存在：{args.image}", file=sys.stderr)
        return 2

    try:
        with Image.open(args.image) as source:
            source.verify()
        with Image.open(args.image) as source:
            width, height = source.size
            print(f"图像：{args.image}\n尺寸：{width} × {height}\n格式：{source.format}")
            if width == 0 or height == 0:
                print("FAIL: 无效图像尺寸")
                return 2

            if abs(width / height - 2.0) > 0.01:
                print("FAIL: 宽高不是 2:1 等距柱状全景比例")
                return 2
            print("PASS: 2:1 宽高比例")

            if width < args.min_width:
                print(f"WARN: 水平分辨率低于建议值 {args.min_width}px；可以预览，但可能模糊")
            else:
                print("PASS: 水平分辨率达到建议值")

            rgb = source.convert("RGB")
            # 比较水平环绕接壤的左右最后/最初一列；差异仅供人工查缝参考。
            left = rgb.crop((0, 0, 1, height))
            right = rgb.crop((width - 1, 0, width, height))
            difference = ImageChops.difference(left, right)
            mean_rgb = ImageStat.Stat(difference).mean
            mean = sum(mean_rgb) / 3
            print(f"边缘 RGB 平均绝对差：{mean:.2f} / 255（越低越连续，不能作为绝对质量分数）")
            if mean > args.seam_threshold:
                print("WARN: 首尾列有较大像素差，建议在球面查看器中检查接缝")
            else:
                print("INFO: 首尾列差异不大，仍需球面目视验收")
            print("INFO: 比例和像素差异无法证明 360°×180° 投影及空间一致性")
            return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: 无法解析图像：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())