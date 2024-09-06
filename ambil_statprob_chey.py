import requests
import time

url = "https://sipa.umrah.ac.id/backend/lirs/add_new" 
count = 0
headers = {
    "Cookie": "X_SESSION_SIPA=eyJpdiI6IjRWWW5XdGl4WHNDenZNVm5JVW9kdEE9PSIsInZhbHVlIjoiU0Z3aUFkQTErYnVPYVhrUXU5RzBEby9XY3FqZUI3cXJDQjRHYzVhTm1zOGlCcGk1SGhzOG16OHRsOFhQYlVTZSIsIm1hYyI6IjMzZGVlYTk5OWU4OTNjMzM5YTI2MmEzN2JjYjhiMzc1NDllYjM1MTIyOWU3YzAyN2I3NzY3MGEwYmY5NmY4ZmYiLCJ0YWciOiIifQ%3D%3D; X_REFRESH_SIPA=eyJpdiI6ImJXU2VPYlBvNmJnU1ppUG94NVBxeFE9PSIsInZhbHVlIjoiT3AvSzVpL1JmNTFJaFlwaXphdEl1TnY0ek16c2ZmdEtMek9zSTJhSWRqa2lCNWNGb1A4TktjUURWZmlMSnc4eSIsIm1hYyI6ImNiYzUyMjQwNzM2NDk0OTZkMWNkMDE3ZjIwNjExMDg5M2I4MzhmMzZlOWRmMDE2Yzc5ZmRhNjI5ZGExYzg4MjAiLCJ0YWciOiIifQ%3D%3D; X-LOCAL-DATA-SIPA=eyJpdiI6Ind2VW0wZG0yREFtcjRaY21nVm83UWc9PSIsInZhbHVlIjoiZzBzT2ZFaDY5bzZ4NVhSV0pkOVd0ZlNvWmIxRmp1TzZZSzR3STdadnRoZnhQUWJZbGs4K2sraHlHbEVFamc2MkF4dDdYdmJYQ3NGK01HT0pZTUdFYTFXRnBtWDRINTM2clBLOUtvbFlnNWx2QW5EajRMWERuNEg4SnFkQ0ZVR3NXWDVlQTNqOURkejZCVGIwQ2hvN1lHYXVmUSs3TzZ6Y0xEdUF3cGk4OGJ6d3V0MExUWjBVazllMDhHMG9TNEwzdGo5dzRSVGVvdFBCSXJkRmROY054N1RuWjdiUmZDWnFKbERoTHVOb1p3TjY2MkxlR3lRY3J2SXhweG0xTDdaciIsIm1hYyI6IjYzZDY0NWU3YjdmZmJkN2QxZjM4YjE2MTg0OTlkYTdmNWNmMjQzNDJkYTM3MDk3OTY3MmM3ODdhNDcxOGIzNDQiLCJ0YWciOiIifQ%3D%3D; X-SESSION-ID=Yky7sIhnrzJ4OIpsmuAX9D3nxapTejc0JuEy9IBt"
}

while True:
    try:
        count += 1
        response = requests.post(url,data={"id_kurikulum_matkul": 48534, "id_jadwal": 52277}
        ,headers=headers)

        print(f"{count} ) Status Code: {response.status_code}")
        print("Response Text:", response.text)
        time.sleep(1)
    except Exception:
        pass