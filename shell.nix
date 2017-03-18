with import <nixpkgs> {}; stdenv.mkDerivation {
  name = "env";
  buildInputs = [
    sqlite
    python3
    python3Packages.flask
  ];
  shellHook = "export PYTHONPATH=.:$PYTHONPATH";
}
