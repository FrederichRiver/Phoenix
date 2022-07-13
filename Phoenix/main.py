from .server_model import Server
from .server_utils import Server_setting


s = Server(**Server_setting)
s.run()