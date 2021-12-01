def validate_url(url):
    if url:
        if url.startswith("https://"):
            try:
                owner = url.split('/')[3]
                repo_name = url.split('/')[4]
                return owner, repo_name
            except IndexError:
                print("INDEX ERROR")
                return None, None
        else:
            try:
                owner = url.split('/')[1]
                repo_name = url.split('/')[2]
                return owner, repo_name
            except IndexError:
                print("INDEX ERROR")
                return None, None

