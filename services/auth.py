from utils.jwt import create_token, TokenType


def validate_credentials(email: str, password: str) -> [bool, str]:
    if email == 'merajsiddiqui@outlook.com' and password == 'kota@9811':
        return True, create_token('abc', TokenType.ACCESS_TOKEN)
    else:
        return False, 'Credentials Invalid'
