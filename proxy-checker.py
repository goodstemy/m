"""Find 10 working proxies supporting CONNECT method
   to 25 port (SMTP) and save them to a file."""

import asyncio
from proxybroker import Broker

countries = ['US', 'GB', 'CA', 'AU', 'NZ']


async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'w') as f:
        while True:
            proxy = await proxies.get()
            print(proxy)
            if proxy is None:
                break
            print(proxy, 'are checked')
            f.write('%s:%d\n' % (proxy.host, proxy.port))


def main():
    proxies = asyncio.Queue()
    broker = Broker(proxies, judges=['smtp://smtp.gmail.com'], max_tries=1)

    # Check proxy in spam databases (DNSBL). By default is disabled.
    # more databases: http://www.dnsbl.info/dnsbl-database-check.php
    dnsbl = ['bl.spamcop.net', 'cbl.abuseat.org', 'dnsbl.sorbs.net',
             'zen.spamhaus.org', 'bl.mcafee.com', 'spam.spamrats.com']

    tasks = asyncio.gather(
        broker.find(types=['SOCKS5', 'CONNECT:25'], dnsbl=dnsbl, limit=10, countries=countries),
        save(proxies, filename='checked-proxy.txt'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

if __name__ == '__main__':
    main()