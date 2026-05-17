#!/usr/bin/env python3
"""
网页截图工具 - 使用Playwright截图
"""
import sys, os, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk
import subprocess

class App:
    def __init__(self, root):
        self.root = root
        root.title("网页截图工具 v1.0")
        root.geometry("600x450")
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#7b1fa2", height=50)
        f.pack(fill="x")
        tk.Label(f, text="📸 网页截图工具", font=("Arial",14,"bold"),
                 fg="white", bg="#7b1fa2").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        tk.Label(main, text="输入网址：", font=("Arial",11)).pack(anchor="w", pady=5)
        self.url_entry = tk.Entry(main, font=("Arial",11), width=50)
        self.url_entry.pack(fill="x", pady=5)
        self.url_entry.insert(0, "https://github.com/102839544")
        
        # 选项
        of = tk.Frame(main)
        of.pack(fill="x", pady=10)
        self.full_page = tk.BooleanVar(value=True)
        tk.Checkbutton(of, text="完整页面截图", variable=self.full_page,
                       font=("Arial",10)).pack(anchor="w")
        
        tk.Button(main, text="📷 截图", command=self.screenshot,
                  bg="#7b1fa2", fg="white", font=("Arial",11,"bold"),
                  padx=30, pady=8).pack(pady=15)
        
        self.lb = tk.Listbox(main, font=("Consolas",9), bg="#f3e5f5", height=8)
        self.lb.pack(fill="both", expand=True, pady=5)
        
        self.status = tk.Label(main, text="需要安装 playwright：pip install playwright && playwright install",
                               font=("Arial",9), fg="gray")
        self.status.pack()
    
    def screenshot(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("提示", "请输入网址")
            return
        
        if not url.startswith("http"):
            url = "https://" + url
        
        out_dir = filedialog.askdirectory(title="选择保存目录")
        if not out_dir: return
        
        try:
            self.status.config(text="截图中...")
            self.root.update()
            
            # 使用 playwright 截图
            import asyncio
            from playwright.async_api import async_playwright
            
            async def take_screenshot():
                async with async_playwright() as p:
                    browser = await p.chromium.launch()
                    page = await browser.new_page()
                    await page.goto(url)
                    
                    filename = url.replace("https://","").replace("http://","").replace("/","_")[:30]
                    out_path = str(Path(out_dir) / f"{filename}.png")
                    
                    if self.full_page.get():
                        await page.screenshot(path=out_path, full_page=True)
                    else:
                        await page.screenshot(path=out_path)
                    
                    await browser.close()
                    return out_path
            
            out_path = asyncio.run(take_screenshot())
            
            self.lb.insert(0, f"{Path(out_path).name}")
            self.status.config(text=f"✅ 截图成功：{out_path}")
            messagebox.showinfo("完成", f"截图已保存至：\n{out_path}")
            
        except ImportError:
            messagebox.showerror("缺少依赖", 
                "请安装：\n\npip install playwright\nplaywright install")
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.status.config(text="❌ 截图失败")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
