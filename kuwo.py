"""
酷我音乐API - 精简版命令行工具
使用方法：
    python kuwo.py              # 交互式选择
    python kuwo.py --all        # 调用全部API
    python kuwo.py --rank       # 只获取排行榜
    python kuwo.py --playlist   # 只获取歌单
"""

import sys
import uuid
import requests


class KuwoAPI:
    """酷我音乐API精简客户端"""
    
    BASE_URL = "https://kuwo.cn"
    
    def __init__(self, secret, cookies):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'secret': secret
        })
        # 解析Cookie
        for item in cookies.split('; '):
            if '=' in item:
                k, v = item.split('=', 1)
                self.session.cookies.set(k, v)
    
    def _request(self, endpoint, params, referer):
        """发送请求"""
        params.update({'httpsStatus': '1', 'reqId': str(uuid.uuid1()), 'plat': 'web_www', 'from': ''})
        try:
            r = self.session.get(f"{self.BASE_URL}{endpoint}", params=params, headers={'Referer': referer}, timeout=10)
            return r.json() if r.status_code == 200 else None
        except:
            return None
    
    def rank(self, bang_id=17, page=1, size=10):
        """获取排行榜"""
        return self._request("/api/www/bang/bang/musicList", {'bangId': bang_id, 'pn': page, 'rn': size}, f"{self.BASE_URL}/rankList")
    
    def playlist(self, page=1, size=10, order="new"):
        """获取歌单"""
        params = {'pn': page, 'rn': size}
        if order == "hot": params['order'] = 'hot'
        return self._request("/api/www/classify/playlist/getRcmPlayList", params, f"{self.BASE_URL}/playlists")
    
    def detail(self, pid, page=1, size=100):
        """获取歌单详情"""
        return self._request("/api/www/playlist/playListInfo", {'pid': pid, 'pn': page, 'rn': size}, f"{self.BASE_URL}/playlist_detail/{pid}")


def print_songs(data, title="歌曲列表"):
    """打印歌曲列表"""
    if not data or data.get('code') != 200:
        print(f"❌ 获取失败: {data.get('message') if data else '请求错误'}")
        return
    
    songs = data.get('data', {}).get('musicList', [])
    print(f"\n{'='*60}\n{title} (共{len(songs)}首)\n{'='*60}")
    for i, s in enumerate(songs, 1):
        print(f"{i:2}. {s.get('name')} - {s.get('artist')}")


def print_playlists(data, title="歌单列表"):
    """打印歌单列表"""
    if not data or data.get('code') != 200:
        print(f"❌ 获取失败: {data.get('message') if data else '请求错误'}")
        return
    
    lists = data.get('data', {}).get('data', [])
    print(f"\n{'='*60}\n{title} (共{len(lists)}个)\n{'='*60}")
    for i, p in enumerate(lists, 1):
        if isinstance(p, dict):
            print(f"{i:2}. {p.get('name', p.get('img', 'Unknown'))} - 播放:{p.get('listencnt', 'N/A')}")


def run_all(api):
    """运行全部API"""
    print("\n🎵 酷我音乐API - 全部测试\n")
    
    # 1. 飙升榜
    print_songs(api.rank(93, 1, 5), "飙升榜 Top5")
    
    # 2. 热歌榜
    print_songs(api.rank(16, 1, 5), "热歌榜 Top5")
    
    # 3. 流行榜
    print_songs(api.rank(17, 1, 5), "流行榜 Top5")
    
    # 4. 最热歌单
    print_playlists(api.playlist(1, 5, "hot"), "最热歌单 Top5")
    
    # 5. 最新歌单
    print_playlists(api.playlist(1, 5, "new"), "最新歌单 Top5")


def interactive_mode(api):
    """交互式模式"""
    while True:
        print("\n" + "="*60)
        print("🎵 酷我音乐API")
        print("="*60)
        print("1. 飙升榜")
        print("2. 热歌榜")
        print("3. 流行榜")
        print("4. 最热歌单")
        print("5. 最新歌单")
        print("6. 全部测试")
        print("0. 退出")
        print("="*60)
        
        choice = input("\n请选择 (0-6): ").strip()
        
        if choice == '0':
            print("👋 再见！")
            break
        elif choice == '1':
            print_songs(api.rank(93, 1, 20), "飙升榜 Top20")
        elif choice == '2':
            print_songs(api.rank(16, 1, 20), "热歌榜 Top20")
        elif choice == '3':
            print_songs(api.rank(17, 1, 20), "流行榜 Top20")
        elif choice == '4':
            print_playlists(api.playlist(1, 20, "hot"), "最热歌单 Top20")
        elif choice == '5':
            print_playlists(api.playlist(1, 20, "new"), "最新歌单 Top20")
        elif choice == '6':
            run_all(api)
        else:
            print("❌ 无效选择")


def main():
    # 从浏览器获取 (首次使用需要手动填写)
    SECRET = "4808c5e1637d1c18866894db2f82ff5a6aa79aa70389cb503fc702dfc3c750bb056fc4c3"
    COOKIES = "Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1759400246,1759492551; HMACCOUNT=ACF8C8B39A45F6FE; _ga=GA1.2.646944111.1759492551; _gid=GA1.2.1612503252.1759492551; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1759493846; Hm_Iuvt_cdb524f42f23cer9b268564v7y735ewrq2324=kXNCrZt3XM4Jd8Nwbhkp4sWW6GyFEA57; _ga_ETPBRPM9ML=GS2.2.s1759492551$o1$g1$t1759493846$j60$l0$h0"
    
    # 检查是否设置了Secret
    if SECRET.startswith("从浏览器") or len(SECRET) < 50:
        print("\n❌ 请先设置SECRET和COOKIES！")
        print("\n获取方法：")
        print("1. 访问 https://kuwo.cn/rankList")
        print("2. 按F12打开开发者工具")
        print("3. 切换到Network标签，刷新页面")
        print("4. 找到musicList请求，复制Request Headers中的：")
        print("   - secret: xxxx")
        print("   - cookie: xxxx")
        print("5. 粘贴到本文件的SECRET和COOKIES变量中")
        print("\n然后重新运行此脚本。\n")
        return
    
    api = KuwoAPI(SECRET, COOKIES)
    
    # 命令行参数
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--all', '-a']:
            run_all(api)
        elif arg in ['--rank', '-r']:
            print_songs(api.rank(17, 1, 20), "流行榜 Top20")
        elif arg in ['--playlist', '-p']:
            print_playlists(api.playlist(1, 20, "hot"), "最热歌单 Top20")
        else:
            print(f"未知参数: {arg}")
            print("用法: python kuwo.py [--all|--rank|--playlist]")
    else:
        # 交互式模式
        interactive_mode(api)


if __name__ == "__main__":
    main()

