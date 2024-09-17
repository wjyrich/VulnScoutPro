import os

from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
import json

base_file_path = 'dirscan/dirsearch/reports/target.json'

@login_required
def dirresult(request):
    if os.access(base_file_path, os.F_OK):
        f = open(base_file_path)
        data = json.load(f)  # json被转换为python字典

        # 获取扫描url的端口等信息，将字典的键转为集合
        # 获取info中的键
        info_keys = set(data["info"].keys())
        info_keys.discard('time')  # 安全移除'time'
        info_keys.discard('args')   # 安全移除'args'
        key_list = list(info_keys)

        # 提取URL
        urls = []
        for result in data["results"]:
            for url in result.keys():
                urls.append(url)

        # 将提取的URL添加到key_list
        key_list.extend(urls)

        # 计数
        n = 0
        for key in data:
            n = n + 1
        # 列表合一
        a = []
        num = 0
        # 遍历results列表
        for result in data["results"]:
            for url, items in result.items():
                for item in items:
                    # 提取path和status
                    path_status = {
                        "path": item.get("path"),
                        "status": item.get("status")
                    }
                    a.append(path_status)  # 将提取的字典添加到结果列表中

        print({"a": a, "key_list": key_list})
        return render(request, "dir-result.html", {"a": a, "key_list": key_list})
    else:
        error = "暂无结果"
        return render(request, "dir-result.html", {"error": error})
