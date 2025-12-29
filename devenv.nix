{
  inputs,
  config,
  pkgs,
  lib,
  ...
}:

{
  env = {
    PYTHONPATH = "${config.git.root}/src";
    DJANGO_SETTINGS_MODULE = "nu_quran_api.settings";
    DJANGO_ENVIRONMENT = "PROD";
    DJANGO_DB_NAME = "nuqc";
    DJANGO_DB_USER = "dev";
    DJANGO_DB_PASSWORD = "dev";
  };

  languages.python = {
    enable = true;
    version = "3.13";
    venv.enable = true;
    uv = {
      enable = true;
      sync = {
        enable = true;
        allExtras = true;
        allGroups = true;
      };
    };
  };

  tasks =
    let
      git = lib.getExe pkgs.git;
      buildah = lib.getExe pkgs.buildah;
    in
    {
      "nuqc:env:version" = {
        cwd = config.git.root;
        exec = ''
          if [ -z "''${NUQC_GIT_COMMIT}" ]; then
            # NOTE: Use GitHub Actions variables when available
            if [ -n "''${GITHUB_SHA}" ]; then
              export NUQC_GIT_COMMIT="''${GITHUB_SHA}"
            else
              export NUQC_GIT_COMMIT="$(${git} rev-parse --verify HEAD)"
            fi
          fi

          export NUQC_VERSION="$(uvx setuptools-scm)"
        '';
        exports = [
          "NUQC_GIT_COMMIT"
          "NUQC_VERSION"
        ];
      };

      "nuqc:build:oci" = {
        after = [ "nuqc:env:version" ];
        exec = ''
          if grep -q .dev <<<"''${NUQC_VERSION}"; then
            NUQC_IMAGE_TAG="$(cut -d+ -f1 <<<"''${NUQC_VERSION}")"
          else
            NUQC_IMAGE_TAG="''${NUQC_VERSION}"
          fi

          ${buildah} build \
          --build-arg=VCS_REF=''${NUQC_GIT_COMMIT} \
          --build-arg=VERSION=''${NUQC_VERSION} \
          -t nu-quran-api:''${NUQC_IMAGE_TAG} .
        '';
      };
    };

  services = {
    postgres = {
      enable = true;
      listen_addresses = "localhost";
      initialDatabases = [
        {
          name = "nuqc";
          user = "dev";
          pass = "dev";
        }
      ];
    };
  };

  processes = {
    dbmigrate = {
      process-compose.depends_on.postgres.condition = "process_healthy";
      exec = ''
        django-admin makemigrations
        django-admin migrate
        django-admin setuproles
      '';
    };

    devserver = {
      process-compose.depends_on.dbmigrate.condition = "process_completed_successfully";
      exec = ''
        django-admin runserver
      '';
    };
  };

  treefmt = {
    enable = true;
    config.programs = {
      ruff-check.enable = true;
      ruff-format.enable = true;
      prettier.enable = true;
      nixfmt.enable = true;
      taplo.enable = true;
    };
  };

  git-hooks.hooks = {
    treefmt.enable = true;
  };
}
