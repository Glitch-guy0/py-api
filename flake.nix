{
  description = "fastapi dev environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?ref=release-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }@inputs:
  flake-utils.lib.eachDefaultSystem 
  (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.default = pkgs.mkShell {
        # Environment variables
        EDITOR = "vim";

        packages = with pkgs; [
          python3Full
          vim
        ];

        shellHook = ''
          if [ ! -d .venv ]; then
            python3 -m venv .venv
            pip install -r requirements.txt --no-cache-dir
          fi
          source .venv/bin/activate
          echo "Running fastapi dev environment"
        '';
      };
    }
  );
}
