import json
import os
import asyncio
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import DocumentAttributeFilename

# === 保持原有配置 ===
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["TELEGRAM_SESSION"]
CHANNEL_USERNAME = 'AnimeNep' # 替换目标
DATA_FILE = 'data.json'

async def main():
    # 1. 读取旧数据
    data = []
    min_id = 0
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = json.load(f)
            data = content.get('videos', [])
            if data:
                min_id = data[0]['id'] # 新数据在最前面，所以第一个就是最大的ID

    print(f"当前已有视频数: {len(data)}，从 ID {min_id} 开始增量抓取...")

    # 2. 抓取新数据
    print("正在初始化 Telegram Client...")
    
    # 显式禁用 IPv6，通常能解决 GitHub Actions 卡住的问题
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")
    
    # 手动控制连接，增加调试信息
    try:
        await client.connect()
    except OSError:
        print("连接失败，尝试重新连接...")
        await client.connect()
        
    if not await client.is_user_authorized():
        print("❌ 错误：Session String 已失效或未授权。脚本将挂起等待输入，正在终止...")
        return

    print("✅ 连接成功！开始获取频道实体...")

    async with client:
        # 注意：get_entity 有时也会卡，加个 try
        try:
            entity = await client.get_entity(CHANNEL_USERNAME)
            print(f"已找到频道: {entity.title} (ID: {entity.id})")
        except ValueError:
            print(f"❌ 找不到频道: {CHANNEL_USERNAME}，请检查用户名是否正确或频道是否被封禁。")
            return

        new_videos = []
        print(f"开始遍历消息 (从 ID {min_id} 开始)...")
        
        count = 0 # 用于打印进度的计数器

        async for message in client.iter_messages(entity, min_id=min_id, limit=None):
            # 打印心跳日志，防止 GitHub Actions 以为程序死掉
            count += 1
            if count % 1000 == 0:
                print(f"已扫描 {count} 条消息...", flush=True)

            # === 修改核心判断逻辑 ===
            # 只有当消息包含 document（泛指所有非图片的附件，如视频、文件）时才处理
            # 这样就自动排除了纯文本消息和纯图片消息
            if message.document: 
                file_name = None
                is_video = False
                
                # 安全地获取 attributes
                # 有些 document 可能没有 attributes 属性，虽然少见，但加个 getattr 更稳妥
                attributes = getattr(message.document, 'attributes', []) or []

                for attr in attributes:
                    if isinstance(attr, DocumentAttributeFilename):
                        file_name = attr.file_name
                
                # 检查 MIME 类型
                # message.file.mime_type 是安全的，因为 message.document 存在则 message.file 一定存在
                mime_type = getattr(message.file, 'mime_type', '') or ''
                
                if mime_type.startswith('video/') or (file_name and file_name.endswith(('.mkv', '.mp4', '.avi', '.mov'))):
                    is_video = True

                if is_video and file_name:
                    new_videos.append({
                        'id': message.id,
                        'name': file_name,
                        'link': f"https://t.me/{CHANNEL_USERNAME}/{message.id}",
                        'date': message.date.strftime('%Y-%m-%d'),
                        'size': round(message.file.size / (1024 * 1024), 2)
                    })
        
        print(f"新增 {len(new_videos)} 条视频。")
        full_data = new_videos + data

        # 3. 保存数据 (只保存 JSON)
        # 记录 timestamp 用于前端判断版本
        output = {
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'total': len(full_data),
            'videos': full_data
        }
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, separators=(',', ':')) # 使用 compact 格式减少体积

    print("数据更新完成。")

if __name__ == '__main__':
    asyncio.run(main())
