# deepin-git-repo
deepin git version for archlinux

This repository only provides the git version of deepin. You can replace the deepin group in the community by installing the deepin-git group.

The PKGBUILD for all packages are there [https://github.com/justforlxz/deepin-git-repo](https://github.com/justforlxz/deepin-git-repo), Each branch saves the corresponding software.

Before adding this repository, you should first add the key used to sign the packages in it. You can do this by running the following commands:

```shell
wget -qO - https://packages.justforlxz.com/deepingit.asc \
    | sudo pacman-key --add -
```

It is recommended that you now fingerprint it by running

```shell
sudo pacman-key --finger DCAF15B4605D5BEB
```

and in a final step, you have to locally sign the key to trust it via

```shell
sudo pacman-key --lsign-key DCAF15B4605D5BEB
```

More infos on this process can be found at [https://wiki.archlinux.org/index.php/Pacman/Package_signing#Adding_unofficial_keys](https://wiki.archlinux.org/index.php/Pacman/Package_signing#Adding_unofficial_keys). You can now add the repository by editing /etc/pacman.conf and adding

```shell
[deepingit]
Server = https://packages.justforlxz.com/
```

at the end of the file. See [https://wiki.archlinux.org/index.php/Pacman#Repositories_and_mirrors](https://wiki.archlinux.org/index.php/Pacman#Repositories_and_mirrors) for details.

to install deepin git version:

```shell
sudo pacman -Syy deepin-git
```
