# -*- coding: utf-8 -*-
# @Author  : CCY
import uiautomator2 as u2
import time, random

# 网易云音乐包名
PKG = "com.netease.cloudmusic"
#请在此处修改“Install”为你设备所显示的应用市场弹窗中的文字（根据系统语言而定）
install = "Install"
# 常见应用商店包名 (主要是小米，也加上其他的防万一)
MARKET_PKGS = [
    "com.xiaomi.market",       # 小米应用商店
    "com.huawei.appmarket",    # 华为
    "com.oppo.market",         # OPPO
    "com.bbk.appstore",        # vivo
    "com.tencent.android.qqdownloader" # 应用宝
]

# === 连接设备 ===
try:
    d = u2.connect()
    print(f"已连接设备: {d.info.get('productName', 'Unknown')}")
except Exception as e:
    print(f"连接失败: {e}")

def zzz(a=0.8, b=1.8):
    """随机等待一段时间"""
    time.sleep(a + random.random()*(b-a))

# === 智能点击函数 ===
def smart_click(index=None, **selector):
    try:
        obj = d(**selector)
        if index is not None:
            obj = obj[index]
        if not obj.exists:
            return False
        obj.click()
        print(f"✅ 点击 {selector}")
        return True
    except Exception as e:
        print(f"❌ smart_click 执行出错: {e}")
        return False

def check_back():
    """检查是否有快速验证弹窗"""
    if d(textContains="快速验证").exists:
        print("⚠️ 检测到验证弹窗，尝试返回...")
        d.press('back')

if __name__ == "__main__":
    print("🚀 脚本开始运行...")
    d.app_start(PKG)
    zzz(2)

    total_loops = 7
    for i in range(1, total_loops + 1):
        print(f"\n========== 正在执行第 {i} / {total_loops} 次循环 ==========")
        
        # 1. 点击“看视频，点亮拼图”
        if smart_click(textContains="看视频，点亮拼图"):
            print("等待视频/广告页加载...")
            zzz(2.5, 3.5)
            
            # 2. 点击“进入落地页查看详情”
            if d(textContains="进入落地页查看详情").exists(timeout=5):
                smart_click(textContains="进入落地页查看详情")
                print("已点击进入落地页，等待跳转检测...")
                
                # 给一点时间让手机反应（跳转或弹窗）
                time.sleep(3)
                
                # === 核心修改：检测应用市场跳转或弹窗 ===
                current_app = d.app_current()
                current_pkg = current_app.get("package")
                
                # --- 情况 A: 此时已跳转到应用商店 APP ---
                if current_pkg in MARKET_PKGS:
                    print(f"⚠️ 检测到跳转至应用商店 ({current_pkg})")
                    print("⏳ 保持在应用商店，等待 10 秒...")
                    time.sleep(10)
                    
                    print("🔙 执行应用商店返回流程 (3快+1慢)...")
                    # 3次返回，间隔0.5秒
                    for _ in range(3):
                        d.press("back")
                        time.sleep(0.5)
                    
                    # 再进行1次返回
                    d.press("back")
                    
                    print("✅ 应用商店流程结束，跳过后续步骤，直接进入下一次循环")
                    zzz(2)
                    continue  # <--- 关键：跳过本次循环剩余代码，直接开始第 i+1 次
                
                # --- 情况 B: 还在原APP，但有“应用商店”小窗口/弹窗 ---
                # 判断依据：当前包名还是网易云，但屏幕上有"应用商店"或"安装"字样
                elif d(textContains="应用商店").exists or d(text=install).exists:
                    print("⚠️ 检测到应用商店小窗口/弹窗")
                    print("🔙 点击一次返回以关闭弹窗")
                    d.press("back")
                    zzz(1)
                    
                    print("⏳ 弹窗关闭，继续观看广告 10 秒...")
                    time.sleep(10)
                    # 这里不加 continue，代码会自然向下执行“标准返回流程”
                
                # --- 情况 C: 普通网页/落地页 ---
                else:
                    print("ℹ️ 未检测到应用商店，按普通网页处理")
                    #判断用了几秒，所以此处不用12秒等待
                    print("⏳ 正在浏览，等待 7 秒...")
                    time.sleep(7)

            else:
                print("ℹ️ 未找到'进入落地页'按钮，继续等待...")
                time.sleep(12) # 如果没按钮，可能是纯视频，也等一会

            # === 标准返回流程 (如果执行了情况A，上面会continue跳过这里) ===
            print("🔙 [标准流程] 第 1 次返回")
            d.press("back")
            zzz(1.5, 2.0)

            print("🔙 [标准流程] 第 2 次返回")
            d.press("back")
            
            check_back()
            
            print("休息 2 秒...")
            zzz(2.0, 3.0)
            
        else:
            print("⚠️ 未在当前屏幕找到 '看视频，点亮拼图' 按钮")
            zzz(1)

    print("\n✅ 所有任务循环已完成。")