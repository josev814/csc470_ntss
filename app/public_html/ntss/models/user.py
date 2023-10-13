from ntss.models.database import MysqlDatabase

class Users(MysqlDatabase):
    MysqlDatabase.table = 'users'

    def get_permissions(self, user_id):
        MysqlDatabase.table = 'user_permissions'
        pass

    def get_user(self, user_email:str, user_password: None) -> dict:
        query_filter = [
                {'column':'email', 'operator':'=', 'value': user_email}
            ]
        self.select(
            '*',
            query_filter
        )
    
    def add_user(self, user_email:str, user_password: str) -> int:
        """
        Adds a user and returns their user_id from the database
        """
        self.create(
            {
                'user_email': user_email,
                'password': self._set_encrypted_password(user_password)
            }
        )
    
    def _set_encrypted_password(self, password):
        """
        Encrypts the password for a user
        """
        import hashlib
        from random import random
        salt = hashlib.sha256(str(random()), str(random()))[:5]
        hash = hashlib.sha256(f'{salt}{password}').hexdigest()
        encrypted = hashlib.sha256(f'{salt}||{hash}')
        return encrypted

    def _check_password(self, password, encrypted_password) -> bool:
        """
        Checks if the password submitted is the same as the password that was stored
        """
        import hashlib
        salt, hash = encrypted_password.split('||')
        return hash == hashlib.sha256(salt, password)
    