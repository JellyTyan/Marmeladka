from database.database_manager import DatabaseManager

class UserProfileFunc():
    def __init__(self):
        self.db_manager = DatabaseManager()

    async def get_bump_count(self, id: int):
        bump_count = await self.db_manager.fetchone("select bump_count FROM user_data WHERE id = ?", (id,))

        if bump_count is None:
            return "0"
        else:
            return str(bump_count[0])

    async def get_voice_count(self, id: int):
        voice_time = await self.db_manager.fetchone("select voice_time FROM user_data WHERE id = ?", (id,))

        if voice_time is None:
            return "0"
        else:
            voice_time = voice_time[0]
            days = voice_time // 86400
            hours = (voice_time % 86400) // 3600
            minutes = (voice_time % 3600) // 60
            seconds = voice_time % 60
            return f"{days}d {hours:02d}:{minutes:02d}:{seconds:02d}"

    async def get_message_count(self, id: int):
        message_count = await self.db_manager.fetchone("select message_count FROM user_data WHERE id = ?", (id,))

        if message_count is None:
            return "0"
        else:
            return str(message_count[0])

    async def get_invite_count(self, id: int):
        invite_count = await self.db_manager.fetchone("SELECT invite_count FROM user_data WHERE id = ?", (id,))

        if invite_count is None:
            return "0"
        else:
            return str(invite_count[0])

    async def get_biograpgy(self, id: int):
        biography = await self.db_manager.fetchone("SELECT biography FROM user_bio WHERE id = ?", (id,))

        if biography is None:
            return "Биография не задана"
        else:
            return biography[0]

    async def get_tag(self, id: int):
        tag = await self.db_manager.fetchone("SELECT tag FROM user_bio WHERE id = ?", (id,))

        if tag is None:
            return "Тег не задан"
        else:
            return tag[0]
