# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of MusicFlow


import os
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance,
                 ImageFilter, ImageFont, ImageOps)

from musicflow import config
from musicflow.helpers import Track


class Thumbnail:
    def __init__(self):
        self.rect = (760, 430)
        self.fill = (255, 255, 255)
        self.muted = (220, 220, 225)
        self.mask = Image.new("L", self.rect, 0)
        self.font_title = ImageFont.truetype("musicflow/helpers/Raleway-Bold.ttf", 34)
        self.font_meta = ImageFont.truetype("musicflow/helpers/Inter-Light.ttf", 24)
        self.font_small = ImageFont.truetype("musicflow/helpers/Inter-Light.ttf", 20)
        self.session: aiohttp.ClientSession | None = None

    async def start(self) -> None:
        self.session = aiohttp.ClientSession()
    async def close(self) -> None:
        await self.session.close()

    async def save_thumb(self, output_path: str, url: str) -> str:
        async with self.session.get(url) as resp:
            with open(output_path, "wb") as f: f.write(await resp.read())
        return output_path

    async def generate(self, song: Track, size=(1280, 720)) -> str:
        try:
            os.makedirs("cache", exist_ok=True)
            output = f"cache/{song.id}.png"
            if os.path.exists(output):
                return output
            temp = f"cache/temp_{song.id}.jpg"
            await self.save_thumb(temp, song.thumbnail)
            source = Image.open(temp).convert("RGB")
            canvas = ImageOps.fit(source, size, method=Image.Resampling.LANCZOS)
            background = canvas.filter(ImageFilter.GaussianBlur(32))
            background = ImageEnhance.Brightness(background).enhance(0.34)
            image = background.convert("RGBA")
            art = ImageOps.fit(source, self.rect, method=Image.Resampling.LANCZOS)
            mask = Image.new("L", self.rect, 0)
            ImageDraw.Draw(mask).rounded_rectangle((0, 0, self.rect[0]-1, self.rect[1]-1), radius=24, fill=255)
            art.putalpha(mask)
            image.alpha_composite(art, (260, 34))

            draw = ImageDraw.Draw(image)
            title = (song.title or "Unknown track").strip()
            artist = (song.channel_name or "Unknown artist").strip()
            draw.text((58, 505), title[:42], font=self.font_title, fill=self.fill)
            draw.text((58, 550), artist[:42], font=self.font_meta, fill=self.muted)
            draw.text((58, 600), f"Requested by {song.user or 'MusicFlow user'}", font=self.font_small, fill=self.muted)
            draw.text((58, 640), "MusicFlow", font=self.font_small, fill=self.fill)
            draw.text((1060, 640), song.duration or "", font=self.font_small, fill=self.muted)
            image.save(output, "PNG", optimize=True)
            try:
                os.remove(temp)
            except OSError:
                pass
            return output
        except Exception:
            return config.DEFAULT_THUMB
