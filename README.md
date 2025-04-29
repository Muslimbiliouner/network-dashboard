# 🛰️ Real-Time Network Traffic Monitor (Pro Version)

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-%23FF4B4B.svg?&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Real-time network traffic monitoring dashboard built with **Python**, **Streamlit**, **Plotly**, and **Scapy**.  
Capture live TCP/UDP packets, visualize interactively, and analyze your network activity in real-time.

---

## 📚 Table of Contents
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Code Structure](#-code-structure)
- [Installation](#installation)
- [Usage](#-usage)
- [License](#-license)
- [Credits](#-credits)

---

## ✨ Features
- 📦 Capture live network traffic (TCP and UDP packets)
- 📈 Real-time interactive dashboard with auto-refresh
- 🌎 Top Source & Destination IP analysis
- 🛡️ TCP Flags breakdown visualization
- 📊 Packet Size distribution
- 💾 Export captured data to CSV
- ⚡ Lightweight, runs locally in minutes

---

## 📷 Screenshots

### 📈 Protocols Captured
![Protocols Captured](screenshots/Protocols%20Captured.png)  
Visualisasi distribusi protokol jaringan (seperti TCP, UDP, ICMP) dalam bentuk pie chart. Menunjukkan proporsi paket yang ditangkap berdasarkan jenis protokol.

---

### 📈 Packets Over Time
![Packets Over Time](screenshots/Packets%20Over%20Time.png)  
Grafik jumlah paket yang diterima per detik. Memberikan gambaran lalu lintas jaringan sepanjang waktu.

---

### 🔍 Top Source IPs
![Top Source IPs](screenshots/Top%20Source%20IPs.png)  
Menampilkan daftar IP sumber teratas yang mengirimkan paket terbanyak. Membantu mengidentifikasi perangkat aktif dalam jaringan.

---

### 🔍 Top Destination IPs
![Top Destination IPs](screenshots/Top%20Destination%20IPs.png)  
Menampilkan daftar IP tujuan teratas yang menerima paket terbanyak. Berguna untuk melihat target utama komunikasi jaringan.

---

### 🔍 Top Source-Destination Pairs
![Top Source-Destination Pairs](screenshots/Top%20Source-Destination%20Pairs.png)  
Menganalisis pasangan IP sumber dan tujuan yang paling banyak berinteraksi. Memberikan insight ke jalur komunikasi dominan.

---

### 🛡️ TCP Flags Breakdown
![TCP Flags Breakdown](screenshots/TCP%20Flags%20Breakdown.png)  
Visualisasi distribusi flag TCP (seperti SYN, ACK, FIN). Penting untuk analisis perilaku koneksi TCP.

---

### 📦 Packet Size Distribution
![Packet Size Distribution](screenshots/Packet%20Size%20Distribution.png)  
Histogram ukuran paket yang ditangkap. Membantu memahami besar kecilnya data yang melewati jaringan.

---

## Code Structure

| File | Deskripsi |
|:-----|:----------|
| `dashboard.py` | Aplikasi utama Streamlit yang menjalankan packet capturing, visualisasi, dan dashboard interaktif. |
| `requirements.txt` | Daftar dependencies Python yang diperlukan. |
| `screenshots/` | Folder berisi gambar tangkapan layar untuk dokumentasi. |

### Penjelasan `dashboard.py`
- **Import Libraries**:  
  Mengimpor Streamlit, Pandas, Plotly, threading, Scapy, dan utilitas lainnya.

- **PacketProcessor Class**:  
  Class utama untuk menangani parsing dan penyimpanan data paket yang ditangkap.

- **start_packet_capture Function**:  
  Memulai proses penangkapan paket di thread terpisah agar tidak menghambat UI.

- **dashboard_tabs Function**:  
  Membuat tab-tab di dashboard Streamlit untuk berbagai analisis (Overview, IP Analysis, TCP Flags, dll).

- **main Function**:  
  Mengatur keseluruhan jalannya aplikasi, memanggil packet capture dan menampilkan dashboard.

---

## Installation

Clone the repository:

\`\`\`bash
git clone https://github.com/Muslimbiliouner/network-dashboard.git
cd network-dashboard
\`\`\`

Create a virtual environment (optional but recommended):

\`\`\`bash
conda create --name myenv python=3.11
conda activate myenv
\`\`\`

Install the required packages:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

If needed, install system libraries:

\`\`\`bash
sudo apt update
sudo apt install libpcap-dev libpcap0.8-dev
\`\`\`

---

## 🚀 Usage

Run the Streamlit app:

\`\`\`bash
streamlit run dashboard.py
\`\`\`

or you can use:

\`\`\`bash
sudo env "PATH=$PATH" streamlit run dashboard.py
\`\`\`

> **Note:**  
> You need to generate some network activity (e.g., open websites, ping servers) to see captured packets in real-time.

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙌 Credits

Built with ❤️ by **Rahmatulloh Muslimbiliouner**  
- GitHub: [@Muslimbiliouner](https://github.com/Muslimbiliouner)
- LinkedIn : [Rahmatulloh](https://www.linkedin.com/in/rahmatulloh-655578263)
