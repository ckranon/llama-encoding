let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python313.withPackages (python-pkgs: [
      python-pkgs.psycopg
      python-pkgs.python-dotenv
    ]))
  ];
}
