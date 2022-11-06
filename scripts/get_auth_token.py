import random
import hashlib
import base64
import requests
import socket

dirigera_ip = '127.0.0.1'


def generateCodeChallenge():
    codeAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
    codeLength = 128

    code = ''.join(random.choice(codeAlphabet) for _ in range(codeLength))
    hash = base64.urlsafe_b64encode(hashlib.sha256(
        code.encode()).digest()).rstrip(b'=').decode('us-ascii')

    print(f'CODE: {code}\nHASH: {hash}')

    return {'code': code, 'hash': hash}


def getOauthCode(hash: str):
    response = requests.get(
        f'https://{dirigera_ip}:8443/v1/oauth/authorize',
        params={
            "audience": "homesmart.local",
            "response_type": "code",
            "code_challenge": hash,
            "code_challenge_method": "S256"
        },
        verify=False
    ).json()
    code = response['code']

    print(f'oauth code: {code}')

    return code


def getOauthToken(code: str, challenge: str):
    response = requests.post(
        f'https://{dirigera_ip}:8443/v1/oauth/token',
        data=f"code={code}&name={socket.gethostname()}&grant_type=authorization_code&code_verifier={challenge}",
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        verify=False
    ).json()

    print(response)

    token = response['access_token']
    print(f'oauth token: {token}')
    return token


codeChallenge = generateCodeChallenge()
code = getOauthCode(codeChallenge['hash'])

input('Press the action button on the dirigera and then press enter')

token = getOauthToken(code, codeChallenge['code'])
