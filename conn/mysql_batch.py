import urllib

import aiomysql


class AIOMysqlWrapper:
    def __init__(self, pool):
        self.pool = pool

    async def query(self, sql, args):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, args)
                await conn.commit()
                return list(await cur.fetchall())

    async def query_without_arg(self, sql):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                await conn.commit()
                return list(await cur.fetchall())

    @staticmethod
    async def create_from_uri(uri: str):
        mysql_cf = urllib.parse.urlparse(uri)
        pool = await aiomysql.create_pool(host=mysql_cf.hostname, user=mysql_cf.username,
                                          password=mysql_cf.password, db=mysql_cf.path.lstrip('/'),
                                          cursorclass=aiomysql.cursors.DictCursor,
                                          charset='utf8')

        return AIOMysqlWrapper(pool)
