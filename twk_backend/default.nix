let
  pkgs = import ((import <nixpkgs> {}).fetchFromGitHub {
           owner = "NixOS";
           repo = "nixpkgs";
           rev = "2dcd512e7431001c7c0b80db60f524e2893c7654";
           sha256 = "0p9v8d168n7s5zxdhbx1jhmr400ddfk7bq2a1d5jira03m6gwhdv";
  }) { };

  inherit (pkgs) stdenv;

  # django 2.1 have iframe login unauthorized problem, to be investigated
  my_django = pkgs.python36Packages.django_2_0;

  django-cors-headers = pkgs.python3.pkgs.buildPythonPackage rec {
    version  = "2.2.0";
    pname = "django-cors-headers";
    name = pname + "-" + version;
    buildInputs = [ my_django ];
    doCheck = false;
    src = pkgs.python3.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "11xrv574fw6ng2mj46a74lhvd7ais6cp8cagp0bnaha9xhb4iv67";
    };
  };
in rec {
  env = stdenv.mkDerivation rec {
    name = "twk-bakend-env";
    version = "0.1" ;
    buildInputs = with pkgs.python36Packages;
                    [ my_django
                      requests
                      docutils
                      coverage
                      (djangorestframework.override { django = my_django; })
                    ] ++
                    [ django-cors-headers
                    ];
  } ;
}
