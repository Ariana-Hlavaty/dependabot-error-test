{ pkgs, ... }:

let
  fake_k8s_jwt = pkgs.writeText "fake-k8s-jwt" "token";

  grpc_health_probe = pkgs.buildGoModule rec {
    pname = "grpc-health-probe";
    version = "0.4.34";

    src = pkgs.fetchFromGitHub {
      owner = "grpc-ecosystem";
      repo = "grpc-health-probe";
      rev = "v${version}";
      hash = "sha256-JN4zimJFfgy3ZKBqwmAncqkICaUvb+dUKddpjWNKry4=";
    };

    vendorHash = "sha256-FI2pBEvKe7Gp2NXFw6BHPQ9yBIGicog2BZVRsf7E9jo=";

    meta = with pkgs.lib; {
      description = "A command-line tool to perform health-checks for gRPC applications in Kubernetes and elsewhere ";
      homepage = "https://github.com/grpc-ecosystem/grpc-health-probe";
      license = licenses.asl20;
      maintainers = with maintainers; [ johnchildren ];
    };
  };
in
{
  env = {
    OPENSSL_DIR = "${pkgs.openssl.dev}";
    OPENSSL_LIB_DIR = "${pkgs.openssl.out}/lib";
  };

  cachix.enable = false;

  # The devenv direnv integration doesn't allow multiline env vars
  # which means we can't use it for PEM format keys.
  dotenv.enable = false;
  dotenv.disableHint = true;

  packages =
    with pkgs;
    [
      # misc utils
      git
      curl
      jq
      viu
      process-compose
      commitizen

      # python
      poetry
      black
      isort
      pandoc
      jre8
      uv
      ruff
      pyright
    ]
    ++ lib.optionals pkgs.stdenv.isLinux [ glibcLocales ]
    ++ lib.optionals pkgs.stdenv.isDarwin (
      with pkgs.darwin.apple_sdk;
      [
      ]
    );

  enterShell = ''
    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
  '';

  languages.nix.enable = true;
  languages.python = {
    enable = true;
    package = pkgs.python312;
  };
}
