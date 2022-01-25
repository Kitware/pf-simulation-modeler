import click
import yaml
import json
import re

proxies = []
proxy_count = 1


def flatten_dict(dd, separator=".", prefix=""):
    return (
        {
            prefix + separator + k if prefix else k: v
            for kk, vv in dd.items()
            for k, v in flatten_dict(vv, separator, kk).items()
        }
        if isinstance(dd, dict)
        else {prefix: dd}
    )


def make_new_proxy(name):
    global proxy_count
    prox = {
        "id": proxy_count,
        "mtime": 1,
        "own": [],
        "name": name,
        "type": name,
        "tags": [],
        "properties": {},
    }
    proxy_count += 1
    return prox


def clean_value(value):
    # yaml.safe_load not specific enough (eg parses "1e-4" as string)
    if isinstance(value, str):
        try:
            value = float(value)
        except:
            pass
    return value


def add_proxies_for_dynamic_model(proxies, prefix, run, model_type_name, model_type):

    proxies_by_name = {}

    for (prop_name, prop) in model_type.items():

        if prop_name == "name" or prop_name.startswith("_") or "{" in prop_name:
            continue

        exportSuffix = prop["_exportSuffix"]
        for run_key in run.keys():

            # Build up regex to match dynamic run key
            dynamic_name_group = "\.([^.]+)\."
            regex = prefix + dynamic_name_group + exportSuffix + "$"
            match = re.match(regex, run_key)

            if match:

                # Collect proxies of this type by name
                dynamic_name = match.group(1)
                if dynamic_name not in proxies_by_name:
                    proxies_by_name[dynamic_name] = make_new_proxy(model_type_name)
                    proxies_by_name[dynamic_name]["properties"]["name"] = dynamic_name

                value = clean_value(run[run_key])
                proxies_by_name[dynamic_name]["properties"][prop_name] = value

    proxies[model_type_name] = list(proxies_by_name.values())


def add_key_to_proxy(new_proxy, prop_name, run, run_key, prop):
    if prop_name in ["name", "_exportPrefix"]:
        return
    for domain in prop.get("domains", []):
        if domain.get("type") == "ProxyBuilder":
            return
    exportSuffix = prop["_exportSuffix"]
    if exportSuffix == run_key:
        value = run[run_key]
        new_proxy["properties"][prop_name] = clean_value(value)


@click.command()
@click.option(
    "-r",
    "--run-file",
    required=True,
    help="A flat map of keys to value from a previous parflow run.",
)
@click.option(
    "-m",
    "--model-file",
    required=True,
    help="A pysimput model whose modeltypes will extract values from the run into proxies.",
)
@click.option(
    "-o",
    "--output",
    default="pf_settings.yaml",
    help="location to write the output to.",
)
def cli(run_file, model_file, output):

    with open(run_file) as run_file_handle:
        run = flatten_dict(yaml.safe_load(run_file_handle))
    with open(model_file) as model_file_handle:
        model_types = yaml.safe_load(model_file_handle)

    proxies = {}
    for (model_type_name, model_type) in model_types.items():

        prefix = model_type.get("_exportPrefix")
        static_model = not prefix

        if static_model:
            # Make one proxy for each modeltype, and fill it with run's values
            new_proxy = make_new_proxy(model_type_name)
            for (prop_name, prop) in model_type.items():
                for run_key in run.keys():
                    add_key_to_proxy(new_proxy, prop_name, run, run_key, prop)
            proxies[model_type_name] = [new_proxy]

        else:
            add_proxies_for_dynamic_model(
                proxies, prefix, run, model_type_name, model_type
            )

    flat_proxies = [proxy for model in proxies.values() for proxy in model]
    pf_settings = {"save": json.dumps({"model": model_types, "proxies": flat_proxies})}

    with open(output, "w") as output_handle:
        yaml.dump(pf_settings, output_handle)


if __name__ == "__main__":
    cli()
