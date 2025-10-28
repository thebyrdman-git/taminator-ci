# Fix Rocky Linux VM Network (No DHCP)

**Issue**: VM not getting IP from DHCP  
**Hypervisor**: KVM/libvirt  
**VM**: rfe-test-alma9-local

---

## Quick Diagnosis (Run in VM)

**On the Rocky Linux VM**, open terminal and run:

```bash
# Check if interface is up
ip link show

# Check current IP
ip addr show

# Check DHCP client
sudo systemctl status NetworkManager

# Try to get DHCP
sudo dhclient -v
```

---

## Solution 1: Restart NetworkManager (Easiest)

**In the VM**:

```bash
# Restart NetworkManager
sudo systemctl restart NetworkManager

# Wait 5 seconds, then check
ip addr show

# Should see IP like 192.168.122.x
```

**Test internet**:
```bash
ping -c 3 8.8.8.8
ping -c 3 google.com
```

---

## Solution 2: Manual Interface Up

**If interface is down**:

```bash
# Find interface name (usually enp1s0 or similar)
ip link show

# Bring it up
sudo ip link set enp1s0 up

# Request DHCP
sudo dhclient enp1s0

# Check IP
ip addr show enp1s0
```

---

## Solution 3: NetworkManager Configuration

**Check connection**:

```bash
# List connections
nmcli connection show

# Show devices
nmcli device status

# If disconnected, connect
nmcli device connect enp1s0

# Or restart connection
nmcli connection up "System enp1s0"
```

---

## Solution 4: Check VM Network Settings (Host Side)

**On your laptop (host)**, check VM settings:

```bash
# Check default network is running
sudo virsh net-list --all

# Should show:
# Name      State    Autostart   Persistent
# default   active   yes         yes

# If not active:
sudo virsh net-start default
sudo virsh net-autostart default

# Check DHCP range
sudo virsh net-dumpxml default | grep -A5 dhcp
```

---

## Solution 5: Reconfigure Network in virt-manager

**In virt-manager GUI**:

1. Right-click VM → **"Show virtual hardware details"**
2. Click **"NIC"** in left panel
3. **Network source**: Select "Virtual network 'default': NAT"
4. **Device model**: virtio
5. Click **"Apply"**
6. Restart VM

---

## Solution 6: Check Firewall (Host)

**On laptop (host)**:

```bash
# Check if firewall is blocking
sudo firewall-cmd --list-all

# Allow libvirt zone
sudo firewall-cmd --permanent --zone=libvirt --set-target=ACCEPT
sudo firewall-cmd --reload

# Or if using iptables
sudo iptables -L -n | grep FORWARD
```

---

## Solution 7: Reset to DHCP (In VM)

**If static IP was set before**:

```bash
# Edit connection
sudo nmcli connection modify "System enp1s0" ipv4.method auto

# Restart connection
sudo nmcli connection down "System enp1s0"
sudo nmcli connection up "System enp1s0"

# Check
ip addr show
```

---

## Solution 8: Recreate Network Connection (In VM)

**Nuclear option**:

```bash
# Delete existing connection
sudo nmcli connection delete "System enp1s0"

# Let NetworkManager recreate it
sudo systemctl restart NetworkManager

# Should auto-create and connect
nmcli connection show
```

---

## Expected Working State

**In VM, should see**:

```bash
$ ip addr show
...
enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP>
    inet 192.168.122.X/24 brd 192.168.122.255 scope global dynamic
```

**And**:

```bash
$ ping -c 3 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=115 time=15.2 ms
...
```

---

## Quick Troubleshooting Decision Tree

```
1. Is interface UP?
   NO → sudo ip link set enp1s0 up
   YES → Go to 2

2. Is NetworkManager running?
   NO → sudo systemctl start NetworkManager
   YES → Go to 3

3. Does interface have IP?
   NO → sudo dhclient enp1s0
   YES → Go to 4

4. Can ping gateway (192.168.122.1)?
   NO → Check VM network settings in virt-manager
   YES → Go to 5

5. Can ping 8.8.8.8?
   NO → Check DNS (see below)
   YES → Network working!

6. Can ping google.com?
   NO → DNS issue (see below)
   YES → ALL WORKING!
```

---

## DNS Fix (If Needed)

**If you can ping 8.8.8.8 but not google.com**:

```bash
# Check DNS
cat /etc/resolv.conf

# Should have:
# nameserver 192.168.122.1

# If missing, add it
echo "nameserver 192.168.122.1" | sudo tee /etc/resolv.conf

# Or use Google DNS
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

---

## After Network Works

**Transfer AppImage**:

```bash
# Option A: wget (if you host it)
wget http://YOUR_LAPTOP_IP:8000/Taminator-2.0.0.AppImage

# Option B: scp (now that network works!)
scp user@YOUR_LAPTOP_IP:/home/jbyrd/TAMINATOR/gui/dist/Taminator-2.0.0.AppImage ~/

# Option C: HTTP server on laptop
# On laptop: cd /home/jbyrd/TAMINATOR/gui/dist && python3 -m http.server 8000
# In VM: wget http://LAPTOP_IP:8000/Taminator-2.0.0.AppImage
```

---

## Common Issues

### Issue: "No suitable device found"
**Cause**: No network interface detected  
**Fix**: Check VM has NIC attached in virt-manager

### Issue: "Connection activation failed"
**Cause**: NetworkManager can't activate connection  
**Fix**: Recreate connection (Solution 8)

### Issue: "DHCP timeout"
**Cause**: Can't reach DHCP server  
**Fix**: Check host default network is active

### Issue: "Device not managed by NetworkManager"
**Cause**: Interface in /etc/sysconfig/network-scripts  
**Fix**: Remove old ifcfg files, let NetworkManager manage it

---

## Most Likely Solution

**Try this first** (works 90% of the time):

```bash
# In the VM:
sudo systemctl restart NetworkManager
sleep 5
ip addr show

# Should now have 192.168.122.X IP
# Test:
ping -c 3 8.8.8.8
```

**If that doesn't work, try Solution 8** (recreate connection).

---

**Once network works, continue with VM testing!** 🚀

