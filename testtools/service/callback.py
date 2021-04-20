import os

from db import mysqldb
import requests
from config import CommonConfig
from dao.userdao import User


class VerifyCallback(object):

    def __init__(self, account):
        self.account = account

    def lend_verify_callback(self, result, env='c'):
        loan_result = mysqldb.sqlhelper.fetch_all("SELECT loan.system_unique_id,loan.audit_id,loan.loan_"
                                                  "id FROM user_account account LEFT JOIN template_log  loan "
                                                  "ON account.uid = loan.uid WHERE account.account = %s AND "
                                                  "loan.status=4 "
                                                  "ORDER BY loan.id DESC LIMIT 1", (self.account,))
        if loan_result:
            loan_id = loan_result[0].get("loan_id")
            system_unique_id = loan_result[0].get("system_unique_id")
            audit_id = loan_result[0].get("audit_id")
            print(loan_id, system_unique_id, audit_id)

            headers = {
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
            }

            data = 'icode=0100010005&salt=&data={"type":"async","retCode":"00S0000",' \
                   '"requestId":"20190523194931_2805139678658519426","agencyRequestId":' \
                   '"88b4b14ef0bf31baa39c1e8d6eec377c","message":{"eventCode":"haoHuanLendAudit",' \
                   '"loan":"%s","appVersion":"500","applicationNo":"APPL_HAOHUAN202008181122306c6bdA",' \
                   '"verifyResult":"%s","loanKey":"hh_20190523194931_2805139678658519426",' \
                   '"sessionId":"20190523194931_2805139678658519426","loanId":"%s",' \
                   '"userKey":"%s"}}&sign=&key=&' % (loan_id, result, audit_id, system_unique_id)
            # print(data)
            host = CommonConfig.loancenter_env.get(env, 'http://hfq-gateway.test.rrdbg.com')
            resp = requests.post(url=host + '/loancenter/audit/risk-analyse-notice',
                                 data=data,
                                 headers=headers)
            # print(resp.text)
            return resp.text

    def auth_verify_callback(self, result):
        user = User(self.account)
        user_key = user.user_key
        audit_id = user.audit_id
        # result = 'ACCEPT' if result else 'REJECT'
        os.system(
            r'jmeter  -n -t /usr/python-script/jmeter-script/audit-notice.jmx -DuserKey={} -DloanId={} -Dresult={}'.format(
                user_key, audit_id, result))