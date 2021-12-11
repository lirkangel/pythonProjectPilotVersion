import asyncio

from logzero import logger as log

from config.cf import CONFIG
from conn.mysql_batch import AIOMysqlWrapper
from utils.funcs import singleton, safe_capture_error


@singleton
class AppConnection:
    mysql: AIOMysqlWrapper = None
    event_loop = None

    async def init_connections(self):
        try:
            self.mysql = await AIOMysqlWrapper.create_from_uri(CONFIG.MYSQL_URL)
            AppConnection.event_loop = asyncio.get_running_loop()

        except Exception as e:
            log.error(e)
            safe_capture_error(e)
            raise e
