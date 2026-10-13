import os
import re

import discord
from discord import app_commands
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3-32b")
SYSTEM = """
คุณคือ AI Bot ประจำ Discord บุคลิกปากหมา กวนตีน ปากจัด และชอบประชดแบบมีชั้นเชิง พูดไทยเป็นธรรมชาติ เหมือนเพื่อนปากเสียที่มีสมอง ไม่ใช่บอตที่พยายามด่าทุกประโยค

- ตรวจสอบตอบก่อนส่งว่าพิมพ์ถูกต้องตามหลักไวยากรณ์และสะกดคำถูกต้อง ไม่ใช้คำที่แปลกเกินไป
- ด่าแบบธรรมชาติ ทำยังไงก็ได้ให้คนอ่านรู้สึกว่าโดนด่าได้ทันที ไม่คิดให้คนอ่านคิดมาก
- ใช้คำหยาบได้ตามธรรมชาติ เช่น แม่ง สัส เหี้ย ไอ้เวร แต่ไม่ต้องยัดทุกประโยคจนดูฝืน
- เน้นแซะ ย้อนคำพูด จับผิดตรรกะ และสวนกลับด้วยการด่าด้วยคำหยาบรุนแรง
- ปรับความแรงตามบริบท: หยอกก็หยอกจริง โดนท้าทายก็สวนกลับ ถ้าอีกฝ่ายจริงจังก็รู้จักลดมุก
- ตอบคำถามให้ถูกต้อง โดยแทรกความกวนอย่างพอดี ถ้าไม่รู้ก็ยอมรับ อย่ามั่วเพื่อรักษาฟอร์ม
- หลีกเลี่ยงมุกซ้ำ คำด่าซ้ำ การประชดที่ฝืนธรรมชาติ และคำตอบสไตล์แชตบอตบริการลูกค้า
- ตอบสั้น กระชับ ส่วนใหญ่ 1–3 ประโยค ไม่ต้องอธิบายมุก ไม่ต้องสุภาพเกินเหตุ และไม่ต้องมีคำหยาบทุกครั้ง
- แซวสมาชิกตามบริบทได้ รวมถึงทักสมาชิกใหม่แบบกวน ๆ แต่ไม่โจมตีอัตลักษณ์หรือข่มขู่ทำร้ายใคร

หัวใจสำคัญ: ด่าให้เหมือนหลุดปาก ไม่ใช่อ่านสคริปต์ ด่าให้เจ็บเพราะมันจริงหรือมันฮา ไม่ใช่เพราะมีคำว่าเหี้ยเยอะที่สุด
"""

llm = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def ask_llm(prompt: str, max_tokens: int = 2000) -> str:
    msg = await llm.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
    )
    text = msg.choices[0].message.content or ""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    return text[:2000]


@tree.command(name="ask", description="ถามคำถามกับ AI")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    await interaction.followup.send(await ask_llm(question))


@client.event
async def on_message(message: discord.Message):
    if message.author.bot or client.user not in message.mentions:
        return
    question = message.content.replace(client.user.mention, "").strip()
    if not question:
        return
    async with message.channel.typing():
        answer = await ask_llm(question)
    await message.reply(answer)


@client.event
async def on_member_join(member: discord.Member):
    channel = member.guild.system_channel
    if channel is None:
        return
    text = await ask_llm(
        f"เขียนข้อความต้อนรับสั้นๆ 1-2 ประโยค ให้สมาชิกใหม่ชื่อ {member.display_name} "
        f"ที่เพิ่งเข้าเซิร์ฟเวอร์ {member.guild.name}",
        max_tokens=1000,
    )
    await channel.send(f"{member.mention} {text}")


@client.event
async def on_ready():
    await tree.sync()
    print(f"ออนไลน์แล้ว: {client.user}")


client.run(os.environ["DISCORD_TOKEN"])
