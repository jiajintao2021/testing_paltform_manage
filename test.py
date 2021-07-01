"""
@TIME: 2021/6/16 11:26
@AUTHOR: JiaJinTao
"""

from ldap3 import Server, Connection, ALL, SUBTREE, ServerPool
'192.168.200.100:389'

url = '192.168.100.200:389'
username = 'jiajintao@enovatemotors.com'
password = '1qaz2WSX'
'jiajintao@enovatemotors.com 1qaz2WSX'

target_username = 'lingchen'


def login():
    server = Server(url)
    conn = Connection(
        server, user=username, password=password
    )
    conn.bind()
    print(conn)
    # res = conn.search(
    #     search_base='DC=dearcc,DC=cn',
    #     search_filter=f'(sAMAccountName=jiajintao)',
    #     attributes=['cn', 'givenName', 'mail', 'sAMAccountName'],
    # )
    print(conn.result)
    print(conn.response)
    response = conn



if __name__ == '__main__':
    login()