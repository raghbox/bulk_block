import requests
import subprocess

def download_bulk_deals(from_date, to_date):

    session = requests.Session()


    url = f'https://www.nseindia.com/api/historical/block-deals?from={from_date}&to={to_date}'


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://www.nseindia.com/report-detail/display-bulk-and-block-deals',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
        'Priority': 'u=4',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }


    session.get('https://www.nseindia.com', headers=headers)


    url = f"{url}&csv=true"
    print(f"Requesting URL: {url}")

    output_filename = f"/home/micro2/Desktop/nsefile/nseblock/nseblock_{from_date}_{to_date}_nsebulk.csv"
    

    response = session.get(url, headers=headers)


    if response.status_code == 200:

        subprocess.run([
            'wget',
            '--user-agent=Mozilla/5.0',   
            '--output-document=' + output_filename,  
            url
        ])
        print(f"File saved as {output_filename}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

# Example usage
#download_bulk_deals('01-01-2018', '31-12-2018')

for i in range(2004, 2025):
    download_bulk_deals(f"01-01-{str(i)}", f"31-12-{str(i)}")
    print(i)

