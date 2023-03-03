import aiohttp
from core.config import settings


class AuthUsers():
    """Read user information from auth."""

    def __init__(self):
        pass

    async def read_info_users(self, users_ids: list) -> dict | None:
        """Reading and organizing user data."""
        auth_users = await self._read_auth_users()
        info_users = {}
        for auth_user in auth_users:
            user_id = auth_user['id']
            if user_id in users_ids:
                info = {
                    'user_email': auth_user['email'],
                    'user_name': auth_user['full_name'], 
                }
                info_users[user_id] = info
        return info_users        

    async def _read_auth_users(self) -> list:
        async with aiohttp.ClientSession() as session:
            payload = {                
                'email': settings.auth_login_email,
                'password': settings.auth_login_password
            }
            async with session.post(settings.auth_login_url, json=payload) as response:
                tokens = await response.json()
            access_token = tokens['access_token']
            headers = {'Authorization': f'Bearer {access_token}'}
            async with session.get(settings.auth_users_url, headers=headers) as response:
                data_users = await response.json()
            return data_users 
    

def get_auth_users_service() -> AuthUsers:
    """interface and movie service connectivity."""
    return AuthUsers()
