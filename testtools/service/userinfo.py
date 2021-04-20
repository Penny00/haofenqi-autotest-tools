from db import mysqldb
from utils import dict2obj


class User(object):
    def __init__(self, account):
        self.account = account
        ret = mysqldb.sqlhelper.fetch_all(
            "SELECT account.system_unique_id,audit.audit_id,account.uid FROM user_account "
            "account LEFT JOIN user_audit  audit "
            "ON account.uid = audit.uid WHERE account.account = %s "
            "ORDER BY audit.id DESC LIMIT 1", (self.account,))
        self.user_info = dict2obj(ret[0]) if ret else None


    def uid(self):
        return self.user_info.uid


    def user_key(self):
        return self.user_info.system_unique_id


    def audit_id(self):
        return self.user_info.audit_id
