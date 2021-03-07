
import keyring
from keyrings.alt.file import PlaintextKeyring
keyring.set_keyring(PlaintextKeyring())
keyring.set_keyring(PlaintextKeyring())
keyring.set_password('CryptoUsersService', 'LOCAL_MONGO_USERNAME', 'cryptoAdmin')
keyring.set_password('CryptoUsersService', 'cryptoAdmin', 'DaPStREA2!')
keyring.set_password('CryptoUsersService', 'CENTRAL_MONGO_USERNAME', 'admin')
keyring.set_password('CryptoUsersService', 'admin', 'admin')

