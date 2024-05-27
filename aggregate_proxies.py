import yaml
import requests

def load_yaml(url):
    response = requests.get(url)
    return yaml.safe_load(response.text)

def save_yaml(data, filename):
    with open(filename, 'w') as file:
        yaml.safe_dump(data, file)

def remove_duplicates(nodes):
    seen = set()
    unique_nodes = []
    for node in nodes:
        identifier = node['name']  # 假设每个节点都有唯一的'name'字段作为标识
        if identifier not in seen:
            seen.add(identifier)
            unique_nodes.append(node)
    return unique_nodes

# URL列表
urls = [
    "https://raw.githubusercontent.com/fighter2011/aggregator/main/aggregate/data/proxies.yaml",
    "https://raw.githubusercontent.com/bibistellar/aggregator/main/data/proxies.yaml",
    "https://raw.githubusercontent.com/harrylisen/aggregator/main/aggregate/data/proxies.yaml",
    "https://raw.githubusercontent.com/zzr2002314/aggregator/master/aggregate/data/proxies.yaml",
    "https://raw.githubusercontent.com/dreamtonight/vpn/master/data/proxies.yaml",
    "https://raw.githubusercontent.com/xnic888/aggregator/main/aggregate/data/proxies.yaml",
    "https://pastebin.com/raw/grshqq71"
]

# 加载和整合数据
all_nodes = []
for url in urls:
    data = load_yaml(url)
    all_nodes.extend(data['proxies'])  # 假设每个YAML文件的节点信息都在'proxies'键下

# 去重节点
unique_nodes = remove_duplicates(all_nodes)

# 保存结果
save_yaml({'proxies': unique_nodes}, 'aggregated_proxies.yaml')
