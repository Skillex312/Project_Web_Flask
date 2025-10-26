{pkgs, ...}: {
  channel = "stable-23.11";
  packages = [
    pkgs.python3
    pkgs.python3.pkgs.pip
    pkgs.python3.pkgs.flask
  ];
}
