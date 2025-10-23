{ pkgs, lib, config, inputs, ... }:

{
  languages.python = {
    enable = true;
    version = "3.12";
    uv.enable = true;
    venv = {
      enable = true;
      requirements = builtins.readFile ./deps/requirements.dev.txt;
    };
  };

  # https://devenv.sh/tests/
  enterTest = ''
    pytest
  '';
}
