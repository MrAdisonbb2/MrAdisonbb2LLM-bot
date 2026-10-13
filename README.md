# MrAdisonbb2LLM-bot

บอท Discord ที่คุยกับ AI (LLM) ได้ ใช้ [Groq](https://console.groq.com) เป็นเบื้องหลัง ใช้ฟรีได้

## บอททำอะไรได้

- `/ask คำถาม` ถามอะไรก็ได้ บอทตอบกลับในห้อง
- `@ชื่อบอท ข้อความ` แท็กบอทในห้องแชต บอทจะตอบกลับ
- ต้อนรับสมาชิกใหม่อัตโนมัติด้วยข้อความที่ AI แต่งให้

## สิ่งที่ต้องมี

- Python 3.10 ขึ้นไป
- บัญชี Discord และเซิร์ฟเวอร์ที่เรามีสิทธิ์ Manage Server
- บัญชี Groq (สมัครฟรี ไม่ต้องใช้บัตร)

## ขั้นที่ 1: สร้างบอทใน Discord

1. เข้า https://discord.com/developers/applications แล้วกด **New Application** ตั้งชื่อบอท
2. ไปที่เมนู **Bot**
   - กด **Reset Token** แล้ว **Copy** เก็บไว้ (นี่คือ `DISCORD_TOKEN`)
   - เลื่อนลงไปที่ **Privileged Gateway Intents** เปิด **Server Members Intent** และ **Message Content Intent**
   - กด **Save Changes**
3. ไปที่เมนู **OAuth2** > **OAuth2 URL Generator**
   - Scopes: ติ๊ก `bot` และ `applications.commands`
   - Bot Permissions: ติ๊ก **View Channels**, **Send Messages**, **Send Messages in Threads**, **Read Message History**
4. Copy ลิงก์ด้านล่างสุด เปิดในเบราว์เซอร์ เลือกเซิร์ฟเวอร์ แล้วกด **Authorize**

## ขั้นที่ 2: เอา API key ของ Groq

1. เข้า https://console.groq.com แล้วล็อกอิน
2. ไปที่ **API Keys** กด **Create API Key** แล้ว copy เก็บไว้ (นี่คือ `GROQ_API_KEY`)

## ขั้นที่ 3: ติดตั้ง

```bash
git clone https://github.com/MrAdisonbb2/MrAdisonbb2LLM-bot.git
cd MrAdisonbb2LLM-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

บน Windows ใช้ `venv\Scripts\activate` แทน `source venv/bin/activate`

## ขั้นที่ 4: ใส่ key

สร้างไฟล์ชื่อ `.env` ในโฟลเดอร์โปรเจกต์ แล้วใส่:

```
DISCORD_TOKEN=ใส่token
GROQ_API_KEY=ใส่key
GROQ_MODEL=openai/gpt-oss-20b
```

ดูชื่อโมเดลที่ใช้ได้ที่หน้า **Models** ใน console.groq.com

> ⚠️ ห้ามแชร์หรืออัปโหลดไฟล์ `.env` ขึ้น GitHub เด็ดขาด (ไฟล์นี้ถูกใส่ไว้ใน `.gitignore` แล้ว) ถ้า key หลุด ให้ reset ใหม่ทันที

## ขั้นที่ 5: รันบอท

```bash
python bot.py
```

ถ้าขึ้น `ออนไลน์แล้ว: ชื่อบอท` แปลว่าใช้ได้ ลองพิมพ์ `/ask` ใน Discord ได้เลย

- หยุดบอท: กด `Ctrl+C`
- บอททำงานเฉพาะตอนที่ terminal เปิดอยู่
- ข้อความต้อนรับจะส่งไปที่ห้องที่ตั้งไว้ใน Server Settings > Overview > **System Messages Channel**

## แก้ปัญหาที่เจอบ่อย

| อาการ | วิธีแก้ |
|---|---|
| `ModuleNotFoundError` | ยังไม่ได้เปิด venv ให้รัน `source venv/bin/activate` ก่อน |
| `KeyError: 'DISCORD_TOKEN'` | หาไฟล์ `.env` ไม่เจอ เช็กว่าชื่อไฟล์ถูกและอยู่โฟลเดอร์เดียวกับ `bot.py` |
| `Improper token has been passed` | token ผิด ให้ Reset Token แล้ว copy ใหม่ |
| `PrivilegedIntentsRequired` | ยังไม่ได้เปิด Intents ในขั้นที่ 1 ข้อ 2 |
| `model_not_found` (404) | ชื่อโมเดลใน `.env` ใช้ไม่ได้ ไปดูชื่อใหม่ที่หน้า Models ของ Groq |
| ไม่เห็นคำสั่ง `/ask` | กด `Ctrl+R` รีโหลด Discord |
| บอทขึ้น "is thinking..." ค้าง | ดู error ใน terminal ที่รันบอท |
