import time
import schedule
import pandas as pd
from main import measure_cpu_usage, measure_ram_usage, measure_disk_usage, measure_network_sent, measure_network_recv
from model import make_prediction
from tagosender import send_to_tago


def save_to_csv(cpu, disk, network_recv, network_sent, ram):
    # Adds data to CSV
    data = {
        "cpu": [cpu],
        "disk": [disk],
        "network_recv": [network_recv],
        "network_sent": [network_sent],
        "ram": [ram]
    }
    df = pd.DataFrame(data)

    # If the file does not exist, write a title, if it does, do not write a title
    try:
        df.to_csv('output22.csv', mode='a', index=False, header=False)
    except ValueError:
        df.to_csv('output22.csv', mode='w', index=False, header=True)


def collect_and_predict(save_resource_data=False):

    cpu_before = measure_cpu_usage()
    ram_before = measure_ram_usage()
    disk_before = measure_disk_usage()
    network_sent_before = measure_network_sent()
    network_recv_before = measure_network_recv()

    # wait
    time.sleep(5)

    # Measure next values
    cpu_after = measure_cpu_usage()
    ram_after = measure_ram_usage()
    disk_after = measure_disk_usage()
    network_sent_after = measure_network_sent()
    network_recv_after = measure_network_recv()

    # Calculate the differences
    cpu_diff = cpu_after - cpu_before
    disk_diff = disk_after - disk_before
    network_recv_diff = network_recv_after - network_recv_before
    network_sent_diff = network_sent_after - network_sent_before
    ram_diff = ram_after - ram_before

    # Make a prediction with the model
    prediction = make_prediction(cpu_diff, disk_diff, network_recv_diff, network_sent_diff, ram_diff)
    print(f"Predicted result: {prediction}")

    # Send predictions and data to Tago
    send_to_tago({
        "cpu": cpu_diff,
        "disk": disk_diff,
        "network_recv": network_recv_diff,
        "network_sent": network_sent_diff,
        "ram": ram_diff
    }, prediction)

    # Save to CSV if desired
    if save_resource_data:
        save_to_csv(cpu_diff, disk_diff, network_recv_diff, network_sent_diff, ram_diff)


# Set Schedule
schedule.every(15).seconds.do(collect_and_predict, save_resource_data=True)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Program finished.")

