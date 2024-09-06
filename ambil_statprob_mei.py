import requests
import time

url = "https://sipa.umrah.ac.id/backend/lirs/add_new" 
count = 0
headers = {
    "Cookie": "X_SESSION_MANAGER=GyJw6udNSNdWJ4DrodVzkqHnO5bBMufW9tgZxMpY; X-SESSION-ID=MNmwS7MfiYcgMbTsxSRLeT2nCS6is9G2uJleWGrp; X_SESSION_SIPA=eyJpdiI6IkY1SVZjc2pkZTdsWTdHRUU4VWQ0MHc9PSIsInZhbHVlIjoiRVgraWQwSkp6MUdLbzA5TmtUWlc4YmV6T09lTERyb1JVOGNKRHI2K1dYeWluT01ZYkdqSlh6ekpNR2c5VTJzRCIsIm1hYyI6ImQ2N2ExMjAzYmI2ODlkYzgxYTcyMmYzZDg1NDUxMjliOGJhODQ1ZjFiZTIzNjcwMTExZmEzZmU1NDJmMGU5MzciLCJ0YWciOiIifQ%3D%3D; X_REFRESH_SIPA=eyJpdiI6ImwrZDRWUTRIU2oyTWlZbXZzc0g0NEE9PSIsInZhbHVlIjoiYXdncnV4all2RGlEMUlqL1NMcmtDSXFOTmV2aFc3azl3eTZHSzlnVlJydHdVWmZ4c1pUZTc4ZGM5dVlNM3ZnSyIsIm1hYyI6IjNkMjNjZjg5NGEwOTljNGIxM2ZhYWQyNTY2YzYwNGFlYzkyYmU2OGE5Y2QzZDQwM2FjNTQxZDI1YzJiMGUzNmIiLCJ0YWciOiIifQ%3D%3D; X-LOCAL-DATA-SIPA=eyJpdiI6Im95b2IvTUZ0Q2lpQWh6NitLSVJkTkE9PSIsInZhbHVlIjoiTS9YSmFKNk44WmwrK1NGcFFRdkRJOW1odVpwbmxIM1Z0V0RsV1VlbXRPMmtPQnVBZzN5cFlEa2RpY0pnbnI1d1luUmFOV2FwOWcxWis4eitYREorMlprNS9zYWF5UE5mbUpNeDJIbzIrTGFlQWxQQnIvaThJcWFnOVI1REZ2YUFNWWx4TVhoZGZ3WERvUW9qUFk3NDc1QzBkSmpOTHQweWNlQ0NWd3ErbklVWFZkRXhMU3dGWDBjWGdVbnNMNWtWcGRFZDhBMnpFSXNNMkpkVk5VMEY3bFdUN3p5NmduVm5tejEwRjR0NFFBOWxpVXdUcEg3MFhXMVFBYWFrQjl4MCIsIm1hYyI6IjkzZDliZDQ4YTYyN2M5YjZkZGQ3YTQ2ZDZmMDM2YmJlYmMwZjI2ZDE0MDNjYjE1YTE3MjViZjMxYWNjYmI2ZjIiLCJ0YWciOiIifQ%3D%3D"
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