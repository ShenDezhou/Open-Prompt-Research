# import pkg_resources
import utils as U


def load_prompt(prompt):
    # package_path = pkg_resources.resource_filename("voyager", "")
    return U.load_text(f"prompts/{prompt}.txt")
