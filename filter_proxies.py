import yaml
import requests
import os

def filter_nodes_by_keyword(yaml_url, keyword):
    response = requests.get(yaml_url)
    data = yaml.safe_load(response.content)
    
    filtered_nodes = []
    for node in data['proxies']:
        if keyword in node['name']:
            filtered_nodes.append(node)
    
    return filtered_nodes

def deduplicate_nodes(nodes):
    seen = set()
    unique_nodes = []
    for node in nodes:
        identifier = (node['server'], node['port'], node['type'])
        if identifier not in seen:
            seen.add(identifier)
            unique_nodes.append(node)
    return unique_nodes

def main():
    yaml_urls = [
        'https://raw.githubusercontent.com/zzr2002314/aggregator/main/data/clash.yaml',
        'https://raw.githubusercontent.com/qjlxg/aggregator/main/data/clash.yaml',
        'https://raw.githubusercontent.com/qjlxg/aggregator/main/data/clash.yaml'
    ]
    keyword = '美'

    all_filtered_nodes = []
    for yaml_url in yaml_urls:
        filtered_nodes = filter_nodes_by_keyword(yaml_url, keyword)
        all_filtered_nodes.extend(filtered_nodes)

    unique_nodes = deduplicate_nodes(all_filtered_nodes)
    
    output_dir = 'data1'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'aggregated_proxies.yaml')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({'proxies': unique_nodes}, f, allow_unicode=True)
    
    print(f"Filtered and deduplicated {len(unique_nodes)} nodes, saved to {output_file}")

if __name__ == '__main__':
    main()
