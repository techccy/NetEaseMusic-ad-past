# NetEase Cloud Music Auto Task Script (网易云音乐自动任务脚本)

这是一个基于 Python 和 `uiautomator2` 的安卓自动化脚本，专为**网易云音乐**的“看视频，点亮拼图”积分任务设计。

它可以自动完成浏览广告任务，并具备**智能识别应用商店跳转**、**处理弹窗**以及**模拟真人操作**的高级功能，特别针对小米/Redmi 设备进行了优化。

## ✨ 功能特性 (Features)

* **🤖 全自动执行**：自动识别任务按钮，完成点击、浏览、返回的全流程（默认循环 7 次）。
* **🛡️ 智能防跳转**：
    * 检测到强制跳转至应用商店（如小米、华为、OPPO 商店）时，自动在此页面停留 10 秒，随后执行“3次快退 + 1次慢退”逻辑，确保从商店安全返回。
* **🧩 弹窗处理**：识别应用内的“应用商店小窗口”或“安装”弹窗，自动关闭并继续任务。
* **🧠 智能等待**：使用随机延迟（Random Sleep）模拟真人操作，降低被检测风险。
* **📱 兼容性**：基于 `uiautomator2`，支持绝大多数 Android 设备（已在 Redmi HyperOS/MIUI 上测试通过）。

## 🛠️ 环境要求 (Prerequisites)

在使用本脚本前，请确保你的环境满足以下要求：

* **Python 3.x**
* **ADB (Android Debug Bridge)**：已配置环境变量。
* **Android 设备**：
    * 开启 **USB 调试**。
    * **重要**：如果是小米/Redmi 手机，必须在开发者选项中开启 **USB 调试（安全设置）** 以允许模拟点击。

## 📦 安装与配置 (Installation)

1.  **克隆项目**
    ```bash
    git clone [https://github.com/你的用户名/你的仓库名.git](https://github.com/你的用户名/你的仓库名.git)
    cd 你的仓库名
    ```

2.  **安装依赖**
    ```bash
    pip install uiautomator2
    ```

3.  **初始化设备**
    连接手机并运行初始化命令（将在手机上安装 ATX 代理）：
    ```bash
    python -m uiautomator2 init
    ```

## 🚀 快速开始 (Quick Start)

1.  使用 USB 数据线连接 Android 手机至电脑。
2.  确保手机已解锁。
3.  运行脚本：
    ```bash
    python task.py
    ```
4.  脚本将自动启动网易云音乐 App 并开始执行任务。

## ⚙️ 核心逻辑说明

脚本针对广告跳转的处理逻辑如下：

| 场景 | 处理方式 |
| :--- | :--- |
| **普通视频广告** | 浏览 12-17 秒 -> 2 次返回 |
| **跳转至应用商店** | 停留 10 秒 -> 3 次快速返回 (间隔0.5s) -> 1 次普通返回 |
| **应用内弹窗** | 点击返回关闭弹窗 -> 继续浏览 10 秒 -> 标准返回流程 |

## 📝 配置说明

你可以在 `task.py` 顶部修改以下配置：

```python
# 目标应用包名
PKG = "com.netease.cloudmusic"
#请在此处修改“Install”为你设备所显示的应用市场弹窗中的文字（根据系统语言而定）
install = "Install"
# 循环次数
total_loops = 7

# 需要检测的应用商店列表
MARKET_PKGS = [
    "com.xiaomi.market",
    "com.huawei.appmarket",
    ...
]

## 📄 License

此项目遵循 [MIT License](LICENSE) 开源协议。

```text
Copyright (c) 2025 CCY
