from conn import AppConnection


async def select_into_apschedule():
    conn = AppConnection().mysql
    query_sql = "select * from apschedule_check " \
                "where checked = 0"
    return await conn.query_without_arg(query_sql)


async def select_into_info_account(phone_number):
    conn = AppConnection().mysql
    query_sql = "select * from account_info_bnpl as a join account_bnpl ab on ab.id = a.user_id where phone_number = %s"
    res = await conn.query(query_sql, phone_number)
    if len(res) != 0:
        return res[0]
    else:
        return []


async def get_uuid_info_account(phone_number):
    conn = AppConnection().mysql
    query_sql = "select * from apschedule_check" \
                "where phone_number = %s"
    res = await conn.query(query_sql, phone_number)
    if len(res) != 0:
        return res
    else:
        return []


async def select_text_send(case: str):
    conn = AppConnection().mysql
    query_sql = "select * from notification_case " \
                "where name = %s"
    return await conn.query(query_sql, case)


async def insert_into_apschedule(uuid, phone_number):
    conn = AppConnection().mysql
    query_sql = "insert into `apscheduler_check` (uuid,phone_number) " \
                "values (%s,%s)" \
                "ON DUPLICATE KEY UPDATE uuid =%s, phone_number = %s"
    return await conn.insert(query_sql, [uuid, phone_number, uuid, phone_number])


async def reset_counter_otp(phone_number):
    conn = AppConnection().mysql
    query_sql = "UPDATE `account_phone_otp` SET counter_call=0 " \
                "WHERE phone_number=%s;"
    return await conn.query(query_sql, phone_number)


async def update_into_apschedule(uid):
    conn = AppConnection().mysql
    query_sql = "update apschedule_check" \
                "set values (%s) where uid = %s"
    await conn.query(query_sql, [1, uid])
