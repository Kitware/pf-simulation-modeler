import click
import yaml
from pathlib import Path


def add_type(node, prop):
    if "domains" not in node:
        return
    if "DoubleValue" in node["domains"]:
        prop["type"] = "float32"
        return
    if "IntValue" in node["domains"]:
        prop["type"] = "int8"
        return
    prop["type"] = "string"


def add_help(node, prop):
    help_text = node.get("help", "").strip("\n").split("] ", 1)
    prop["_help"] = help_text[1] if len(help_text) > 1 else help_text[0]


def add_domains(node, prop, name, property_name):
    domains = node.get("domains")
    if not domains:
        return

    # Check for Range
    for numeric_domain in ["DoubleValue", "IntValue"]:
        if domains.get(numeric_domain):
            min_value = None
            max_value = None
            if "min_value" in domains[numeric_domain]:
                min_value = domains[numeric_domain]["min_value"]
            if "max_value" in domains[numeric_domain]:
                max_value = domains[numeric_domain]["max_value"]
            if min_value is not None or max_value is not None:
                prop["domains"] = [
                    {
                        "type": "Range",
                        "value_range": [min_value, max_value],
                        "level": 1,
                    }
                ]
                return

    # Check for LabelList
    enum_list = node["domains"].get("EnumDomain", {}).get("enum_list")
    if enum_list:
        prop["domains"] = [
            {
                "type": "LabelList",
                "values": [{"text": name, "value": name} for name in enum_list],
            }
        ]
        return


class ModelBuilder:
    def __init__(self):
        self.model = {}

    def write(self, output):
        with open(output, "w", encoding="utf8") as f:
            yaml.dump(self.model, f)

    def add_to_model(self, node, name=None, parents=[], model_type_name=None):

        # Ignore leaves
        if type(node) is not dict:
            return

        parents = list(parents)  # Copy

        # Validate that .{dynamic_keys} never have __value__ children
        # if name and name.startswith(".{") and node.get("__value__"):
        #     print("Assumption invalidated. Found dynamic key with __value__ as child")
        #     print(parents, name, node, model_type_name)
        #     exit()

        # Check whether this node starts a group for its children + self
        if node.get("__simput__", {}).get("GroupChildrenAs"):
            model_type_name = node.get("__simput__", {}).get("GroupChildrenAs")

        if name and name.startswith(".{"):
            export_prefix = ".".join(parents)

            if model_type_name:
                new_prop = {}
                nested_model_type_name = (export_prefix + name).replace(
                    ".", "_"
                )  # Storage identifier

                # Add prop to current model
                new_prop["domains"] = [
                    {
                        "type": "ProxyBuilder",
                        "values": [
                            {
                                "name": nested_model_type_name,
                                "type": nested_model_type_name,
                            }
                        ],
                    }
                ]
                self.add_model_prop(model_type_name, nested_model_type_name, new_prop)

                # Add new model with link back to old
                self.add_model_prop(
                    nested_model_type_name, "_exportPrefix", export_prefix
                )
                self.add_model_prop(
                    nested_model_type_name,
                    "name",
                    {
                        "_ui": "skip",
                        "type": "string",
                        "_help": "The name distinguishing this instance of "
                        + nested_model_type_name,
                    },
                )

                # Recurse onto children
                for key in node.keys():
                    if key == "__value__" or not key.startswith("__"):
                        self.add_to_model(
                            node.get(key),
                            key,
                            parents=[],
                            model_type_name=nested_model_type_name,
                        )

        else:
            # Decide identifiers for node
            if name and name != "__value__":
                # __value__ goes by parent's name
                parents += [name]
            export_suffix = ".".join(parents)  # Unique identifier
            property_name = export_suffix.replace(".", "_")  # Storage identifier

            # This is a property. Add to model
            if node.get("help") and model_type_name:
                new_prop = {"_exportSuffix": export_suffix}
                add_help(node, new_prop)
                add_type(node, new_prop)
                add_domains(node, new_prop, name, property_name)
                self.add_model_prop(model_type_name, property_name, new_prop)

            # Recurse onto children
            for key in node.keys():
                if key == "__value__" or not key.startswith("__"):
                    self.add_to_model(
                        node.get(key), key, parents, model_type_name=model_type_name
                    )

    def add_model_prop(self, model_type_name, property_name, new_prop):
        if not self.model.get(model_type_name):
            self.model[model_type_name] = {}

        self.model[model_type_name].update(
            {
                property_name: new_prop,
            }
        )


@click.command()
@click.option(
    "-o",
    "--output",
    default=".",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
    help="The directory to output the model file to. If no output "
    + "is provided the file will be created in the current directory.",
)
@click.option(
    "-d",
    "--def_directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
    help="The directory of definition files.",
)
@click.option(
    "-f",
    "--def_file",
    multiple=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="A definition file to use.",
)
@click.option(
    "--include-wells",
    default=False,
    help="Whether to include support for Wells. This is complicated and left out by default.",
)
@click.option(
    "--include-clm",
    default=False,
    help="Whether to include support for CLM. This is complicated and left out by default",
)
def cli(output, def_directory, def_file, include_wells, include_clm):
    """Accepts a single file, list of files, or directory name."""
    model = ModelBuilder()

    files = (
        Path(def_directory).iterdir() if def_directory else [Path(f) for f in def_file]
    )

    for f in files:
        with open(f) as value:
            data = yaml.load(value, Loader=yaml.Loader)
            model.add_to_model(data)

    model.write(f"{output}/model.yaml")


if __name__ == "__main__":
    cli()
