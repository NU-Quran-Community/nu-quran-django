{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

let
  ruff = lib.getExe pkgs.ruff;
in
{
  languages.python = {
    enable = true;
    version = "3.12";
    venv.enable = true;
    uv = {
      enable = true;
      sync = {
        enable = true;
        allExtras = true;
      };
    };
  };

  tasks = {
    "admin:db:setup" = {
      before = [ "devenv:processes:dev-server" ];
      cwd = config.git.root;
      exec = ''
        source ''${DEVENV_STATE}/venv/bin/activate
        python ''${DEVENV_ROOT}/src/manage.py makemigrations
        python ''${DEVENV_ROOT}/src/manage.py migrate
      '';
    };
  };

  processes = {
    dev-server = {
      cwd = config.git.root;
      exec = ''
        source ''${DEVENV_STATE}/venv/bin/activate
        python ''${DEVENV_ROOT}/src/manage.py runserver
      '';
    };
  };

  git-hooks.hooks = {
    nil.enable = true;
    nixfmt.enable = true;
    ruff-format.enable = true;
    ruff = {
      enable = true;
      entry = "${ruff} check --ignore F403";
    };
  };
}
