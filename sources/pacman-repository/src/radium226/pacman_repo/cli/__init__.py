from click import group, pass_context, Context, option
from pathlib import Path
from typing import cast

from ..models import Config
from .. import actions

@group()
@option("--repo", "repo_folder_path", type=Path, required=False)
@pass_context
def app(context: Context, repo_folder_path: Path | None):
    repo_folder_path = repo_folder_path or ( Path.cwd() / "repo" )
    context.obj = Config(
        repo_folder_path=repo_folder_path
    )


@app.command()
@pass_context
def serve(context: Context):
    config = cast(Config, context.obj)
    actions.build(config)



@app.command()
@pass_context
def build(context: Context):
    config = cast(Config, context.obj)
    actions.serve(config)
    