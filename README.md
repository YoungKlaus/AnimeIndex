# 📺 Anime Index (Telegram 动漫索引)

> 一个极速、自动更新的 Telegram 动漫资源搜索引擎。

此项目利用 **GitHub Actions** 每日自动抓取 Telegram 频道中的视频资源，并生成一个纯静态的搜索页面。旨在解决 Telegram 频道历史文件难以检索、无法多关键字筛选的痛点。

## 🔗 在线访问

**👉 点击进入索引库： [https://youngklaus.github.io/AnimeIndex/](https://youngklaus.github.io/AnimeIndex/)**

---

## ✨ 项目特点

*   **⚡️ 极速体验**：纯静态页面，基于本地 JSON 索引，搜索无延迟。
*   **🔍 高级搜索**：支持多关键字筛选（例如输入 `进击 1080p` 即可精准定位）。
*   **📱 多端适配**：完美支持 PC、iPad 和 手机端访问。
*   **🔄 自动更新**：后端爬虫每天自动增量抓取最新发布的动漫资源。
*   **🚀 直达链接**：点击按钮直接唤起 Telegram App 跳转至对应消息进行下载。

## 🛠️ 技术栈

*   **Backend**: Python + Telethon (Telegram API)
*   **Automation**: GitHub Actions (Cron Job)
*   **Frontend**: Vanilla JS + GitHub Pages
*   **Database**: JSON (NoSQL, flat file)

## ⚠️ 免责声明

*   本项目的资源索引均来自于公开的 Telegram 频道，本项目不存储任何视频文件。
*   仅供学习和技术研究使用，请勿用于商业用途。
