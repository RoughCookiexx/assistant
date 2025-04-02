import yaml

def match_yaml_pair(yaml_data, key, value):
    result = ""

    if isinstance(yaml_data, dict):
        for k, v in yaml_data.items():
            if k == key and v == value:
                result += yaml.dump(yaml_data)
                break
            else:
                result += match_yaml_pair(v, key, value)

    elif isinstance(yaml_data, list):
        for item in yaml_data:
            result += match_yaml_pair(item, key, value)

    return result


