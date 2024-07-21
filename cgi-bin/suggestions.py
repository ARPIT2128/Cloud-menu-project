#!/usr/bin/env python3

import cgi
import cgitb
import json
import requests

# Enable traceback for debugging CGI scripts
cgitb.enable()

def fetch_suggestions(query):
    suggestions = []
    try:
        url = 'https://suggestqueries.google.com/complete/search'
        params = {
            'client': 'firefox',
            'q': query
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:
                suggestions = data[1]  

    except Exception as e:
        print(f"Error fetching suggestions: {e}")

    return suggestions

def main():
    print("Content-Type: application/json\n")

    form = cgi.FieldStorage()
    query = form.getvalue('query', '')

    suggestions = fetch_suggestions(query)

    print(json.dumps(suggestions))

if __name__ == '__main__':
    main()
