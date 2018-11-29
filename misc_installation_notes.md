# VMD PLUGINS

```bash
sudo port install gmake gsl xdrfile libmatheval
tar -xzvf plugins.tar && cd plugins
gmake MACOSXX86_64
sudo mkdir -p /opt/lib
sudo env PLUGINDIR=/opt/lib/vmd/plugins gmake distrib
```

# PLUMED (+mpi +vmd_plugins)

```bash
sudo port install mpich-clang70
tar -xzvf plumed-2.4.3.tar && cd plumed-2.4.3
./configure --prefix=/opt/plumed-2.4.3 LDFLAGS='-ltcl8.5 -L/usr/lib -L/opt/lib/vmd/plugins/MACOSXX86_64/molfile -L/opt/local/lib' CPPFLAGS='-I/opt/lib/vmd/plugins/include/ -I/opt/lib/vmd/plugins/MACOSXX86_64/molfile -I/opt/local/include' CXX=mpic++-mpich-clang70
make -j 4
sudo make install
```

# GROMACS (+openCL +mpi +plumed)

```bash
sudo port install clang-7.0
tar -xzvf gromacs-2018.4.tar && cd gromacs-2018.4
plumed patch -p -e gromacs-2018.3 # yeah, I know...
cmake ../gromacs-2018.4 -DCMAKE_C_COMPILER=clang-mp-7.0 -DCMAKE_CXX_COMPILER=/opt/local/bin/clang++-mp-7.0 -DGMX_GPU=ON -DGMX_USE_OPENCL=ON -DCMAKE_INSTALL_PREFIX=/opt/gromacs-2018.4 -DCMAKE_PREFIX_PATH="/opt/local" -DGMX_BUILD_OWN_FFTW=ON
sudo make install
echo "configure completions and man pages by adding
'source /opt/gromacs-2018.4/bin/GMXRC' to your ~/.${SHELL##/*/}rc"
```
