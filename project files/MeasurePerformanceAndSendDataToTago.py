import requests
import json
import psutil
import time

url = "https://api.eu-w1.tago.io/data"
headers = {
    "Content-Type": "application/json",
    "Authorization": "dee65a7f-c0d1-4198-b9c6-48383201bbe9"
}


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


# ---------- Bad Codes ----------
def inefficient_sum():
    result = 0
    for i in range(10**5):
        result += i
    return result


def redundant_loop():
    result = []
    for i in range(100):
        for j in range(100):
            result.append(i*j)
    return result


def bad_sorting():
    big_list = list(range(10**4, 0, -1))
    for i in range(len(big_list)):
        for j in range(i+1, len(big_list)):
            if big_list[i] > big_list[j]:
                big_list[i], big_list[j] = big_list[j], big_list[i]
    return big_list


def useless_computation():
    x = 1
    for i in range(1, 1000):
        for j in range(1, 10):
            x = (x * i * j) // (i + 1)
    return x


def bad_prime_numbers():
    primes = []
    for num in range(2, 1000):
        for i in range(2, num):
            if num % i == 0:
                break
        else:
            primes.append(num)
    return primes


def bad_fibonacci():
    def fib(n):
        if n <= 1:
            return n
        else:
            return fib(n-1) + fib(n-2)
    return fib(20)


def bad_factorial():
    def factorial(n):
        if n == 0:
            return 1
        else:
            return n * factorial(n-1)
    return factorial(15)


# ---------- Good Codes ----------

def efficient_sum():
    return sum(range(10**5))


def optimized_loop():
    result = [i*j for i in range(100) for j in range(100)]
    return result


def builtin_sorting():
    big_list = list(range(10**4, 0, -1))
    big_list.sort()
    return big_list


def efficient_computation():
    x = 1
    for i in range(1, 1000):
        x *= i
    return x


def good_prime_numbers():
    primes = []
    for num in range(2, 1000):
        if all(num % i != 0 for i in range(2, int(num**0.5)+1)):
            primes.append(num)
    return primes


def good_fibonacci():
    a, b = 0, 1
    for _ in range(20):
        a, b = b, a + b
    return a


def good_factorial():
    result = 1
    for i in range(1, 16):
        result *= i
    return result


data = []

bad_functions = [
    inefficient_sum,
    redundant_loop,
    bad_sorting,
    useless_computation,
    bad_prime_numbers,
    bad_fibonacci,
    bad_factorial
]

good_functions = [
    efficient_sum,
    optimized_loop,
    builtin_sorting,
    efficient_computation,
    good_prime_numbers,
    good_fibonacci,
    good_factorial
]

# Running the Bad Codes
for i, func in enumerate(bad_functions):
    cpu_before = measure_cpu_usage()
    ram_before = measure_ram_usage()
    net_sent_before = measure_network_sent()
    net_recv_before = measure_network_recv()
    disk_before = measure_disk_usage()

    result = func()

    cpu_after = measure_cpu_usage()
    ram_after = measure_ram_usage()
    net_sent_after = measure_network_sent()
    net_recv_after = measure_network_recv()
    disk_after = measure_disk_usage()

    data.extend([
        {"variable": f"cpu_before_bad_code_{i+1}", "value": cpu_before},
        {"variable": f"ram_before_bad_code_{i+1}", "value": ram_before},
        {"variable": f"network_sent_before_bad_code_{i+1}", "value": net_sent_before},
        {"variable": f"network_recv_before_bad_code_{i+1}", "value": net_recv_before},
        {"variable": f"disk_before_bad_code_{i+1}", "value": disk_before},

        {"variable": f"cpu_after_bad_code_{i+1}", "value": cpu_after},
        {"variable": f"ram_after_bad_code_{i+1}", "value": ram_after},
        {"variable": f"network_sent_after_bad_code_{i+1}", "value": net_sent_after},
        {"variable": f"network_recv_after_bad_code_{i+1}", "value": net_recv_after},
        {"variable": f"disk_after_bad_code_{i+1}", "value": disk_after},

        {"variable": f"bad_code_result_{i+1}", "value": str(result)[:50]}
    ])

# Running the Good Codes
for i, func in enumerate(good_functions):
    cpu_before = measure_cpu_usage()
    ram_before = measure_ram_usage()
    net_sent_before = measure_network_sent()
    net_recv_before = measure_network_recv()
    disk_before = measure_disk_usage()

    result = func()

    cpu_after = measure_cpu_usage()
    ram_after = measure_ram_usage()
    net_sent_after = measure_network_sent()
    net_recv_after = measure_network_recv()
    disk_after = measure_disk_usage()

    data.extend([
        {"variable": f"cpu_before_good_code_{i+1}", "value": cpu_before},
        {"variable": f"ram_before_good_code_{i+1}", "value": ram_before},
        {"variable": f"network_sent_before_good_code_{i+1}", "value": net_sent_before},
        {"variable": f"network_recv_before_good_code_{i+1}", "value": net_recv_before},
        {"variable": f"disk_before_good_code_{i+1}", "value": disk_before},

        {"variable": f"cpu_after_good_code_{i+1}", "value": cpu_after},
        {"variable": f"ram_after_good_code_{i+1}", "value": ram_after},
        {"variable": f"network_sent_after_good_code_{i+1}", "value": net_sent_after},
        {"variable": f"network_recv_after_good_code_{i+1}", "value": net_recv_after},
        {"variable": f"disk_after_good_code_{i+1}", "value": disk_after},

        {"variable": f"good_code_result_{i+1}", "value": str(result)[:50]}
    ])

# ---------- Send Data ----------
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
