from socketio import AsyncServer
from sqlmodel import select
from datetime import datetime

from app.models.message import ConnectedUser, Message
from app.models.user import User
from app.database import get_session
from app.utils.token import decode_access_token , get_current_user


def register_socketio_events(sio: AsyncServer):
    @sio.event
    async def connect(sid, environ):
        print(f"✅ Client connected: {sid}")
        headers = environ.get("asgi.scope", {}).get("headers", [])

        # Extract Authorization token from headers
        token = None
        for name, value in headers:
            if name == b'authorization':
                token = value.decode().replace("Bearer ", "").strip()

        if not token:
            print(f"❌ No token provided by {sid}")
            await sio.disconnect(sid)
            return

        user_data = decode_access_token(token)
        if not user_data:
            print(f"❌ Invalid token from {sid}")
            await sio.disconnect(sid)
            return

        user_id = user_data["user_id"]

        async for session in get_session():
            connected = ConnectedUser(user_id=user_id, sid=sid, connected_at=datetime.utcnow())
            session.add(connected)
            await session.commit()

    @sio.event
    async def join(sid, data):
        room = data.get("room")
        if not room:
            await sio.emit("error", {"message": "Missing room"}, to=sid)
            return

        await sio.enter_room(sid, room)
        await sio.emit("message", f"{sid} joined room {room}", room=room)
        print(f"📥 {sid} joined {room}")

    @sio.event
    async def message(sid, data):
        room = data.get("room")
        content = data.get("message")

        if not room or not content:
            await sio.emit("error", {"message": "Missing room or message"}, to=sid)
            return

        async with get_session() as session:
            # Get user ID from sid
            result = await session.exec(select(ConnectedUser).where(ConnectedUser.sid == sid))
            connected_user = result.first()
            if not connected_user:
                await sio.emit("error", {"message": "Unauthorized"}, to=sid)
                return

            # Save message to DB
            msg = Message(
                sender_id=connected_user.user_id,
                group_id=int(room),
                content=content,
                sent_at=datetime.utcnow()
            )
            session.add(msg)
            await session.commit()

        await sio.emit("message", {
            "room": room,
            "from": connected_user.user_id,
            "content": content,
            "sent_at": msg.sent_at.isoformat()
        }, room=room)
        print(f"💬 [{room}] {connected_user.user_id}: {content}")

    @sio.event
    async def private_message(sid, data):
        receiver_id = data.get("receiver_id")
        content = data.get("message")

        if not receiver_id or not content:
            await sio.emit("error", {"message": "Missing receiver_id or message"}, to=sid)
            return

        async with get_session() as session:
            # Get sender
            sender_result = await session.exec(select(ConnectedUser).where(ConnectedUser.sid == sid))
            sender_conn = sender_result.first()
            if not sender_conn:
                await sio.emit("error", {"message": "Unauthorized"}, to=sid)
                return

            # Get receiver sid
            receiver_result = await session.exec(select(ConnectedUser).where(ConnectedUser.user_id == receiver_id))
            receiver_conn = receiver_result.first()

            # Save to DB
            msg = Message(
                sender_id=sender_conn.user_id,
                receiver_id=receiver_id,
                content=content,
                sent_at=datetime.utcnow()
            )
            session.add(msg)
            await session.commit()

            # Deliver message if receiver is connected
            if receiver_conn:
                await sio.emit("private_message", {
                    "from": sender_conn.user_id,
                    "content": content,
                    "sent_at": msg.sent_at.isoformat()
                }, to=receiver_conn.sid)

            await sio.emit("private_message_sent", {
                "to": receiver_id,
                "content": content,
                "sent_at": msg.sent_at.isoformat()
            }, to=sid)

    @sio.event
    async def disconnect(sid):
        print(f"🔌 Client disconnected: {sid}")
        async with get_session() as session:
            result = await session.exec(select(ConnectedUser).where(ConnectedUser.sid == sid))
            user_conn = result.first()
            if user_conn:
                await session.delete(user_conn)
                await session.commit()
                print(f"❎ Removed sid {sid} from ConnectedUser")
