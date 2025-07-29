import requests
import json
import psutil

url = "https://api.eu-w1.tago.io/data"
headers = {
    "Content-Type": "application/json",
    "Authorization": "9d4dec69-7b72-4051-a643-ba05526a8296"
}

# Measurement Functions
def measure_cpu_usage():
    return psutil.cpu_percent(interval=1)


def measure_ram_usage():
    return psutil.virtual_memory().percent


def measure_network_sent():
    return psutil.net_io_counters().bytes_sent


def measure_network_recv():
    return psutil.net_io_counters().bytes_recv

def measure_disk_usage():
    return psutil.disk_usage('/').percent


# An example code block (you can change this)
def sample_code():
    result = 0
    for i in range(10 ** 5):
        result += i
    return result


# Before measurements
cpu_before = measure_cpu_usage()
ram_before = measure_ram_usage()
net_sent_before = measure_network_sent()
net_recv_before = measure_network_recv()
disk_before = measure_disk_usage()

result = sample_code()

# After measurements
cpu_after = measure_cpu_usage()
ram_after = measure_ram_usage()
net_sent_after = measure_network_sent()
net_recv_after = measure_network_recv()
disk_after = measure_disk_usage()

# Data Preparation
data = [
    {"variable": "cpu_before", "value": cpu_before},
    {"variable": "ram_before", "value": ram_before},
    {"variable": "network_sent_before", "value": net_sent_before},
    {"variable": "network_recv_before", "value": net_recv_before},
    {"variable": "disk_before", "value": disk_before},

    {"variable": "cpu_after", "value": cpu_after},
    {"variable": "ram_after", "value": ram_after},
    {"variable": "network_sent_after", "value": net_sent_after},
    {"variable": "network_recv_after", "value": net_recv_after},
    {"variable": "disk_after", "value": disk_after},

    {"variable": "code_result", "value": str(result)[:50]}
]

# Send to API
response = requests.post(url, headers=headers, json=data)

print(f"HTTP Status Code: {response.status_code}")
print(f"Response Content: {response.text}")

if response.status_code in [200, 202]:
    try:
        response_data = response.json()
        print(f"Response JSON: {json.dumps(response_data, indent=4)}")
        if response_data.get("status") == True:
            print("Data was sent successfully!")
        else:
            print(f"API response failed: {response_data.get('message')}")
    except json.JSONDecodeError:
        print(f"Error: Response is not in JSON format. Response: {response.text}")
else:
    print(f"Data could not be sent: {response.status_code}, {response.text}")