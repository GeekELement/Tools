
# 使用 Ubuntu 开启 NFS 共享并在 Windows 上访问

## 一、在 Ubuntu 上设置 NFS 共享

### 1. 安装 NFS 服务

```bash
sudo apt update
sudo apt install nfs-kernel-server
```

### 2. 创建共享目录

```bash
sudo mkdir -p /mnt/nfs_share
```

### 3. 设置目录权限

```bash
sudo chown nobody:nogroup /mnt/nfs_share
sudo chmod 777 /mnt/nfs_share
```

### 4. 配置 NFS 导出

编辑 `/etc/exports` 文件，添加共享配置：

```bash
sudo nano /etc/exports
```

添加以下行（将 `<客户端_IP>` 替换为允许访问的客户端 IP 地址，或使用 `*` 表示允许所有）：

```
/mnt/nfs_share <客户端_IP>(rw,sync,no_subtree_check)
```

### 5. 导出共享

运行以下命令以应用更改：

```bash
sudo exportfs -ra
```

### 6. 启动 NFS 服务并设置自动启动

```bash
sudo systemctl enable nfs-server
sudo systemctl start nfs-server
```

### 7. 检查 NFS 服务状态

```bash
sudo systemctl status nfs-server
```

## 二、在 Windows 上访问 NFS 共享

### 1. 启用 NFS 客户端功能

1. 打开“控制面板”。
2. 点击“程序” > “程序和功能”。
3. 在左侧点击“启用或关闭 Windows 功能”。
4. 勾选“服务于 NFS 的客户端”。

### 2. 挂载 NFS 共享

打开命令提示符（以管理员身份），使用以下命令挂载 NFS 共享：

```bash
net use N: \\<服务器_IP>\mnt\nfs_share /persistent:yes
```

将 `<服务器_IP>` 替换为你的 NFS 服务器的 IP 地址。

### 3. 验证挂载

在文件资源管理器中，你应该能够看到驱动器 N:，并访问 NFS 共享的内容。

## 三、故障排除

- **检查 NFS 服务状态**：确保 Ubuntu 服务器上的 NFS 服务正在运行。
- **网络连接**：确保 Windows 机器能够 ping 通 NFS 服务器。
- **防火墙设置**：确保防火墙未阻止 NFS 连接。
- **查看事件查看器**：检查 Windows 事件查看器中的相关错误日志。
