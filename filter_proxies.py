import yaml
import requests
import os

def filter_nodes_by_region(yaml_url, regions):
    response = requests.get(yaml_url)
    data = yaml.safe_load(response.content)
    
    filtered_nodes = []
    for node in data['proxies']:
        for region in regions:
            if any(keyword in node['name'] for keyword in regions[region]):
                filtered_nodes.append(node)
                break
    
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
    yaml_url = 'https://raw.githubusercontent.com/ailongfei/aggregator/main/data/clash.yaml'
    regions = {
        'Hong Kong': ['港'],
        'Taiwan': ['台'],
        'Korea': ['韩'],
        'Japan': ['日'],
        'Singapore': ['新']
    }

    filtered_nodes = filter_nodes_by_region(yaml_url, regions)
    unique_nodes = deduplicate_nodes(filtered_nodes)
    
    output_dir = 'data1'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'aggregated_proxies.yaml')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({'proxies': unique_nodes}, f, allow_unicode=True)
    
    print(f"Filtered and deduplicated {len(unique_nodes)} nodes, saved to {output_file}")

if __name__ == '__main__':
    main()
