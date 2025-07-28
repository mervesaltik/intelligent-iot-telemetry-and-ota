# Intelligent IoT-Based Telemetry and Adaptive Over-the-Air (OTA) Update Mechanism

## 👩🏻‍💻 Developed By

- [Merve Saltık](https://github.com/mervesaltik)
- [Sude Güzel](https://github.com/sdgzl)
- [Aleyna Menekşe](https://github.com/Aleynamnks)  

## 🧠 Project Overview

This system collects telemetry data from IoT devices (CPU, memory, network, and power metrics) and uses a machine learning model to evaluate the impact of software updates. If an update enhances device performance and stability, it is approved. Otherwise, it is blocked. This intelligent OTA update mechanism increases system resilience and reduces update-induced failures.


## 🎯 Motivation

Traditional IoT update mechanisms often ignore real-time system data, which can lead to excessive CPU loads, memory leaks, or network congestion. This project aims to:
- Evaluate real-time performance metrics.
- Apply updates only if they improve or maintain performance.
- Create a smarter, adaptive, and failure-resistant IoT ecosystem.

## 🔬 Methodology

The proposed approach combines:
- **Continuous Monitoring:** Real-time tracking of CPU, RAM, network, and power usage to understand device performance before updates.
- **Machine Learning Anomaly Detection:** ML models classify device states as “good” or “bad” based on telemetry data, helping to assess the impact of updates.
- **Adaptive OTA Updates:** Updates are only applied if they improve or maintain performance. Harmful updates are blocked automatically to protect device stability and resources.

## 🕵🏻‍♀️ Results Presentation And Discussion

To evaluate how software quality impacts system resources, we first developed Python scripts that simulate both inefficient (bad) and optimized (good) code. These scripts were executed on a local machine to measure their effects on CPU usage, RAM consumption, network activity, and disk operations. The resource data was collected in real-time and transmitted to an IoT analytics platform called TagoIO using a device token.

On the TagoIO platform:
- A virtual device was created.
- Telemetry data from each script execution was sent to this device in real time.
- The data was then exported as CSV and JSON formats for further analysis.
