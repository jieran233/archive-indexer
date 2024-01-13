# archive-indexer

## Usage

### MSYS2 (Windows), on SMB (Mounted as network driver by Explorer)

Open your SMB driver in Explorer

Type `msys2.cmd` in the address bar of explorer

```shell
pacman -S git
pacman -S coreutils unzip unrar

mkdir tools && cd tools
git clone https://github.com/jieran233/archive-indexer
cd archive-indexer
./mkindex.sh </path/to/your/archive/file>
```

### Linux, on SMB (Mounted by GNOME Nautilus)

Open your SMB root path in terminal via Nautilus

```shell
# For Debian-based Linux, the following package names are exactly the same, just replace `pacman -S` with `apt install`
sudo pacman -S git
sudo pacman -S coreutils unzip unrar

mkdir tools && cd tools
git clone https://github.com/jieran233/archive-indexer
cd archive-indexer
./mkindex.sh </path/to/your/archive/file>
```