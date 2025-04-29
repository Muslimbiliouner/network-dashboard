import streamlit as st
import pandas as pd
import plotly.express as px
import threading
import time
from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP

# Optional: Auto-refresh every few seconds
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Packet Processor Class ---
class PacketProcessor:
    def __init__(self):
        self.protocol_map = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
        self.packet_data = []
        self.start_time = datetime.now()
        self.lock = threading.Lock()

    def get_protocol_name(self, proto_num):
        return self.protocol_map.get(proto_num, f'OTHER({proto_num})')

    def process_packet(self, packet):
        try:
            if IP in packet:
                with self.lock:
                    packet_info = {
                        'timestamp': datetime.now(),
                        'source': packet[IP].src,
                        'destination': packet[IP].dst,
                        'protocol': self.get_protocol_name(packet[IP].proto),
                        'size': len(packet),
                        'time_relative': (datetime.now() - self.start_time).total_seconds(),
                        'src_port': None,
                        'dst_port': None,
                        'tcp_flags': None
                    }

                    if TCP in packet:
                        packet_info.update({
                            'src_port': packet[TCP].sport,
                            'dst_port': packet[TCP].dport,
                            'tcp_flags': str(packet[TCP].flags)
                        })
                    elif UDP in packet:
                        packet_info.update({
                            'src_port': packet[UDP].sport,
                            'dst_port': packet[UDP].dport
                        })

                    self.packet_data.append(packet_info)

                    # Keep only last 10,000 packets
                    if len(self.packet_data) > 10000:
                        self.packet_data.pop(0)
        except Exception as e:
            logger.error(f"Error processing packet: {str(e)}")

    def get_dataframe(self):
        with self.lock:
            return pd.DataFrame(self.packet_data)

# --- Start Capture ---
def start_packet_capture():
    processor = PacketProcessor()

    def capture_packets():
        sniff(prn=processor.process_packet, store=False, filter="tcp or udp")

    capture_thread = threading.Thread(target=capture_packets, daemon=True)
    capture_thread.start()

    return processor

# --- Create Visualizations ---
def dashboard_tabs(df):
    tabs = st.tabs(["📈 Overview", "🔍 IP Analysis", "🛡️ TCP Flags", "📦 Packet Sizes", "💾 Save Data"])

    with tabs[0]:  # Overview
        st.subheader("Protocol Distribution")
        if not df.empty:
            fig = px.pie(df, names="protocol", title="Protocols Captured")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Packets Over Time")
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            timeline = df.groupby(df['timestamp'].dt.floor('S')).size()
            fig2 = px.line(x=timeline.index, y=timeline.values, labels={"x": "Time", "y": "Packets"}, title="Packets per Second")
            st.plotly_chart(fig2, use_container_width=True)

    with tabs[1]:  # IP Analysis
        st.subheader("Top Source IPs")
        if not df.empty:
            top_sources = df['source'].value_counts().head(10)
            fig3 = px.bar(x=top_sources.index, y=top_sources.values, labels={"x": "Source IP", "y": "Count"})
            st.plotly_chart(fig3, use_container_width=True)

            st.subheader("Top Destination IPs")
            top_destinations = df['destination'].value_counts().head(10)
            fig4 = px.bar(x=top_destinations.index, y=top_destinations.values, labels={"x": "Destination IP", "y": "Count"})
            st.plotly_chart(fig4, use_container_width=True)

            st.subheader("Top Source-Destination Pairs")
            pairs = df.groupby(['source', 'destination']).size().sort_values(ascending=False).head(10)
            pairs_df = pairs.reset_index(name="count")
            fig5 = px.bar(pairs_df, x="count", y=pairs_df.apply(lambda x: f"{x['source']} → {x['destination']}", axis=1), orientation='h')
            st.plotly_chart(fig5, use_container_width=True)

    with tabs[2]:  # TCP Flags
        st.subheader("TCP Flags Breakdown")
        if 'tcp_flags' in df.columns and not df['tcp_flags'].dropna().empty:
            flags_count = df['tcp_flags'].value_counts()
            fig6 = px.bar(x=flags_count.index, y=flags_count.values, labels={"x": "TCP Flags", "y": "Count"})
            st.plotly_chart(fig6, use_container_width=True)
        else:
            st.info("No TCP packets captured yet.")

    with tabs[3]:  # Packet Sizes
        st.subheader("Packet Size Distribution")
        if not df.empty:
            fig7 = px.histogram(df, x="size", nbins=50, title="Packet Sizes (Bytes)")
            st.plotly_chart(fig7, use_container_width=True)

    with tabs[4]:  # Save Data
        st.subheader("Download Captured Packets")
        if not df.empty:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="captured_packets.csv",
                mime="text/csv",
            )

# --- Main App ---
def main():
    st.set_page_config(page_title="🛰️ PRO Network Traffic Monitor", layout="wide")
    st.title("🛰️ Real-Time Network Traffic Analysis (Pro Version)")

    # Optional Auto-refresh every 5s
    if st_autorefresh:
        st_autorefresh(interval=5000, limit=None, key="refresh_counter")

    if 'processor' not in st.session_state:
        st.session_state.processor = start_packet_capture()
        st.session_state.start_time = time.time()

    df = st.session_state.processor.get_dataframe()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📦 Total Packets", len(df))
    with col2:
        duration = time.time() - st.session_state.start_time
        st.metric("⏳ Capture Duration", f"{duration:.2f}s")

    if not df.empty:
        dashboard_tabs(df)
    else:
        st.warning("Waiting for packets... Make sure you have traffic or try pinging/google browsing.")

    if st.button("🔄 Manual Refresh"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()
