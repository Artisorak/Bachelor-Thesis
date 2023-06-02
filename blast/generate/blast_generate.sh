echo "Compiling IC_generator_blast.cpp"
g++ -o IC_generator_blast IC_generator_blast.cpp
echo ""

echo "Running IC_generator_blast"
./IC_generator_blast 128
echo ""

echo "Calculating density with PkDGrav3"
cd ../../../pkdgrav3/build/
make
cd ../../bachelor-thesis/blast/generate
../../../pkdgrav3/build/pkdgrav3 -n0 blast_n0.par
echo ""

echo "Adjusting temperature to move particles to the same isotrope"
python3 ../../scripts/adjust_isentrope.py blast_n0.00000 1.6666666666666667
echo ""

echo "Compiling txt2tipsy.cpp"
g++ -o txt2tipsy ../../scripts/txt2tipsy.cpp
echo ""

echo "Converting to tipsy format"
./txt2tipsy blast_n0.00000_adjusted_isentrope
echo ""
echo "moving temporary files to temporary folder"
mkdir temporary
mv ic_blast_grid_128.tipsy blast_n0.00000 blast_n0.00000_adjusted_isentrope.txt temporary

echo "Renaming files"
mv blast_n0.00000_adjusted_isentrope.tipsy ../relax/blast_ic_grid_isentrope.tipsy
cp blast_ic_grid_isentrope.tipsy ~/EULER/cluster/bachelorthesis/NewSPH/pkdgrav3/run/