#!/bin/bash  

# Sistem güncellemelerini yap  
sudo apt update -y && sudo apt upgrade -y  

# Gerekli paketleri yükle  
sudo apt install -y ca-certificates zlib1g-dev libncurses5-dev libgdbm-dev \
libnss3-dev tmux iptables curl nvme-cli git wget make jq libleveldb-dev \
build-essential pkg-config ncdu tar clang bsdmainutils lsb-release \
libssl-dev libreadline-dev libffi-dev jq gcc screen unzip lz4  

# Rust'u kur  
curl --proto '=https' --tlsv1.3 https://sh.rustup.rs -sSf | sh  
source "$HOME/.cargo/env"  

# Yeni bir screen oturumu başlat ve Nexus CLI'yi kur  
screen -S nexus -d -m bash -c "curl https://cli.nexus.xyz/install.sh | sh; exit"  

# Screen oturumundan çık  
sleep 5  # Kurulumun tamamlanması için kısa bir bekleme süresi  
screen -S nexus -X quit  

# Prover ID'yi görüntüle  
echo "Prover ID:"  
cat "$HOME/.nexus/prover-id"
