from pyrogram import filters
from config import CONTROL_GROUP_ID
from relay.vc_bridge import VCBridge
from relay import state

bridge = None

def register(app):
    global bridge
    bridge = VCBridge(app)

    @app.on_message(filters.command("connect") & filters.chat(CONTROL_GROUP_ID))
    async def connect(_, m):
        if len(m.command) < 2:
            return await m.reply("Usage: /connect <target_group_id>")
        target = int(m.command[1])
        await bridge.start(m.chat.id, target)
        await m.reply(f"🔗 Connected → `{target}`")

    @app.on_message(filters.command("volume") & filters.chat(CONTROL_GROUP_ID))
    async def volume(_, m):
        if len(m.command) < 2:
            return
        percent = int(m.command[1])
        state.volume = max(0.1, min(3.0, percent / 100))
        await m.reply(f"🔊 Volume = {int(state.volume*100)}%")

    @app.on_message(filters.command("stop") & filters.chat(CONTROL_GROUP_ID))
    async def stop(_, m):
        await bridge.stop()
        await m.reply("⛔ Relay stopped")
